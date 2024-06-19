from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time

def get_market(driver):
    driver.get("https://www.toyodiy.com/parts/q.html")
    market = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@name='market']"))
    )
    return market

def get_years(driver):
    driver.get("https://www.toyodiy.com/parts/q.html")
    years = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/td/a"))
    )
    return years

def get_makes(driver, year):
    year.click()
    makes = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr/td/a"))
    )
    return makes

def get_models_and_frames(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')[1:]  # Skip header row
    data = []
    for row in rows:
        cols = row.find_all('td')
        model = cols[0].text.strip()
        frame_codes = cols[1].text.strip()
        data.append((model, frame_codes))
    return data

def main():
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    try:
        years = get_years(driver)

        with open('scraped_data.csv', 'w', newline='') as csvfile:
            fieldnames = ['market', 'year', 'make', 'model', 'frame_codes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for year in years:
                year_text = year.text
                year.click()
                time.sleep(2)  # wait for the page to load

                makes = get_makes(driver, year)
                for make in makes:
                    make_text = make.text
                    make.click()
                    time.sleep(2)  # wait for the page to load

                    data = get_models_and_frames(driver)
                    for model, frame_codes in data:
                        writer.writerow({
                            'market': 'Japan',
                            'year': year_text,
                            'make': make_text,
                            'model': model,
                            'frame_codes': frame_codes
                        })
                    driver.back()  # go back to the year page
                    time.sleep(2)

                driver.back()  # go back to the initial page
                time.sleep(2)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()

