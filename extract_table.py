
from docx2csv import extract_tables, extract
import requests

url = 'https://www.fedramp.gov/assets/resources/templates/FedRAMP-SSP-High-Baseline-Template.docx'

print("Retrieving Current FEDRamp guidlines from https://www.fedramp.gov/assets/resources/templates/FedRAMP-SSP-High-Baseline-Template.docx")
r = requests.get(url, allow_redirects=True)
print("Write to local copy fedramp.docx")
open('fedramp.docx', 'wb').write(r.content)

print("Extracting tables with more than 20 rows from docx into csv")
extract(filename='fedramp.docx', format="csv", sizefilter=20)