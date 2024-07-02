import os
import PyPDF2
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests

def extract_arinsun_data(pdf_path, table_header, search_term):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        in_target_table = False
        for page in pdf_reader.pages:
            text = page.extract_text()
            lines = text.split('\n')
            for line in lines:
                if table_header in line:
                    in_target_table = True
                    continue
                if in_target_table and search_term in line:
                    match = re.search(rf'{search_term}\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', line)
                    if match:
                        return f"{search_term} {match.group(1)} {match.group(2)} {match.group(3)}"
                if in_target_table and line.strip() == '':
                    in_target_table = False
    return None

def fetch_and_process_pdfs():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    months_2023 = [
        "jan23", "feb23", "mar23", "apr23", "may23", "jun23",
        "jul23", "aug23", "sep23", "oct23", "nov23", "dec23"
    ]
    months_2024 = ["jan24", "feb24", "mar24", "apr24"]
    months = months_2023 + months_2024

    table_header = "RE Generator Schedule (MU) Actual (MU) Deviation (MU)"
    search_term = "Arinsun_RUMS"

    results = {}

    for month in months:
        url = f"https://www.wrpc.gov.in/htm/{month}/rea{month}.pdf"
        pdf_path = f"rea{month}.pdf"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(pdf_path, 'wb') as pdf_file:
                    pdf_file.write(response.content)
                print(f"Successfully downloaded PDF for {month.capitalize()}")
                
                arinsun_data = extract_arinsun_data(pdf_path, table_header, search_term)
                if arinsun_data:
                    results[month] = arinsun_data
                else:
                    results[month] = "Data not found"
                
                os.remove(pdf_path)  # Remove the PDF after processing
            else:
                print(f"Failed to download PDF for {month.capitalize()}")
                results[month] = "PDF not available"
        except Exception as e:
            print(f"Error processing PDF for {month.capitalize()}: {e}")
            results[month] = f"Error: {str(e)}"

    driver.quit()
    return results

if __name__ == "__main__":
    results = fetch_and_process_pdfs()
    for month, data in results.items():
        print(f"{month.capitalize()}: {data}")