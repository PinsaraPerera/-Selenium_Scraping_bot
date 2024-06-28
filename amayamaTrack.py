import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

service = Service(executable_path="/usr/local/bin/chromedriver")
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run headless Chrome
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
)

driver = webdriver.Chrome(service=service, options=options)

rows_list = []


def random_delay():
    time.sleep(random.uniform(1, 5))


def safe_click(element):
    retries = 3
    for _ in range(retries):
        try:
            element.click()
            return
        except Exception as e:
            print(f"Error clicking element: {e}. Retrying...")
            time.sleep(2)
    raise Exception(f"Failed to click element after {retries} retries")


def get_vehicle_list():
    try:
        main_div_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[2]/div/div/div/div[2]")
            )
        )

        div_elements = main_div_element.find_elements(By.TAG_NAME, "div")

        for div_index in range(len(div_elements)):
            driver.refresh()
            time.sleep(3)
            random_delay()

            try:
                main_div_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div[2]")
                    )
                )
                div_elements = main_div_element.find_elements(By.TAG_NAME, "div")
                div_element = div_elements[div_index]
                a_elements = div_element.find_elements(By.TAG_NAME, "a")

                for a_index in range(len(a_elements)):
                    driver.refresh()
                    time.sleep(5)
                    random_delay()
                    try:
                        main_div_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "/html/body/div[2]/div/div/div/div[2]")
                            )
                        )
                        div_elements = main_div_element.find_elements(
                            By.TAG_NAME, "div"
                        )
                        div_element = div_elements[div_index]
                        a_elements = div_element.find_elements(By.TAG_NAME, "a")
                        a_element = a_elements[a_index]

                        # Wait until the element is clickable and scroll to it
                        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable(a_element)
                        )
                        driver.execute_script(
                            "arguments[0].scrollIntoView(true);", a_element
                        )
                        driver.execute_script("arguments[0].click();", a_element)

                        #                         safe_click(a_element)

                        # Get current page URL
                        current_url = driver.current_url
                        vehicle_url = current_url
                        print(f"Current URL: {current_url}")

                        # Re-locate the markets_div_element after navigation
                        markets_div_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "/html/body/div[2]/div/div/div/div[2]")
                            )
                        )

                        markets = markets_div_element.find_elements(By.TAG_NAME, "div")

                        for market_index in range(len(markets)):
                            driver.refresh()
                            time.sleep(5)
                            random_delay()
                            try:
                                markets_div_element = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located(
                                        (
                                            By.XPATH,
                                            "/html/body/div[2]/div/div/div/div[2]",
                                        )
                                    )
                                )
                                markets = markets_div_element.find_elements(
                                    By.TAG_NAME, "div"
                                )
                                market = markets[market_index]

                                market_tags = market.find_elements(
                                    By.CLASS_NAME, "market__title"
                                )
                                if not market_tags:
                                    print(
                                        f"Market title not found at div {div_index}, a {a_index}, market {market_index}"
                                    )
                                    continue
                                market_tag = market_tags[0]
                                market_name = market_tag.text

                                chassi_models_tag = market.find_elements(
                                    By.TAG_NAME, "a"
                                )

                                for chassi_index in range(len(chassi_models_tag)):
                                    try:
                                        markets_div_element = WebDriverWait(
                                            driver, 10
                                        ).until(
                                            EC.presence_of_element_located(
                                                (
                                                    By.XPATH,
                                                    "/html/body/div[2]/div/div/div/div[2]",
                                                )
                                            )
                                        )
                                        markets = markets_div_element.find_elements(
                                            By.TAG_NAME, "div"
                                        )
                                        market = markets[market_index]

                                        chassi_models_tag = market.find_elements(
                                            By.TAG_NAME, "a"
                                        )
                                        a1_element = chassi_models_tag[chassi_index]

                                        chassi_model_name = a1_element.text

                                        # Wait until the element is clickable and scroll to it
                                        WebDriverWait(driver, 10).until(
                                            EC.element_to_be_clickable(a1_element)
                                        )
                                        driver.execute_script(
                                            "arguments[0].scrollIntoView(true);",
                                            a1_element,
                                        )
                                        driver.execute_script(
                                            "arguments[0].click();", a1_element
                                        )
                                        #                                         safe_click(a1_element)

                                        # Get current page URL
                                        current_url = driver.current_url
                                        print(f"Current URL: {current_url}")

                                        # Re-locate the table_element after navigation
                                        table_element = WebDriverWait(driver, 10).until(
                                            EC.presence_of_element_located(
                                                (
                                                    By.XPATH,
                                                    "/html/body/div[2]/div/div[2]/table/tbody",
                                                )
                                            )
                                        )

                                        table_rows = table_element.find_elements(
                                            By.CLASS_NAME, "epcVariations__row"
                                        )

                                        for table_row in table_rows:
                                            table_data = table_row.find_elements(
                                                By.TAG_NAME, "td"
                                            )

                                            model_tag = table_data[0].find_element(
                                                By.TAG_NAME, "a"
                                            )
                                            model_name = model_tag.text

                                            engine_tag = table_data[1].find_element(
                                                By.TAG_NAME, "span"
                                            )
                                            engine_name = engine_tag.text
                                            engine_name_code = engine_tag.get_attribute(
                                                "data-content"
                                            )

                                            prod_period_name = table_data[2].text

                                            # Handle potential empty <td> for body
                                            try:
                                                body_tag = table_data[3].find_element(
                                                    By.TAG_NAME, "span"
                                                )
                                                body_name = body_tag.text
                                                body_name_code = body_tag.get_attribute(
                                                    "data-content"
                                                )
                                            except:
                                                body_name = ""
                                                body_name_code = ""

                                            # Handle potential empty <td> for grade
                                            try:
                                                grade_tag = table_data[4].find_element(
                                                    By.TAG_NAME, "span"
                                                )
                                                grade_name = grade_tag.text
                                                grade_name_code = (
                                                    grade_tag.get_attribute(
                                                        "data-content"
                                                    )
                                                )
                                            except:
                                                grade_name = ""
                                                grade_name_code = ""

                                            # Handle potential empty <td> for transmission
                                            try:
                                                transmission_tag = table_data[
                                                    5
                                                ].find_element(By.TAG_NAME, "span")
                                                transm_name = transmission_tag.text
                                                transm_name_code = (
                                                    transmission_tag.get_attribute(
                                                        "data-content"
                                                    )
                                                )
                                            except:
                                                transm_name = ""
                                                transm_name_code = ""

                                            options = table_data[6].find_elements(
                                                By.TAG_NAME, "span"
                                            )
                                            option_names = {
                                                option.text: option.get_attribute(
                                                    "data-content"
                                                )
                                                for option in options
                                            }

                                            new_row = {
                                                "Brand": "Toyota",  # Replace with actual brand if needed
                                                "Vehicle": vehicle_name,
                                                "Market": market_name,
                                                "Page_URL": vehicle_url,
                                                "Chassi_model": chassi_model_name,
                                                "Model": model_name,
                                                "Engine": engine_name,
                                                "Engine_code": engine_name_code,
                                                "Prod period": prod_period_name,
                                                "Body": body_name,
                                                "Body_code": body_name_code,
                                                "Grade": grade_name,
                                                "Grade_code": grade_name_code,
                                                "Transm": transm_name,
                                                "Transm_code": transm_name_code,
                                                "Options": option_names,
                                            }

                                            rows_list.append(new_row)

                                    except Exception as e:
                                        print(
                                            f"Error processing chassi model at div {div_index}, a {a_index}, market {market_index}, chassi {chassi_index}: {e}"
                                        )
                                    finally:
                                        driver.back()
                                        time.sleep(2)
                                        random_delay()

                            except Exception as e:
                                print(
                                    f"Error processing market at div {div_index}, a {a_index}, market {market_index}: {e}"
                                )
                                # Re-locate the elements to avoid stale reference
                                markets_div_element = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located(
                                        (
                                            By.XPATH,
                                            "/html/body/div[2]/div/div/div/div[2]",
                                        )
                                    )
                                )
                                markets = markets_div_element.find_elements(
                                    By.TAG_NAME, "div"
                                )
                            finally:
                                if chassi_index != (len(chassi_models_tag) - 1):
                                    print(chassi_index, len(chassi_models_tag) - 1)
                                    driver.back()
                                time.sleep(2)

                    except Exception as e:
                        print(
                            f"Error processing vehicle at div {div_index}, a {a_index}: {e}"
                        )
                        # Re-locate the elements to avoid stale reference
                        main_div_element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "/html/body/div[2]/div/div/div/div[2]")
                            )
                        )
                        div_elements = main_div_element.find_elements(
                            By.TAG_NAME, "div"
                        )
                    finally:
                        driver.back()
                        time.sleep(2)
            except Exception as e:
                print(f"Error processing div {div_index}: {e}")
                main_div_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "/html/body/div[2]/div/div/div/div[2]")
                    )
                )
                div_elements = main_div_element.find_elements(By.TAG_NAME, "div")
            finally:
                #                 driver.back()
                time.sleep(2)
    except Exception as e:
        print(f"Error in main process: {e}")


if __name__ == "__main__":
    driver.get("https://www.amayama.com/en/catalogs/honda")
    get_vehicle_list()
    driver.quit()

    # Convert the list of dictionaries to a DataFrame and save as CSV
    try:
        output_file = "vehicle_data.csv"
        df = pd.DataFrame(rows_list)
        df.to_csv(output_file, index=False)
        print(df)
    except PermissionError as pe:
        print(f"PermissionError: {pe}")
    except Exception as e:
        print(f"An error occurred while saving the CSV file: {e}")
