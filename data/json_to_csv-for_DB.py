import requests
import json
import csv
import pandas as pd

with open('유니온랭킹1페이지.json','r') as file:
    data = json.load(file)

df = pd.json_normalize(data['ranking'])

df.to_csv('ranking_page.csv', index = False, encoding = 'cp949')
