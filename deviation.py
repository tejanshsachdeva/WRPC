import requests

def fetch_pdfs_for_year(year):
    year_data_url = f'https://www.wrpc.gov.in/assets/data/UI_{year}.txt'
    year_data_response = requests.get(year_data_url)
    
    if year_data_response.status_code == 200:
        pdf_data_lines = year_data_response.text.strip().split('\n')
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
                    print(pdf_url)
                else:
                    print(f"Invalid data format: {file_info}")
            else:
                print(f"Invalid line format: {line}")
    else:
        print(f"Failed to fetch data for year {year}")

# Example usage:
year = input("Enter the year (e.g., 2023): ")
fetch_pdfs_for_year(year)