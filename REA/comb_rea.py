import streamlit as st
import requests
import pdfplumber
from io import BytesIO
from datetime import datetime
import pandas as pd
import PyPDF2
import re

def fetch_pdfs_for_year(year):
    year_data_url = f'https://www.wrpc.gov.in/assets/data/REA_{year}.txt'
    year_data_response = requests.get(year_data_url)
    
    if year_data_response.status_code == 200:
        pdf_data_lines = year_data_response.text.strip().split('\n')
        pdf_urls = []
        pdf_names = []
        for line in pdf_data_lines:
            if line.strip().startswith('//') or not line.strip():
                continue
            pdf_details = line.split(',')
            
            if len(pdf_details) >= 3:
                pdf_name = pdf_details[0].strip()
                issue_date = pdf_details[1].strip()
                pdf_path = pdf_details[2].strip()
                
                if pdf_path.startswith('/'):
                    pdf_path = pdf_path[1:]
                
                full_pdf_url = f'https://www.wrpc.gov.in/{pdf_path}'
                pdf_full_name = f"{pdf_name} (Issued on {issue_date})"
                pdf_urls.append(full_pdf_url)
                pdf_names.append(pdf_full_name)
            else:
                st.warning(f"Invalid line format: {line}")
        
        return pdf_urls, pdf_names
    else:
        st.error(f"Failed to fetch data for year {year}")
        return [], []

def extract_first_instance(pdf_path, search_term):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text = page.extract_text()
            lines = text.split('\n')
            for line in lines:
                if search_term in line:
                    match = re.search(rf'{search_term}\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', line)
                    if match:
                        return f"{search_term} {match.group(1)} {match.group(2)} {match.group(3)}"
    return None

def extract_all_table_rows_from_url(pdf_url, search_term):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_file = BytesIO(response.content)
        with pdfplumber.open(pdf_file) as pdf:
            summary_rows = []
            found_first_instance = False
            pdf_filename = pdf_url.split('/')[-1].replace('.pdf', '')
            for page in pdf.pages:
                text = page.extract_text()
                if search_term in text and not found_first_instance:
                    lines = text.split('\n')
                    for line in lines:
                        if search_term in line:
                            match = re.search(rf'{search_term}\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', line)
                            if match:
                                summary_rows.append((pdf_filename, search_term, match.group(1), match.group(2), match.group(3)))
                                found_first_instance = True
                                break
            return summary_rows
    else:
        st.error(f"Failed to fetch the PDF from URL: {pdf_url}")
        return []

def display_results(summary_rows, search_term):
    if summary_rows:
        st.success(f"\nResults found for '{search_term}':")
        st.subheader("First Instance Rows:")
        headers = ["PDF Name", "RE Generator", "Schedule (MU)", "Actual (MU)", "Deviation (MU)"]
        summary_df = pd.DataFrame(summary_rows, columns=headers)
        st.dataframe(summary_df)
    else:
        st.warning(f"No results found for '{search_term}'.")

    st.info(f"Total results found: {len(summary_rows)}")

def convert_to_excel(summary_rows):
    headers = ["PDF Name", "RE Generator", "Schedule (MU)", "Actual (MU)", "Deviation (MU)"]
    summary_df = pd.DataFrame(summary_rows, columns=headers)

    buffer = BytesIO()
    try:
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            summary_df.to_excel(writer, sheet_name="Summary Rows", index=False)
        buffer.seek(0)
        return buffer
    except Exception as e:
        st.error(f"An error occurred while creating the Excel file: {e}")
        return None

def main():
    # Streamlit App
    st.title("Scheduled Revenue Energy (SRE) Data Extractor")

    if st.button("Back to Home"):
        st.session_state.app_choice = None
        st.rerun()

    all_pdf_urls = []
    all_pdf_names = []

    years_input = st.text_input("Enter the years (e.g., 2022,2023):")
    if years_input:
        years = years_input.split(',')
        index_offset = 0

        for year in years:
            year = year.strip()
            pdf_urls, pdf_names = fetch_pdfs_for_year(year)
            if pdf_urls:
                with st.expander(f"List of PDFs for the year {year}: "):
                    for idx, (url, name) in enumerate(zip(pdf_urls, pdf_names)):
                        st.write(f"{index_offset + idx}. {name} ({url})")
                index_offset += len(pdf_urls)
                all_pdf_urls.extend(pdf_urls)
                all_pdf_names.extend(pdf_names)

    if all_pdf_urls:
        indices_input = st.text_input("Enter the indices of the PDFs to search (e.g., 0,1,2):")
        if indices_input:
            try:
                indices = list(map(int, indices_input.split(',')))
                search_term = st.text_input("Enter the name to search for (e.g., Arinsun_RUMS):")
                if search_term:
                    all_summary_rows = []
                    for index in indices:
                        pdf_url = all_pdf_urls[index]
                        summary_rows = extract_all_table_rows_from_url(pdf_url, search_term)
                        all_summary_rows.extend(summary_rows)
                    
                    display_results(all_summary_rows, search_term)

                    if st.button("Download as Excel"):
                        excel_buffer = convert_to_excel(all_summary_rows)
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