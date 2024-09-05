import requests
import json
import csv
import pandas as pd

# 예시를 들기 위해 1페이지의 json파일을 가져왔지만 API_KEY를 활용하여 원하는 정보를 모두 불러와 사용 가능
with open('유니온랭킹1페이지.json','r') as file:
    data = json.load(file)

df = pd.json_normalize(data['ranking'])

df.to_csv('ranking_page.csv', index = False, encoding = 'cp949')
