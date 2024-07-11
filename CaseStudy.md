# Case Study: WRPC Data Extractor

## Introduction

The WRPC Data Extractor was designed to streamline the extraction of data from Western Regional Power Committee's (WRPC) PDF reports. By allowing users to input specific years, select relevant PDFs, and search for keywords, the tool facilitates the generation of consolidated Excel reports for monthly Scheduled Revenue and Deviation Settlement Mechanism (DSM).

## Challenge

WRPC releases numerous PDF reports detailing monthly Scheduled Revenue and DSM. These reports contain vital information for stakeholders, but manually extracting and consolidating data from these PDFs is time-consuming and error-prone. The main challenges included:

- **Manual Effort**: Extracting data manually from multiple PDFs was labor-intensive.
- **Inconsistency**: The format and structure of the PDFs varied, making manual extraction prone to errors.
- **Data Consolidation**: Combining data from multiple PDFs into a single, coherent format required significant effort.
- **Accessibility**: There was a need for a user-friendly interface to simplify the data extraction process.

## Solution

To address these challenges, the WRPC Data Extractor was developed. Key features of the solution included:

- **Automated Data Extraction**: Using `pdfplumber`, the application automates the extraction of data from WRPC's PDF reports.
- **Interactive Interface**: A Streamlit-based web interface allows users to select specific years, choose PDFs, and input search terms effortlessly.
- **Excel Output**: The application generates consolidated Excel files for easy analysis, significantly reducing manual effort and increasing accuracy.
- **Real-time Data Processing**: Users can see and download results in real-time, enhancing the accessibility and usability of the data.

## Result

The WRPC Data Extractor effectively addressed the challenges faced by stakeholders in extracting and consolidating data from WRPC's PDF reports. Key outcomes included:

- **Increased Efficiency**: The automated extraction process significantly reduced the time and effort required to obtain data from multiple PDFs.
- **Improved Accuracy**: Automation minimized errors associated with manual data extraction and consolidation.
- **Enhanced Accessibility**: The user-friendly interface enabled stakeholders to easily access and analyze data, leading to better decision-making.
- **Scalability**: The tool's ability to handle multiple years and numerous PDFs made it adaptable for future data extraction needs.

## Conclusion

The WRPC Data Extractor developed during the internship at Havish M Consulting exemplifies the power of automation and user-centric design in addressing complex data extraction challenges. By leveraging Streamlit, pdfplumber, and other Python libraries, the tool provided an efficient, accurate, and accessible solution for stakeholders, transforming the way data from WRPC's PDF reports is managed and utilized. 

---
