## WRPC Data Extractor

This project was developed during my internship at Havish M Consulting. The Streamlit web application allows users to extract meaningful data from WRPC's PDF reports for monthly Scheduled Revenue and Deviation Settlement Mechanism (DSM). Users can enter a year, select PDFs, and search for specific keywords to generate consolidated Excel reports.

This is the source website for data extraction: [https://wrpc.gov.in/](https://wrpc.gov.in/)

## Features

- **Data Extraction**: Extracts data from WRPC's PDF reports based on user-provided year and search terms.
- **Excel Output**: Generates Excel files containing summarized data for easy analysis.
- **Interactive Interface**: User-friendly interface powered by Streamlit, making it easy to select options and download results.

## Deployment

The application is deployed and accessible online at [WRPC Data Extractor](https://wrpc-hmc.streamlit.app/).

## How to Use

1. **Choose Data Type**: Select between "Monthly Scheduled Revenue" and "Deviation Settlement Mechanism (DSM)".
2. **Enter Year**: Input the desired year(s) for which data extraction is required.
3. **Select PDFs**: Choose specific PDFs from the list provided.
4. **Search Term**: Enter keywords to search within the selected PDFs.
5. **Generate Excel**: Click on the "Download Excel" button to obtain the consolidated data in Excel format.

## Function Explanations

### `fetch_pdfs_for_year(year)`

Fetches PDF URLs for a given year.

- **Inputs**: `year` (e.g., '2023')
- **Outputs**: List of PDF URLs and names
- **Process**: Retrieves and parses a data file to extract and construct the URLs and names of the weekly summary PDFs for the specified year.

### `extract_all_table_rows_from_url(pdf_url, pdf_name, search_term)`

Extracts data from a PDF based on a search term.

- **Inputs**: `pdf_url` (URL of the PDF), `pdf_name` (name for the PDF), `search_term` (keyword to search)
- **Outputs**: Lists containing rows of data: `all_rows` and `summary_rows`
- **Process**: Downloads the PDF, reads its content, searches for the term, and captures relevant rows in two categories: summary rows and daywise summary rows.

### `display_results(results, summary_rows, search_term)`

Displays the extracted data on the Streamlit app.

- **Inputs**: `results` (daywise data rows), `summary_rows` (summary data rows), `search_term` (keyword used for search)
- **Outputs**: None (Displays data in Streamlit UI)
- **Process**: Shows success message, displays dataframes for summary and daywise rows, sorts daywise data by date, and provides an info message with the total results count.

### `convert_to_excel(summary_rows, daywise_rows)`

Converts extracted data to an Excel file.

- **Inputs**: `summary_rows` (summary data rows), `daywise_rows` (daywise data rows)
- **Outputs**: An Excel file in memory (`BytesIO` buffer)
- **Process**: Creates two dataframes from the input rows, writes them to separate sheets in an Excel file, and returns the file as a buffer.

## Screenshots

![1720605310750](image/Readme/1720605310750.png)
*Screenshot of the interface showing data extraction options.*

![1720605344287](image/Readme/1720605344287.png)
*Screenshot of the Excel output generated.*

## Dependencies

- Streamlit
- Requests
- pdfplumber
- Pandas

## Installation

To run this application locally:

1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the application with `streamlit run home.py`.
