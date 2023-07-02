from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

url = "url_here"

driver = webdriver.Chrome()

driver.get(url)
driver.implicitly_wait(5)

try:
    popup_class_name = 'at-cm-no-button'
    no_button = driver.find_element(By.CLASS_NAME, popup_class_name)
    no_button.click()
except:
    print('No element with class name \"{popup_class_name}\". skipping')

sum1_element = driver.find_element(By.ID, 'sum1')
sum2_element = driver.find_element(By.ID, 'sum2')

sum1_element.send_keys(Keys.NUMPAD1, Keys.NUMPAD6)
sum2_element.send_keys('13')

btn = driver.find_element(By.CSS_SELECTOR,'button[onclick="return total()"]')
btn.click()
