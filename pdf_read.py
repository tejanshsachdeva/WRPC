import PyPDF2
import re

def extract_arinsun_data(pdf_path, table_header, search_term):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        in_target_table = False
        for page in pdf_reader.pages:
            text = page.extract_text()
            lines = text.split('\n')
            for line in lines:
                if table_header.strip() == line.strip():  # Check for exact match
                    in_target_table = True
                    continue
                if in_target_table and search_term in line:
                    match = re.search(rf'{search_term}\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)', line)
                    if match:
                        return f"{search_term} {match.group(1)} {match.group(2)} {match.group(3)}"
                if in_target_table and line.strip() == '':
                    in_target_table = False
    return None

pdf_path = r"C:\Users\tejan\Downloads\reajan24.pdf"
table_header = "RE Generator Schedule (MU) Actual (MU) Deviation (MU)"
search_term = "Arinsun_RUMS"
arinsun_data = extract_arinsun_data(pdf_path, table_header, search_term)

# Print the result to the console
if arinsun_data:
    print(arinsun_data)
else:
    print("Data not found")
