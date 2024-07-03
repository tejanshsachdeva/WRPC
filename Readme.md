# DSM Data Extraction and Analysis

This project extracts and analyzes Daywise Summary and Summary Rows data from PDFs published by Western Regional Power Committee (WRPC) for a given year. The program searches for specific terms in the PDFs, extracts relevant data, and displays the results in a tabular format.

## Features

- **Fetch PDFs for a Given Year**: Automatically retrieves the URLs of PDFs for a specified year.
- **Search for Specific Terms**: Searches for user-specified terms within the PDF files.
- **Extract Data**: Extracts both daywise summary data and summary rows from the PDFs.
- **Display Results**: Displays the extracted data in a tabular format, including week number information based on the date.
- **User Interaction**: Allows users to specify the years and PDFs to be analyzed and the search terms.

## Usage

1. **Input Parameters**:

   - **Years**: Enter the years for which you want to fetch and analyze PDFs (e.g., `2023,2024`).
   - **PDF Indices**: Enter the indices of the PDFs to search (e.g., `0,1,2`).
   - **Search Term**: Enter the name or term to search for in the PDFs (e.g., `Athena_RUMS`).
3. **View Results**:

   - The program will display the extracted data in a tabular format, with week numbers included based on the dates.

## Code Overview

- **fetch_pdfs_for_year(year)**: Fetches the list of PDF URLs for the specified year from the WRPC website.
- **extract_all_table_rows_from_url(pdf_url, search_term)**: Extracts all relevant rows containing the search term from the given PDF URL.
- **extract_week_info(pdf_url)**: Extracts the week information from the PDF URL.
- **extract_week_from_date(date_str, year)**: Extracts the week number from a given date string.
- **display_results(results, summary_rows, search_term, year)**: Displays the extracted results in a tabular format, including week numbers.

## Example

Example input and output:

```sh
Enter the years (e.g., 2023,2024): 2023
List of PDFs for the year 2023:
0. https://www.wrpc.gov.in/htm/Jan2023/sum1.pdf
1. https://www.wrpc.gov.in/htm/Feb2023/sum2.pdf

Enter the indices of the PDFs to search (e.g., 0,1,2): 0,1
Enter the name to search for (e.g., Athena_RUMS): Athena_RUMS

Results found for 'Athena_RUMS':

Daywise Summary Rows:
+--------+-------------+-------------+------------+---------------+------------------+-----------+
| Date   | Entity      |   Injection |   Schedule |   DSM Payable |   DSM Receivable |   Net DMC |
+========+=============+=============+============+===============+==================+===========+
| 17-Jun | Athena_RUMS |     1.2519  |    1.45731 |     10.5101   |          2.01765 |   8.49247 |
+--------+-------------+-------------+------------+---------------+------------------+-----------+

Summary Rows:
+-------+--------------+----------+------------+--------------+------------------+--------------------+
| Week  | Name of Entity | Payable | Receivable | Net DSM (Rs.) | Payable/Receivable |                  |
+=======+==============+==========+============+==============+==================+====================+
| Week 24 Jun2023 | Athena_RUMS | 10.5101  | 2.01765  | 8.49247       |                  |
+-------+--------------+----------+------------+--------------+------------------+--------------------+

Total results found: 2
```

## Contributing

1. **Fork the Repository**.
2. **Create a Branch** (`git checkout -b feature/your-feature`).
3. **Commit Your Changes** (`git commit -m 'Add your feature'`).
4. **Push to the Branch** (`git push origin feature/your-feature`).
5. **Open a Pull Request**.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgements

- [pdfplumber](https://github.com/jsvine/pdfplumber) for PDF extraction.
- [tabulate](https://github.com/astanin/python-tabulate) for displaying tables.
