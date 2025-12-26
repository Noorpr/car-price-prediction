import pandas as pd
import json
from curl_cffi import requests
import re
import random
import time
from tqdm import tqdm

def extract_field(field, text):
    pattern = rf'\\"{field}\\"\s*:\s*\\"([^\\"]+)\\"'
    m = re.search(pattern, text)
    return m.group(1) if m else None


df = pd.read_csv("cars_contactcars.csv")

urls = df["Details_URL"].tolist()

new_rows = []

with requests.Session() as s:
    # 3. Wrap your loop in tqdm for a visual progress bar
    # 'unit="req"' labels the progress as requests
    for i in tqdm(range(len(urls)), desc="Scraping Cars", unit="req"):
        try:
            # 4. Use the session 's' instead of 'requests'
            # Note: impersonate="chrome" automatically selects the latest stable version
            response = s.get(urls[i], impersonate="chrome", timeout=10)
            
            # Check for Cloudflare block or server error
            if response.status_code != 200:
                tqdm.write(f"Warning: URL {i} returned status {response.status_code}")
                new_rows.append({
                    "URL" : urls[i],
                    "Color" : None,
                    "Body_type" : None,
                    "Fuel_type" : None,
                    "Engine_cc" : None
                })
                continue

            # Extract fields
            color = extract_field("color", response.text)
            body_type = extract_field("bodyType", response.text)
            fuel_type = extract_field("fuelType", response.text)
            engine_cc = extract_field("engineDisplacement", response.text)

            new_rows.append({
                "URL" : urls[i],
                "Color": color, 
                "Body_type": body_type, 
                "Fuel_type": fuel_type, 
                "Engine_cc": engine_cc
            })

            # 5. RANDOM DELAY (Essential for bypassing Cloudflare)
            # Mimics a human browsing speed (2 to 5 seconds)
            time.sleep(random.uniform(2, 5))
            
            # Longer pause every 15 requests to simulate "reading" the page
            if (i + 1) % 15 == 0:
                time.sleep(random.randint(5, 10))

        except Exception as e:
            tqdm.write(f"Critical error at index {i}: {e}")
            # If a connection error occurs, wait longer before retrying the next URL
            new_rows.append({
                    "URL" : urls[i],
                    "Color" : None,
                    "Body_type" : None,
                    "Fuel_type" : None,
                    "Engine_cc" : None
                })
            time.sleep(30) 
        

print(len(new_rows))

result_df = pd.DataFrame(new_rows)
result_df.to_csv("detailed_urls_data.csv", encoding='utf-8-sig', index=False)
