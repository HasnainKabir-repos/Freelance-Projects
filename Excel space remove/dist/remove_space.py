import pandas as pd

filename = '2022 RBC Visa Excel -Working Copy.xlsx'
df = pd.read_excel(filename)
df[df.columns[0]] = df[df.columns[0]].str.strip()
with pd.ExcelWriter('output.xlsx') as writer:
    df.to_excel(writer, index=False, startrow=1, header=False)