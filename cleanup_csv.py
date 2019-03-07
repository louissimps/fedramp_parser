
import json, csv, io, codecs, os, docx, re
csv_dir = './csv'
files = [
    {'filename': 'FSCB_High.csv', 'Impact': 'High'},
    {'filename': 'FSCB_Moderate.csv', 'Impact': 'Moderate'},
    {'filename': 'FSCB_Low.csv', 'Impact': 'Low'}
    ]


def find_enhancement_by_control_id(id):
    for control in controls['Controls']:
        for e in controls['Controls'][control]["Enhancements"]:
            if(e['ID'] == id):
                return e
    

def find_control_by_id(id):
    for control in controls['Controls']:
        if control == id:
            return control

def extract_related_controls(input_text):
    matches = []
    if("related control" in input_text.lower()):

        m = re.search("related control[s]?:([^\.]+)\.", input_text.lower())
        if(m):
            raw = m.groups(0)[0].replace(" ", "")
            matches = raw.split(",")
    
    return matches 

controls = {'Controls': {}}
idx = 0
for file in files:
    with io.open(csv_dir + "/" + file['filename'], encoding='utf-8') as f:
        reader = csv.DictReader( f, fieldnames = ('Count','SORT ID','Family','ID','Control Name','Control Description','Parameters','Further Guidance','FedRAMP Parameter','','',''))
        

        for row in reader:
            foo = []


            is_enhancement = False
            #Id we are on top row skip to next
            if row['ID'] == 'ID':
                continue

            # If there is a parantheses in the title it is an enhancement
            if '(' in row['ID']:
                foo = row['ID'].split(" ")
                is_enhancement = True
                tc = find_control_by_id(foo[0])
            else:
                tc = find_control_by_id(row['ID'])
            #Set up a blank object
            control = {}
            
            te = find_enhancement_by_control_id(row['ID'])
            
            #If there is an enancement we need to get the parent control
            if is_enhancement:
                if te:
                    te['Impacts'].append(file['Impact'])
                else: 
                    enhancement = { 
                        "ID": row["ID"], 
                        "ControlText": row['Control Description'],
                        "Impacts": [file['Impact']],
                        "RelatedControls": extract_related_controls(row['Control Description']),
                        "FedrampGuidance": row['Further Guidance'].strip()
                        }
                    if controls['Controls'][tc]:
                        controls['Controls'][tc]["Enhancements"].append(enhancement)

                is_enhancement = False
            else: 
                if tc:
                    controls['Controls'][tc]['Impacts'].append(file['Impact'])
                else:
                    control = { 
                        "ID": row["ID"], 
                        "TITLE": row['Control Name'],
                        "Family": row["Family"],
                        "ControlText": row['Control Description'],
                        "Impacts": [file['Impact']],
                        "Enhancements": [],
                        "RelatedControls": extract_related_controls(row['Control Description']),
                        "FedrampGuidance": row['Further Guidance'].strip()
                        }
                    controls['Controls'][row["ID"]] = control

output_struct = {"Controls": []}
for control in controls['Controls']:
    output_struct['Controls'].append(controls['Controls'][control])    

with open('./output/fedramp_controls.json', 'wb') as f:
   json.dump(output_struct, codecs.getwriter('utf-8')(f), ensure_ascii=False)



#print(controls)
# with open('./output/fedramp_controls.json', 'wb') as f:
#    json.dump(controls, codecs.getwriter('utf-8')(f), ensure_ascii=False)

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


