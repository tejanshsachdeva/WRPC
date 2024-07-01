from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
chrome_options = Options()

import time

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.wrpc.gov.in/gl/commercial-rea.html")

# Wait for the year selection element to be clickable and select 2023
wait = WebDriverWait(driver, 10)
year_2023_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@onclick=\"renderDataForYear('2023')\"]")))
year_2023_button.click()

# Define the months and year ranges
months_2023 = [
    "jan23", "feb23", "mar23", "apr23", "may23", "jun23",
    "jul23", "aug23", "sep23", "oct23", "nov23", "dec23"
]
months_2024 = ["jan24", "feb24", "mar24", "apr24"]

# Combine the lists
months = months_2023 + months_2024

for month in months:
    try:
        # Construct the URL
        url = f"https://www.wrpc.gov.in/htm/{month}/rea{month}.pdf"
        driver.get(url)
        
        # Check if the PDF is loaded by checking the current URL
        if driver.current_url == url:
            print(f"Successfully fetched PDF for {month.capitalize()}")
        else:
            print(f"Failed to fetch PDF for {month.capitalize()}")

    except Exception as e:
        print(f"Error fetching PDF for {month.capitalize()}: {e}")

# Close the browser
driver.quit()
