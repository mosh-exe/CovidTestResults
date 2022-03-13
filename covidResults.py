from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from twilio.rest import Client
import time , os


## Load the .env file 
load_dotenv()

## Get info from .env file
FIRSTNAME = os.environ.get('FIRSTNAME')
LASTNAME = os.environ.get('LASTNAME')
MCP = os.environ.get('MCP')
MCP_YEAR = os.environ.get('MCP_YEAR')
MCP_MONTH = os.environ.get('MCP_MONTH')
MCP_DAY = os.environ.get('MCP_DAY')
DOB_YEAR = os.environ.get('DOB_YEAR')
DOB_MONTH = os.environ.get('DOB_MONTH')
DOB_DAY = os.environ.get('DOB_DAY')
ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
PHONE  = os.environ.get('PHONE')
DRIVER_PATH = os.environ.get('DRIVER_PATH')


def prepareDriver():
    '''Set up webdriver for the page we want to scrape'''

    ## PATH of webdriver 
    service = Service(DRIVER_PATH)

    ## webdriver options
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=service, options=options)

    ## NL COVID-19 Test Results webpage
    driver.get("https://healthenl.ca/concerto/covidresults/")

    return driver


def fillForm(driver):
    '''Fill in all the input tags'''

    ## Form info
    firstname = driver.find_element(By.NAME, "firstname")
    firstname.clear()
    firstname.send_keys(FIRSTNAME)
    firstname.send_keys(Keys.RETURN)

    lastname = driver.find_element(By.NAME, "lastname")
    lastname.clear()
    lastname.send_keys(LASTNAME)
    lastname.send_keys(Keys.RETURN)

    mcp = driver.find_element(By.NAME, "mcp")
    mcp.clear()
    mcp.send_keys(MCP)
    mcp.send_keys(Keys.RETURN)

    mcpYear = Select(driver.find_element(By.NAME, "mcpx-year"))
    mcpYear.select_by_value(MCP_YEAR)

    mcpMonth = Select(driver.find_element(By.NAME, "mcpx-month"))
    mcpMonth.select_by_value(MCP_MONTH)

    mcpDay = Select(driver.find_element(By.NAME, "mcpx-day"))
    mcpDay.select_by_value(MCP_DAY)

    dobYear = Select(driver.find_element(By.NAME, "dob-year"))
    dobYear.select_by_value(DOB_YEAR)

    dobMonth = Select(driver.find_element(By.NAME, "dob-month"))
    dobMonth.select_by_value(DOB_MONTH)

    dobDay = Select(driver.find_element(By.NAME, "dob-day"))
    dobDay.select_by_value(DOB_DAY)

    ## Click on get results button
    getResultBtn = driver.find_element(By.ID, "resultsbtn")
    getResultBtn.click()


def sendText(messageToSend):
    '''sends a text message using the twilio api'''

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
                            body = messageToSend,
                            from_ = '+13073125159',
                            to = PHONE
    )

def covidResults():
    '''
    A basic web scraping program to get the results of a recent covid19 PCR Test
    '''

    driver = prepareDriver()
   

    ## fill in the required info
    fillForm(driver)

    ## wait for results to render
    time.sleep(1)

    ## Get most recent test results by the xpath
    getResult = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/table[2]/thead[1]/tr/th/u")
    if (getResult.text == "Most Recent Result"):
        testDate = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/table[2]/tbody/tr/td[1]/strong")
        testResults = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/table[2]/tbody/tr/td[2]/strong")
        print("Test Date: {}".format(testDate.text))
        print("Test Result: {}".format(testResults.text))
        textMessage = "\n{}\n{}\n{}".format(driver.title, testDate.text, testResults.text)
        ## send text with results
        sendText(textMessage)

    time.sleep(1)

    ## Make sure to quit driver so you're not running many instances of the webdriver
    driver.quit()


covidResults()