import streamlit as st
import requests
import pdfplumber
from io import BytesIO
from datetime import datetime
import pandas as pd

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
                
                parts = file_info.split('&yy=')
                if len(parts) == 2:
                    week = parts[0].split('=')[1]
                    month_year = parts[1].split('.')[0]
                    
                    pdf_url = f'https://www.wrpc.gov.in/htm/{month_year}/sum{week}.pdf'
                    pdf_urls.append(pdf_url)
                else:
                    st.warning(f"Invalid data format: {file_info}")
            else:
                st.warning(f"Invalid line format: {line}")
        
        return pdf_urls
    else:
        st.error(f"Failed to fetch data for year {year}")
        return []

def filter_summary_rows(summary_rows):
    # Function to filter out unwanted summary rows
    filtered_rows = []
    for headers, row in summary_rows:
        if not any(keyword in row for keyword in ["WRPC", "Daywise Summary", "Date Entity", "Total", "-", ":", "to", "Page"]):
            filtered_rows.append((headers, row))
    return filtered_rows


def extract_all_table_rows_from_url(pdf_url, search_term):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_file = BytesIO(response.content)
        with pdfplumber.open(pdf_file) as pdf:
            all_rows = []
            summary_rows = []
            week = pdf_url.split('/')[-2]
            week_name = f"week-{week[-1]} {week[:-1]}"
            found_in_first_nine_pages = False
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if search_term in text:
                    if page_num < 9:
                        found_in_first_nine_pages = True
                    lines = text.split('\n')
                    for i, line in enumerate(lines):
                        if search_term in line:
                            if i > 0 and "Sr." in lines[i - 1]:
                                headers1 = "Sr. || Name of Entity || Payable || Receivable || Net DSM (Rs.) || Payable/Receivable"
                                row = line.split()
                                row[0] = week_name
                                if len(row) != 6:  # Adjust this check based on actual column count
                                    print(f"Irrelevant line (invalid columns): {line}")  # Debug print
                                    continue
                                summary_rows.append((headers1, row))
                            elif "Daywise Summary" in line:
                                headers2 = line
                                daywise_data = []
                                for j in range(i + 2, min(i + 9, len(lines))):
                                    daywise_row = lines[j].split()
                                    if len(daywise_row) != 7:  # Adjust this check based on actual column count
                                        print(f"Irrelevant daywise data (invalid columns): {lines[j]}")  # Debug print
                                        continue
                                    daywise_data.append(daywise_row)
                                print(f"Daywise Data: {daywise_data}")  # Debug print
                                all_rows.append((headers2, daywise_data))
                                break
                            elif any(keyword in line for keyword in ["-", ":", "to", "Page"]):
                                continue
                            elif any(keyword in line for keyword in ["WRPC", "Daywise Summary", "Date Entity", "Total"]):
                                continue
                            else:
                                print(f"Irrelevant line: {line}")  # Debug print
                                summary_rows.append(("Summary Row", line.split()))
            if not found_in_first_nine_pages:
                summary_rows = []

            return all_rows, summary_rows
    else:
        st.error(f"Failed to fetch the PDF from URL: {pdf_url}")
        return [], []


def display_results(results, summary_rows, search_term):
    if results or summary_rows:
        st.success(f"\nResults found for '{search_term}':")

        summary_rows = [(headers, row) for headers, row in summary_rows if headers == "Summary Row" or "Sr." in headers]
        daywise_rows = [(headers, row) for headers, row in results if headers.startswith("Daywise Summary")]

        if summary_rows:
            st.subheader("Summary Rows:")
            headers1 = ["Week", "Name of Entity", "Payable", "Receivable", "Net DSM (Rs.)", "Payable/Receivable"]
            summary_data = [row for headers, row in summary_rows if headers == "Summary Row"]
            summary_df = pd.DataFrame(summary_data, columns=headers1)
            st.dataframe(summary_df)

        if daywise_rows:
            st.subheader("Daywise Summary Rows:")
            headers2 = ["Date", "Entity", "Injection", "Schedule", "DSM Payable", "DSM Receivable", "Net DMC"]
            daywise_data = [row for headers, rows in daywise_rows for row in rows]
            daywise_df = pd.DataFrame(daywise_data, columns=headers2)
            try:
                # Convert 'Date' column to datetime, then format it back to string
                daywise_df['Date'] = pd.to_datetime(daywise_df['Date'], format='%d-%b')
                daywise_df['Date'] = daywise_df['Date'].dt.strftime('%d %B')
                daywise_df = daywise_df.sort_values('Date')
            except ValueError as e:
                st.warning(f"Date parsing error: {e}")
            st.dataframe(daywise_df)
    else:
        st.warning(f"No results found for '{search_term}'.")

    st.info(f"Total results found: {len(results) + len(summary_rows)}")

def convert_to_excel(summary_rows, daywise_rows):
    summary_headers = ["Week", "Name of Entity", "Payable", "Receivable", "Net DSM (Rs.)", "Payable/Receivable"]
    daywise_headers = ["Date", "Entity", "Injection", "Schedule", "DSM Payable", "DSM Receivable", "Net DMC"]

    summary_data = [row for headers, row in summary_rows if headers == "Summary Row"]
    daywise_data = [row for headers, rows in daywise_rows for row in rows]

    summary_df = pd.DataFrame(summary_data, columns=summary_headers)
    daywise_df = pd.DataFrame(daywise_data, columns=daywise_headers)
    

    buffer = BytesIO()
    try:
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            summary_df.to_excel(writer, sheet_name="Summary Rows", index=False)
            daywise_df.to_excel(writer, sheet_name="Daywise Summary Rows", index=False)
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"An error occurred while creating the Excel file: {e}")
        return None

def main():
    # Streamlit App
    st.title("Deviation Settlement Mechanism (DSM) Data Extractor")

    if st.button("Back to Home"):
        st.session_state.app_choice = None
        st.rerun()

    all_pdf_urls = []

    years_input = st.text_input("Enter the years (e.g., 2023,2024):")
    if years_input:
        years = years_input.split(',')
        index_offset = 0

        for year in years:
            year = year.strip()
            pdf_urls = fetch_pdfs_for_year(year)
            if pdf_urls:
                with st.expander(f"List of PDFs for the year {year}: "):
                    for idx, url in enumerate(pdf_urls):
                        st.write(f"{index_offset + idx}. {url}")
                index_offset += len(pdf_urls)
                all_pdf_urls.extend(pdf_urls)

    if all_pdf_urls:
        indices_input = st.text_input("Enter the indices of the PDFs to search (e.g., 0,1,2):")
        if indices_input:
            try:
                indices = list(map(int, indices_input.split(',')))
                search_term = st.text_input("Enter the name to search for (e.g., Athena_RUMS):")
                if search_term:
                    all_results = []
                    all_summary_rows = []
                    for index in indices:
                        pdf_url = all_pdf_urls[index]
                        results, summary_rows = extract_all_table_rows_from_url(pdf_url, search_term)
                        all_results.extend(results)
                        all_summary_rows.extend(summary_rows)
                    
                    display_results(all_results, all_summary_rows, search_term)

                    if st.button("Download as Excel"):
                        excel_buffer = convert_to_excel(all_summary_rows, all_results)
                        if excel_buffer:
                            st.download_button(label="Download Excel file", data=excel_buffer, file_name="extracted_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            except ValueError as e:
                st.error(f"Invalid indices input. Please enter a comma-separated list of numbers. Error: {e}")
            except IndexError as e:
                st.error(f"One or more indices are out of range. Error: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred. Error: {e}")

if __name__ == "__main__":
    main()
