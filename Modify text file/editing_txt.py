list_of_articles = []

with open('text.txt', 'r') as f:
    for line in f.readlines():
        list_of_articles.append(line)

new_lines = []
for lines in list_of_articles:
    new_line = lines.replace('.', '')
    new_lines.append(new_line)
with open('text.txt', 'r+') as file:
    file.truncate(0)
    for new in new_lines:
        file.write(new)


import pandas as pd

data = pd.read_table('text.txt', sep='\t', header=None)

data.columns = ['Serial No.', 'Topic']

data.set_index('Serial No.')
data.drop(columns=data.columns[0],
        axis=1,
        inplace=True)
data.to_excel('output.xlsx', sheet_name='Articles', index_label='Serial No.')
print(data)