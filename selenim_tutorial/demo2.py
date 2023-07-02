from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "url_here"

driver = webdriver.Chrome()

driver.get(url)
driver.implicitly_wait(3)

my_element = driver.find_element(By.ID, 'downloadButton')
my_element.click()

# my_missing_element = driver.find_element(By.ID,"doesnt_exist")

WebDriverWait(driver, 30).until(
    EC.text_to_be_present_in_element(
        (By.CLASS_NAME, 'progress-label'),
        'Complete!'
    )
)