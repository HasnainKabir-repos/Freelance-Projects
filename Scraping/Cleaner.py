import re
import pandas as pd
import csv
with open ('Accountants.txt', 'r') as f:
    contents = f.read()

data = re.sub(r'(<p class="adr">)|(</p>)', '', contents)

with open('Accountants.txt', 'w') as f:
    f.write(data)

with open('accounting_draft.csv', 'r') as reader, open('accounting_companies.csv','w') as writer:
    for row in reader:
        writer.write(row.replace('<p class="adr">',''))
        writer.write(row.replace('</p>', ''))