from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time

def extract_data_from_gmaps(url):
    options = Options()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(5)  # allow page to load (consider WebDriverWait instead)

    businesses = []
    try:
        # Example fallback XPaths
        name_xpath = '//h1[contains(@class, "DUwDvf")]'
        phone_xpath = '//button[contains(@aria-label, "Call") or contains(@data-tooltip, "Call")]/div'

        business_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, name_xpath))
        ).text

        # Optional: Get phone if exists
        try:
            phone_number = driver.find_element(By.XPATH, phone_xpath).text
        except:
            phone_number = "N/A"

        businesses.append({
            "Company Name": business_name,
            "Phone": phone_number,
            "Email": "N/A"
        })
    except Exception as e:
        print(" Error extracting data:", e)

    driver.quit()
    return businesses


def save_to_excel(data, filename="business_records.xlsx"):
    df = pd.DataFrame(data)
    if os.path.exists(filename):
        existing = pd.read_excel(filename)
        df = pd.concat([existing, df], ignore_index=True)
    df.to_excel(filename, index=False)

def search_record(company_name, filename="business_records.xlsx"):
    df = pd.read_excel(filename)
    result = df[df['Company Name'].str.contains(company_name, case=False, na=False)]
    print(result)

def show_menu():
    print("1. Extract Data")
    print("2. Save Data")
    print("3. Search Record")

    url = input("Enter the URL: ").strip()
    n = input("Want to save data (y/n): ").strip()
    data = extract_data_from_gmaps(url)
    print(data)
    if n.lower() == 'y':
        save_to_excel(data)
    p = input("Want to search data (y/n): ").strip()
    if p.lower() == 'y':
        company_name = input("Enter the company name: ").strip()
        search_record(company_name)

# if __name__== '_main_':
#     show_menu()
show_menu()