import requests
import pdfplumber
from tabulate import tabulate
from io import BytesIO
from datetime import datetime

def fetch_pdfs_for_year(year):
    year_data_url = f'https://www.wrpc.gov.in/assets/data/UI_{year}.txt'
    year_data_response = requests.get(year_data_url)
    
    if year_data_response.status_code == 200:
        pdf_data_lines = year_data_response.text.strip().split('\n')
        pdf_urls = []
        for line in pdf_data_lines:
            if line.strip().startswith('//') or not line.strip():
                continue
            pdf_details = line.split(',')
            
            if len(pdf_details) >= 3:
                file_info = pdf_details[2]
                
                # Extract month, year, and week from the file_info
                parts = file_info.split('&yy=')
                if len(parts) == 2:
                    week = parts[0].split('=')[1]
                    month_year = parts[1].split('.')[0]
                    
                    # Construct the PDF URL
                    pdf_url = f'https://www.wrpc.gov.in/htm/{month_year}/sum{week}.pdf'
                    pdf_urls.append(pdf_url)
                else:
                    print(f"Invalid data format: {file_info}")
            else:
                print(f"Invalid line format: {line}")
        
        if pdf_urls:
            print("List of PDFs for the year {}: ".format(year))
            for idx, url in enumerate(pdf_urls):
                print(f"{idx}. {url}")
        else:
            print(f"No PDF URLs found for year {year}")
        
        return pdf_urls
    else:
        print(f"Failed to fetch data for year {year}")
        return []

def extract_all_table_rows_from_url(pdf_url, search_term):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_file = BytesIO(response.content)
        with pdfplumber.open(pdf_file) as pdf:
            all_rows = []
            summary_rows = []
            week = pdf_url.split('/')[-2]  # Extract week from URL
            week_name = f"week-{week[-1]} {week[:-1]}"
            for page in pdf.pages:
                text = page.extract_text()
                print(f"Checking page {page.page_number}...")
                if search_term in text:
                    print(f"Found '{search_term}' on page {page.page_number}.")
                    lines = text.split('\n')
                    for i, line in enumerate(lines):
                        if search_term in line:
                            print(f"Processing line: {line}")
                            if i > 0 and "Sr." in lines[i - 1]:
                                headers1 = "Sr. || Name of Entity || Payable || Receivable || Net DSM (Rs.) || Payable/Receivable"
                                row = line.split()
                                row[0] = week_name  # Replace Sr. with week name
                                summary_rows.append((headers1, row))
                                print(f"Added row with header: {headers1}")
                            elif "Daywise Summary" in line:
                                headers2 = line
                                daywise_data = [row.split() for row in lines[i + 2:i + 9] if row.strip()]  # Adjust indices to skip headers and get data rows
                                all_rows.append((headers2, daywise_data))
                                print(f"Added daywise summary with header: {headers2}")
                                break  # Stop processing after adding daywise summary
                            elif not any(header in line for header in ["Daywise Summary", "Date Entity", "Total"]):
                                # Capture any other lines containing the search term
                                summary_rows.append(("Summary Row", line.split()))
                                print(f"Added summary row: {line}")
            return all_rows, summary_rows
    else:
        print(f"Failed to fetch the PDF from URL: {pdf_url}")
        return [], []

def display_results(results, summary_rows, search_term):
    if results or summary_rows:
        print(f"\nResults found for '{search_term}':")

        # Separate summary rows and daywise summary rows
        summary_rows = [(headers, row) for headers, row in summary_rows if headers == "Summary Row" or "Sr." in headers]
        daywise_rows = [(headers, row) for headers, row in results if headers.startswith("Daywise Summary")]

        if summary_rows:
            print("\nSummary Rows:")
            headers1 = "Week || Name of Entity || Payable || Receivable || Net DSM (Rs.) || Payable/Receivable"
            for headers, row in summary_rows:
                print(tabulate([row], headers=headers1.split(" || "), tablefmt="grid"))
                print("\n")

        # Print Daywise Summary Rows
        if daywise_rows:
            print("\nDaywise Summary Rows:")
            headers2 = "Date || Entity || Injection || Schedule || DSM Payable || DSM Receivable || Net DMC"
            all_daywise_rows = []
            for headers, rows in daywise_rows:
                all_daywise_rows.extend(rows)
            
            # Sort by date
            all_daywise_rows.sort(key=lambda x: datetime.strptime(x[0], "%d-%b"))

            print(tabulate(all_daywise_rows, headers=headers2.split(" || "), tablefmt="grid"))
            print("\n")
    else:
        print(f"No results found for '{search_term}'.")

    # Print the number of results
    print(f"Total results found: {len(results) + len(summary_rows)}")

# Example usage:
year = input("Enter the year (e.g., 2023): ")
pdf_urls = fetch_pdfs_for_year(year)

if pdf_urls:
    indices = input("Enter the indices of the PDFs to search (e.g., 0,1,2): ")
    indices = list(map(int, indices.split(',')))
    search_term = input("Enter the name to search for (e.g., Athena_RUMS): ")
    
    all_results = []
    all_summary_rows = []
    for index in indices:
        pdf_url = pdf_urls[index]
        results, summary_rows = extract_all_table_rows_from_url(pdf_url, search_term)
        all_results.extend(results)
        all_summary_rows.extend(summary_rows)
    
    display_results(all_results, all_summary_rows, search_term)
