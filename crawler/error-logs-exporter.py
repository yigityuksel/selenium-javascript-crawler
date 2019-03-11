import os
import json
import pandas as pd
from pprint import pprint
from pandas import ExcelWriter
from pandas.io.json import json_normalize

dir_path = os.path.dirname(os.path.realpath(__file__))


with open(os.path.join(dir_path,"har","SEVERE_JAVASCRIPT - 201903081745.json")) as f:
    data = json.load(f)

df = pd.DataFrame.from_dict(json_normalize(data), orient='columns')
df = df.drop('Error', 1)
df = df.drop('Source', 1)

writer = pd.ExcelWriter('results.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()