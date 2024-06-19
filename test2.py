from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)


def get_vehicle_makes_below(driver):
    try:

        a_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="wMK"]/a'))
        )

        make = a_element.text
        print(make)

    except Exception as e:
        print(e)
        return []


def get_vehicle_makes(driver):
    try:

        tbody_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="wMK"]/div/table/tbody'))
        )

        # Find all <tr> elements within the <tbody>
        tr_element = tbody_element.find_elements(By.TAG_NAME, "tr")

        td_element = tr_element[0].find_elements(By.TAG_NAME, "td")

        # Find all <a> tags within the <td> element
        a_tags = td_element[0].find_elements(By.TAG_NAME, "a")

        for a_tag in a_tags:
            make = a_tag.text
            print(make)

        return "ok"

    except Exception as e:
        print(e)
        return []


def get_years(driver, tr_index=0, td_index=0):
    try:
        tbody_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="wYR"]/div/table/tbody'))
        )

        # Find all <tr> elements within the <tbody>
        tr_elements = tbody_element.find_elements(By.TAG_NAME, "tr")

        for i in range(tr_index, len(tr_elements)):
            tr = tr_elements[i]
            # Find all <td> elements within each <tr>
            td_elements = tr.find_elements(By.TAG_NAME, "td")

            for j in range(td_index, len(td_elements)):
                td = td_elements[j]
                # Find all <a> tags within each <td>
                a_tags = td.find_elements(By.TAG_NAME, "a")

                if not a_tags:
                    continue

                year = a_tags[0].text
                a_tags[0].click()
                time.sleep(2)

                if int(year) <= 2000:
                    makes = get_vehicle_makes_below(driver)
                else:
                    makes = get_vehicle_makes(driver)

                # Go back to the year list
                back_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="wYR"]/a'))
                )
                back_element.click()
                time.sleep(2)

                # Call the function recursively to handle the next td_element
                get_years(driver, i, j + 1)

        return

    except Exception as e:
        print(e)
        return


def get_market_data(driver, start_index=0):
    try:
        # Wait for the specific <td> element to be present
        td_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="wM"]/div/table/tbody/tr/td')
            )
        )

        # Find all <a> tags within the <td> element
        a_tags = td_element.find_elements(By.TAG_NAME, "a")

        for i in range(start_index, len(a_tags)):
            a_tag = a_tags[i]
            market_name = a_tag.text
            if market_name == "Japan" or market_name == "Other":
                a_tag.click()
                time.sleep(2)
                get_years(driver)
                # Click on the back element
                back_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="wM"]/a'))
                )
                back_element.click()
                time.sleep(2)
                # Call the function recursively to handle the next market
                get_market_data(driver, i + 1)

        return

    except Exception as e:
        print(e)
        driver.quit()


if __name__ == "__main__":
    driver.get("https://www.toyodiy.com/parts/q.html")

    # with open('market_data.csv', mode='w', newline='', encoding='utf-8') as file:
    # csv_writer = csv.writer(file)
    # csv_writer.writerow(['Market', 'Year', 'Make'])  # Write the header
    # get_market_data(driver, csv_writer)

    get_market_data(driver)

    driver.quit()
