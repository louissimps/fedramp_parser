
import json, csv, io, codecs, docx, re
FILE_NAME = './csv/fedramp_1.csv'



def get_impact_levels(id, sections):
    return []

def get_sections(id, sections):
    paragraphs = []
    pattern = "^"+str(id)+"[^\s]+"
    for para in sections:
        search_results = re.search(pattern, para.text)
        if search_results is None:
            continue
        else: 
            paragraphs.append(para.text)
    return paragraphs
        


def get_control_enhancements(id, sections):
    enhancements_pattern = "^[A-Z]{2}\-[0-9]+\s[^\(]+(\([A-Z]{1}\)\s{1})+\sCONTROL ENHANCEMENT"
    enhancements = []
    c = id
    for para in sections:
        search_results = re.findall(enhancements_pattern, para)
        if search_results is None:
            continue
        else: 
            enhancements = search_results

    return enhancements
        

def find_id(l, id):
     return l[index(l, lambda item: item["ID"] == id)]


#f = open( FILE_NAME, 'rb')
title = "FEDRamp Controls"
control_sections = {"controls": []}
controls = []
current_section = ""

doc = docx.Document('fedramp.docx')

print("Converting CSV data to JSON structure")
with io.open(FILE_NAME, encoding='utf-8') as f:
    reader = csv.DictReader( f, fieldnames = ("ID","Control Description","Low","Moderate","High"))
    for row in reader:
        for s in row:
            row[s] = row[s][2:-1]
        #If row ID doesn't match control we need to add section
        if row["Low"] == row["Control Description"]:
            continue
        elif row["ID"] == "ID" or row["ID"] == "Sensitivity Level":
            continue
        else:
            paragraphs = get_sections(row["ID"], doc.paragraphs)

            control = {"ID":row["ID"],
            "Title": row["Control Description"],
            "ControlText": row["Control Description"],
            "ImpactLevels": get_impact_levels(row["ID"], paragraphs),
            "Enhancements": get_control_enhancements(row["ID"], paragraphs),
            "Paragraphs": paragraphs
            }
            

            control_sections['controls'].append(control)


print ("Parsing Control Enhancements")


print("Writing JSON Data to fedramp_controls.json")
#    print (json.dumps (control_sections))
with open('fedramp_controls.json', 'wb') as f:
    json.dump(control_sections, codecs.getwriter('utf-8')(f), ensure_ascii=False)

    
