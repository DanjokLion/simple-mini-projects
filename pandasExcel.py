import pandas as pd

def color_rows(row):
    color = 'green' if 'аналог' in row.values else 'white'
    return ['background-color: %s' % color] * len(row)

df_anal = pd.read_excel('test.xlsx', sheet_name='аналоги')
df_master = pd.read_excel('test.xlsx', sheet_name='МастерДата')

df_anal['SKU код'] = df_anal['SKU код'].astype(str)
df_master['SKU код'] = df_master['SKU код'].astype(str)

result = pd.merge(df_anal, df_master, on ='SKU код')
result = result.loc[:, ['№_x', 'SKU код', 'Статус SKU', 'Наименование ассортимента_x', 'аналог', 'Product id']]

found_rows = pd.DataFrame()

for index, row in result.iterrows():
    found_row = df_master[df_master['Product id'] == row['Product id']]

    if not found_row.empty:
        found_rows = pd.concat([found_rows, found_row])
    
found_rows = found_rows.reset_index(drop=True)
found_rows['№'] = found_rows.groupby('Product id').ngroup() + 1
found_rows['аналог'] = found_rows['SKU код'].apply(lambda x: x if x in result['SKU код'].values else 'аналог')
styled_df = found_rows.style.apply(color_rows, axis=1)

styled_df.to_excel('result.xlsx', engine='openpyxl')
