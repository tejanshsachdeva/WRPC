import streamlit as st
import requests
import pdfplumber
from io import BytesIO
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

def extract_all_table_rows_from_url(pdf_url, pdf_name, search_term):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_file = BytesIO(response.content)
        with pdfplumber.open(pdf_file) as pdf:
            summary_rows = []
            found_first_instance = False
            for page in pdf.pages:
                text = page.extract_text()
                if search_term in text and not found_first_instance:
                    lines = text.split('\n')
                    for line in lines:
                        if search_term in line:
                            match = re.search(rf'{search_term}\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', line)
                            if match:
                                summary_rows.append((pdf_name, search_term, match.group(1), match.group(2), match.group(3)))
                                found_first_instance = True
                                break
            return [pdf_name], summary_rows
    else:
        st.error(f"Failed to fetch the PDF from URL: {pdf_url}")
        return [], []

def display_results(all_results, all_summary_rows, search_term):
    if all_summary_rows:
        st.success(f"\nResults found for '{search_term}':")
        st.subheader("Summary Rows:")
        headers = ["PDF Name", "RE Generator", "Schedule (MU)", "Actual (MU)", "Deviation (MU)"]
        summary_df = pd.DataFrame(all_summary_rows, columns=headers)
        st.dataframe(summary_df)
    else:
        st.warning(f"No results found for '{search_term}' in the selected PDFs.")

def convert_to_excel(all_summary_rows, all_results):
    headers = ["PDF Name", "RE Generator", "Schedule (MU)", "Actual (MU)", "Deviation (MU)"]
    summary_df = pd.DataFrame(all_summary_rows, columns=headers)

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

    years_input = st.text_input("Enter the years (e.g., 2023,2024):")
    if years_input:
        years = years_input.split(",")
        for year in years:
            year = year.strip()
            if year.isdigit():
                pdf_urls, pdf_names = fetch_pdfs_for_year(year)
                all_pdf_urls.extend(pdf_urls)
                all_pdf_names.extend(pdf_names)

    selected_pdfs = st.multiselect("Choose PDFs to search for the keyword:", all_pdf_urls, format_func=lambda x: all_pdf_names[all_pdf_urls.index(x)] if x in all_pdf_urls else x)

    search_term = st.text_input("Enter the keyword to search:")
    if search_term and selected_pdfs:
        all_results = []
        all_summary_rows = []
        for pdf_url in selected_pdfs:
            pdf_name = all_pdf_names[all_pdf_urls.index(pdf_url)]
            results, summary_rows = extract_all_table_rows_from_url(pdf_url, pdf_name, search_term)
            all_results.extend(results)
            all_summary_rows.extend(summary_rows)

        if all_results or all_summary_rows:
            display_results(all_results, all_summary_rows, search_term)
            st.info(f"Total PDFs processed: {len(selected_pdfs)}")

            buffer = convert_to_excel(all_summary_rows, all_results)
            if buffer:
                st.download_button(
                    label="Download Excel",
                    data=buffer,
                    file_name="dsm_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.warning(f"No results found for '{search_term}' in the selected PDFs.")

if __name__ == "__main__":
    main()
