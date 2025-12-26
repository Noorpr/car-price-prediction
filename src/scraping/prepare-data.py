from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import urllib.parse as parse
import time
import os
import random
import re


def human_sleep(a = 2.5, b = 7.5):
    time.sleep(random.uniform(a, b))

def human_scroll(driver):
    height = driver.execute_script("return document.body.scrollHeight")
    for y in range(0, height, random.randint(100, 400)):
        driver.execute_script(f"window.scrollTo(0, {y})")
        human_sleep(0.1, 0.3)

CHROME_DRIVER_PATH = "E:\\webDrivers\\chromedriver.exe"
TIMEOUT = 20

service = Service(executable_path=CHROME_DRIVER_PATH)

chrome_options = webdriver.ChromeOptions()

# chrome_options.add_argument("--log-level=3")
# chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome(service=service, options=chrome_options)

df = pd.DataFrame(columns=["Model_name", "Price", "Manufacturer", "Condition", "Type", "Distance", "Details_URL"])


first_url = "https://www.contactcars.com/ar/cars?&type=car&status=4&page=60&sortBy=&sortOrder=false"

while True:
    print("initializing the process")

    parsed_url = parse.urlparse(first_url)
    query = parse.parse_qs(parsed_url.query)

    
    driver.get(first_url)
    human_scroll(driver)
    # human_sleep(3, 6)
    try:

        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "h2.sub-h-lg.text-brand-900.truncate.mt-3")
            )
        )
        human_sleep(2, 4)
    except TimeoutException:
        print("Loading took too much time!")
        break

    # time.sleep(TIMEOUT)
    html = BeautifulSoup(driver.page_source, "html.parser")

    model_names = html.select("h2.sub-h-lg.text-brand-900.truncate.mt-3")

    if not model_names:
        print("no more results, exiting...")
        driver.quit()
        break

    new_rows = []
    for result in model_names:
        model_name = result.text

        # the main div that holds information about the car
        parent = result.find_parent("div", class_="rounded-xl overflow-hidden h-full bg-white-900 w-full flex flex-col shadow-[0_2px_12px_0_rgba(0,0,0,0.10)]")
        # price information
        price_span = parent.find("span", class_="h-600 md:h-500 xl:h-600 text-brand")
        price = price_span.text if price_span else 0

        # manufacturer
        manufacturer_tag = parent.find("a", class_="flex items-center bg-brand-50 h-6 px-1 hover:underline text-brand-600 rounded-full txt-2xs")
        manufacturer = manufacturer_tag.text

        # condition
        condition_tag = parent.find("span", class_="text-neutral-800 txt-sm md:txt-2xs font-bold hover:underline")
        condition = condition_tag.text

        # more information 
        parent_div = parent.find("div", class_="flex items-center gap-1 mt-2")
        spans = parent_div.find_all("span", class_="text-neutral-800 txt-sm md:txt-2xs font-bold")

        type_val = next((
        s.get_text(strip=True)
        for s in spans
        if s.get_text(strip=True)
        and not any(c.isdigit() for c in s.get_text(strip=True))),
        None)

        distance_val = next(
            (s.get_text(strip=True) for 
            s in spans
            if s.get_text(strip=True)
            and any(c.isdigit() for c in s.get_text(strip=True))), 
            None)
        
        details_url_tag = parent.find("a", class_="block relative h-60 w-full")
        details_url = "contactcars.com" + details_url_tag.get("href") if details_url_tag else ""


        new_rows.append({"Model_name" : model_name, "Price": price, "Manufacturer" : manufacturer, "Condition": condition, "Type" : type_val, "Distance": distance_val, "Details_URL" : details_url})


    df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    print("done processing " + str(query['page'][0]) + " pages, found more than " + str(len(model_names)) + " results")

    query['page'][0] = str(int(query['page'][0]) + 1)

    new_query_string = parse.urlencode(query, doseq=True)

    modified_url = parse.urlunparse(parsed_url._replace(query=new_query_string))
    first_url = modified_url
    
    time.sleep(random.uniform(6, 12))

try:
    with open("cars_contactcars.csv", 'a', encoding='utf-8-sig') as f:
        df.to_csv("cars_contactcars.csv", mode='a',header=not os.path.exists("cars_contactcars.csv"), encoding='utf-8-sig', index=False)
except IOError as e:
    print("I/O error while writing to CSV: ", e)

driver.quit()
print(df.head())
    