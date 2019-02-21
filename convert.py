
import json, csv, io, codecs
FILE_NAME = 'fedramp_1.csv'

#f = open( FILE_NAME, 'rb')
title = "FEDRamp Controls"
control_sections = {title: {}}
controls = []
current_section = ""

print("Converting CSV data to JSON structure")
with io.open(FILE_NAME, encoding='utf-8') as f:
    reader = csv.DictReader( f, fieldnames = ("ID","Control Description","Low","Moderate","High"))
    for row in reader:
        frame = {}
        for s in row:
            row[s] = row[s][2:-1]
        #If row ID doesn't match control we need to add section
        if row["Low"] == row["Control Description"]:
            
            current_section = row["ID"]
            section = { "ID":row["ID"],
            "Description": row["Control Description"],
            "controls":[]
            }
            control_sections[title][current_section] = section

        else:
            control = {"ID":row["ID"],
            "Description": row["Control Description"],
            "Low": row["Low"],
            "Moderate": row["Moderate"],
            "High": row["High"] 
            }
            if(current_section in control_sections[title].keys()):
                control_sections[title][current_section]["controls"].append(control)


print("Writing JSON Data to fedramp_controls.json")
#    print (json.dumps (control_sections))
with open('fedramp_controls.json', 'wb') as f:
    json.dump(control_sections, codecs.getwriter('utf-8')(f), ensure_ascii=False)

    
