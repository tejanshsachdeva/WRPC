import pdfplumber
from tabulate import tabulate

# Path to the PDF file
file_path = "C:/Users/tejan/Downloads/sum2.pdf"

# Get user input for the search term
search_term = input("Enter the name to search for (e.g., Athena_RUMS): ")

# Function to search for the term and extract all relevant table rows
def extract_all_table_rows(file_path, search_term):
    with pdfplumber.open(file_path) as pdf:
        all_rows = []
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
                            all_rows.append((headers1, line.split()))
                            print(f"Added row with header: {headers1}")
                        elif "Daywise Summary" in line:
                            headers2 = line
                            daywise_data = [row.split() for row in lines[i + 2:i + 9] if row.strip()]  # Adjust indices to skip headers and get data rows
                            all_rows.append((headers2, daywise_data))
                            print(f"Added daywise summary with header: {headers2}")
                            break  # Stop processing after adding daywise summary
                        elif not any(header in line for header in ["Daywise Summary", "Date Entity", "Total"]):
                            # Capture any other lines containing the search term
                            all_rows.append(("Summary Row", line.split()))
                            print(f"Added summary row: {line}")
        return all_rows

# Extract all relevant table rows
results = extract_all_table_rows(file_path, search_term)

# Print the results in tabular format
if results:
    print(f"\nResults found for '{search_term}':")

    # Separate summary rows and daywise summary rows
    summary_rows = [(headers, row) for headers, row in results if headers == "Summary Row" or "Sr." in headers]
    daywise_rows = [(headers, row) for headers, row in results if headers.startswith("Daywise Summary")]

    if summary_rows:
        print("\nSummary Rows:")
        headers1 = "Sr. || Name of Entity || Payable || Receivable || Net DSM (Rs.) || Payable/Receivable"
        for headers, row in summary_rows:
            print(tabulate([row], headers=headers1.split(" || "), tablefmt="grid"))
            print("\n")

    # Print Daywise Summary Rows
    if daywise_rows:
        print("\nDaywise Summary Rows:")
        headers2 = "Date || Entity || Injection || Schedule || DSM Payable || DSM Receivable || Net DMC"
        for headers, rows in daywise_rows:
            print(tabulate(rows, headers=headers2.split(" || "), tablefmt="grid"))
            print("\n")
else:
    print(f"No results found for '{search_term}'.")

# Print the number of results
print(f"Total results found: {len(results)}")