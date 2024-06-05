from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.google.com")

WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "gLFyf")))

input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
input_element.clear()
input_element.send_keys("keells" + Keys.ENTER)

WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Keells Online")))

link = driver.find_element(By.PARTIAL_LINK_TEXT, "Keells Online")
link.click()

try:
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[3]/div[1]/div[2]/div/div/div[4]'))
    )
    button.click()
except:
    print("The promo-product page was not found.")

try:
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[3]/div/div/div/div[1]/div[3]'))
    )
    button.click()
except:
    print("The individual product element was not found.")

time.sleep(5)

driver.quit()
