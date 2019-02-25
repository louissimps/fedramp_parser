
import json, csv, io, codecs, os, docx, re


doc = docx.Document("./fedramp.docx")


for para in doc.paragraphs:
    if "AC-" in para.text:
        print(re.search("^([^\s]+)", para.text))

#with open('fedramp.txt', 'wb') as f:
#    json.dump(text, codecs.getwriter('utf-8')(f), ensure_ascii=False)

# pathName = os.getcwd()
# file_list = []
# fileNames = os.listdir(pathName)
# for fileName in fileNames:
#     if fileName.endswith(".csv") and fileName.startswith("fedramp_"):
#         file_list.append(fileName)

# for f in file_list:
#     reader = csv.reader(f, delimiter=',')
#     for row in reader:
#         print (row)


