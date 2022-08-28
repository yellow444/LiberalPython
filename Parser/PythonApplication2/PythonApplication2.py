import pandas as pd
import docx
import os
import re

# Сюда сохранить все файлы
entries = os.scandir('doc2/')

columns = list([i for i in range(1,200)])
data = dict((k, []) for k in columns)
def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)
countFile = 0
for entry in entries:
    # Debug
    #if entry.name != '208_ot_18_fevralya_2022.docx' and entry.name != '804_ot_30_aprelya_2022.docx':
    #    continue
    countFile += 1

    #print(str(countFile) + ':' + entry.name)

    raw_text = getText(entry)

    # get text outside tags
    #convert_text = re.split('(?<=\{11\}).*(?=\{11\})',raw_text)
    #convert_text = [string.upper() for string in convert_text]

    # get text inside tags with tags
    dateJoin = pd.DataFrame() # initialize empty df
    for i in columns:
        if i != 199:
            remaining_parts = re.findall('(?<=\{' + i.__str__() + '\}).*(?=\{' + i.__str__() + '\})', raw_text)
        else:
            remaining_parts = [entry.name]
        if remaining_parts is None or len(remaining_parts) == 0:
            continue      
        data[i] += (remaining_parts)

df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in data.items() ]))
df.replace('|','\\')
df.to_csv('result2.csv', encoding='utf-8', index=False, sep='|')

