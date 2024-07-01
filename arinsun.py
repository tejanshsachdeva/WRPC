import requests

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
    else:
        print(f"Failed to fetch {months[month]} {year}")

# Loop through each month-year combination and fetch the PDF
for month, year in month_year_range(start_month, start_year, end_month, end_year):
    fetch_pdf(month, year)
