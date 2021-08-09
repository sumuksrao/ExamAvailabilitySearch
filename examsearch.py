from selenium import webdriver
from selenium.webdriver.support.ui import Select
import fbchat
import time

# Enter the dates you want in MMDD format and then the locations and the year in YYYY
dates = ['0601', '0602', '0603', '0604', '0605', '0606', '0607']
year = '2020'
# Enter list of locations as well as home state in abbreviation
locations = ['san fransisco', 'dallas', 'seattle', 'miami', 'orlando']
home_state = 'CA'

# Specify True if you want to connect FB Message plugin
facebook = False

# Username and password for your facebook account
username = 'USERNAME'
password = 'PASSWORD'

# Enter website for Exam. Please note this was only built for STEP Exams
website = ''

if facebook:
    client = fbchat.Client(username, password)
    # Searching for friends by name and selecting the first response hence [0]
    friends = client.searchForUsers('NAME_OF_FRIEND')
    friend1 = friends[0]


# Dictionary converting month value to what the website expects
month_values = {'05': '5 ' + year, '06': '6 ' + year}

# Path to your chromedriver location
chromedriver_location = r"/Users/sumuksrao/downloads/chromedriver"
options = webdriver.ChromeOptions()
# Adding headless makes this run in the background. Comment line to see browser
options.add_argument('headless')
driver = webdriver.Chrome(chromedriver_location, options=options)
# Going to this website
driver.get(website)

# Finding the State dropdown on the website and selecting NY
select = Select(driver.find_element_by_id('masterPage_cphPageBody_ddlStateProvince'))
select.select_by_value(home_state)

# Going to the next page and selecting seat selection
driver.find_element_by_id('masterPage_cphPageBody_btnNext').click()
driver.find_element_by_id('masterPage_cphPageBody_lnkSeatAvail2').click()

i = 0
while True:
    # Sleep is used to let the webpage load before we continue
    time.sleep(7)
    # Filling in and searching for a specific location
    driver.find_element_by_id('txtSearch').send_keys(locations[i])
    driver.find_element_by_id('btnSearch').click()
    time.sleep(3)

    # Getting the first location in the results and checking its availability
    driver.find_element_by_xpath(
        r'//*[@id="pSiteDisplay"]//*[@id="sites_area"]//*[@id="sites_container"]/table/tbody/tr[1]/td[3]/a[1]').click()
    time.sleep(2)
    available_dates = []

    for date in dates:
        # Finding out which month the calendar is showing
        current_month = driver.find_element_by_id('masterPage_cphPageBody_monthYearlist').get_attribute("value")
        # If the month is different than what we're about to look for then going to the right month
        if current_month != month_values[date[0:2]]:
            select = Select(driver.find_element_by_id('masterPage_cphPageBody_monthYearlist'))
            # Getting month value from date and converting it into the website's format
            select.select_by_value(month_values[date[0:2]])
            driver.find_element_by_id(r'masterPage_cphPageBody_btnGoCal').click()
            time.sleep(2)

        # Getting the value of the date of interest
        val = driver.find_element_by_xpath(r'//*[@id="2020%s"]' % date).get_attribute("class")

        # If date is not grayed out we add it to the lsit
        if val != 'calInactive':
            available_dates.append(date)

    # If there are any available dates, then send a message
    if (len(available_dates) > 0):
        if facebook:
            client.sendMessage(locations[i] + ': ' + str(available_dates), thread_id=friend1.uid)
        else:
            print(locations[i] + ': ' + str(available_dates))

    # Go back to the previous page to search another city
    driver.find_element_by_id('masterPage_cphPageBody_btnBack').click()

    # If you reached the end of the list then go back to first element
    if i == len(locations) - 1:
        i = 0
    else:
        i += 1

driver.close()
