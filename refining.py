#%% import module

# basic module
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# refining module
import os
import glob
import re

#%% 데이터 병합 후 중복 행 제거
os.chdir('C:/Users/a/Desktop/project/instagram_analysis/data') # 파일이 있는 폴더로 디렉토리 변경
csv_file_name_list = glob.glob('*.csv') # csv 파일 추출

csv_file_list = []

for csv_file_name in csv_file_name_list:
    csv_file_list.append(pd.read_csv(csv_file_name))

df_raw = pd.concat(csv_file_list) # 맛집 원본 데이터프레임 생성

df = df_raw.drop_duplicates(['url']) # url 기준 중복행 제거

df = df.sort_values('date') # 시간순 정렬

df = df.reset_index() 
df = df.iloc[:, 1:] # 인덱스 정렬 

#%% 맛집 키워드로 지역명 or 음식 이름 추출
a = df['hashtag_list'][200]

def get_region_or_food_name(string):
    matjib_compile = re.compile('[가-힣]*맛집')
    matjib_list = matjib_compile.findall(string)
    
    name_list = []
    
    for matjib in matjib_list:
        
        if len(matjib) > 2:
            name_list.append(matjib[:-2])
    
    name_string = str(name_list).replace("'", "").replace('[', '').replace(']', '')
    
    return name_string

b = get_region_or_food_name(a)

def double(x):
    return 2 * x

my_list = pd.Series([1, 2, 3])
a = list(map(double, my_list))
