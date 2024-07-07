import requests
import xml.etree.ElementTree as ET

# Get the year range from the user
year_range = input("Enter the year range (e.g., 2022-23): ")

# Fetch the XML data from the URL
url = "https://www.srpc.kar.nic.in/html/xml-search/data/commercial.xml"
response = requests.get(url, verify=False)
xml_data = response.content

# Parse the XML data
root = ET.fromstring(xml_data)

# Iterate over each document and print the required information
for document in root.findall('document'):
    type_elem = document.find('type')
    url1 = document.find('url1')
    url1_desc = document.find('url1_desc')
    period = document.find('period')
    
    if type_elem is not None and type_elem.text == f'REA / RTA / RTDA ({year_range})' and url1 is not None:
        print(f"Period: {period.text}")
        print(f"URL1: {url1.text}")
        print(f"URL1 Description: {url1_desc.text}")
        print("------")
