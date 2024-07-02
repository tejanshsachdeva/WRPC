import requests
import fitz  # PyMuPDF
import pandas as pd
import re
import os

# Dictionary to map month numbers to their names
months = {
    'jan': 'January', 'feb': 'February', 'mar': 'March', 'apr': 'April',
    'may': 'May', 'jun': 'June', 'jul': 'July', 'aug': 'August',
    'sep': 'September', 'oct': 'October', 'nov': 'November', 'dec': 'December'
}

# Start and end year-month
start_year = 2023
end_year = 2024
start_month = 'jan'
end_month = 'apr'

# Function to generate month-year combinations
def month_year_range(start_month, start_year, end_month, end_year):
    current_year = start_year
    current_month = start_month
    while True:
        yield current_month, current_year
        if current_year == end_year and current_month == end_month:
            break
        current_month = list(months.keys())[(list(months.keys()).index(current_month) + 1) % 12]
        if current_month == 'jan':
            current_year += 1

# Function to fetch the PDF
def fetch_pdf(month, year):
    if month == 'apr' and year == 2023:
        url = f"https://www.wrpc.gov.in/htm/apr23/reaapr23.1.pdf"
    else:
        url = f"https://www.wrpc.gov.in/htm/{month}{str(year)[2:]}/rea{month}{str(year)[2:]}.pdf"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Successfully fetched {months[month]} {year}")
        temp_pdf_path = f"{month}{year}.pdf"
        with open(temp_pdf_path, 'wb') as f:
            f.write(response.content)
        return temp_pdf_path
    else:
        print(f"Failed to fetch {months[month]} {year}")
        return None

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    document = fitz.open(pdf_path)
    text = ""
    # Iterate through each page
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()
    return text


# Function to parse the text and extract data using regex
def parse_text(text):
    # Use regex to find lines containing generator names and their respective data
    pattern = r"(\S+)\s+([\d\.]+)\s+([\d\.]+)\s+([\d\.]+)"
    matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
    
    data = []
    for match in matches:
        generator = match[0]
        schedule_mu = match[1]
        actual_mu = match[2]
        deviation_mu = match[3]
        if generator.lower().startswith('arinsun'):
            data.append(['Arinsun_RUMS', schedule_mu, actual_mu, deviation_mu])

    return data


def create_dataframe(data):
    # Create a DataFrame from the parsed data
    df = pd.DataFrame(data, columns=['RE Generator', 'Schedule (MU)', 'Actual (MU)', 'Deviation (MU)'])
    return df

# Loop through each month-year combination, fetch the PDF, extract and display the data
for month, year in month_year_range(start_month, start_year, end_month, end_year):
    pdf_path = fetch_pdf(month, year)
    if pdf_path:
        text = extract_text_from_pdf(pdf_path)
        data = parse_text(text)
        if data:
            df = create_dataframe(data)
            print(f"Data for {months[month]} {year}:")
            print(df)
        else:
            print(f"No data found for {months[month]} {year}")
        print("\n")
        os.remove(pdf_path)  # Clean up the temporary PDF file
