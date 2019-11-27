#%% import module

# basic module
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family = 'Gulim')

# extra module
import os
import glob
import re
import nltk
import wordcloud
from PIL import Image

#%% load data
os.chdir('C:/Users/ssmoo/Desktop/instagram_analysis/data/raw_data')
csv_name_list = glob.glob('*')
csv_file_list = []

for csv_name in csv_name_list:
    csv_file_list.append(pd.read_csv(csv_name))
    
insta_df = pd.concat(csv_file_list)
insta_df = insta_df.drop_duplicates() # 중복행 제거
insta_df = insta_df[insta_df['hashtag_list'].notnull()] # hashtag 결측치 제거
insta_df = insta_df.reset_index()
del insta_df['index']

#%% 지역명 찾기

# 카페로 끝나는 해시태그 찾는 함수 생성
def get_cafe(text):
    cafe_regex = '[0-9a-zA-Z가-힣]*카페'
    cafe_compile = re.compile(cafe_regex)
    cafe_list = cafe_compile.findall(text)
    
    return cafe_list

# 함수 적용
cafe_list = []

for i in range(len(insta_df)):
    tmp_list = get_cafe(insta_df.loc[i, 'hashtag_list'])
    cafe_list += tmp_list

# '카페' 단어 제거
cafe_list_copy = cafe_list
cafe_list = []

for i in range(len(cafe_list_copy)):
    
    if len(cafe_list_copy[i]) > 2:
        cafe_list.append(cafe_list_copy[i][:-2])

freqdist = nltk.FreqDist(cafe_list)
freqdist.most_common(10)

# 불용어 처리
stopword = open('C:/Users/ssmoo/Desktop/instagram_analysis/data/raw_data/불용어.txt',
                encoding = 'utf-8')
stopword_list = stopword.readlines()

for i in range(len(stopword_list)):
    stopword_list[i] = stopword_list[i].replace('\n', '')

dosi = open('C:/Users/ssmoo/Desktop/instagram_analysis/data/raw_data/도시.txt',
            encoding = 'utf-8')
dosi_list = dosi.readlines()

for i in range(len(dosi_list)):
    dosi_list[i] = dosi_list[i].replace('\n', '')

for i in range(len(dosi_list)):
    dosi_list[i] = dosi_list[i].replace('시', '')

stopword_list += dosi_list
for stopword in stopword_list:
    del freqdist[stopword]

#%% wordcloud

# 단순 빈도수 그래프
freqdist.plot(20)    

# 단순 워드클라우
wc = wordcloud.WordCloud(width = 1000,
                         height = 600,
                         background_color = 'white',
                         font_path = 'C:/Users/ssmoo/Downloads/SangSangFlowerRoad.otf',
                         max_words = 100)
plt.figure(figsize = (16, 12),
           dpi = 200)
plt.imshow(wc.generate_from_frequencies(freqdist))
plt.show()

# 커피잔으로 시각화

# 커피잔 이미지 불러오기 및 확인
coffee_mask = np.array(Image.open('C:/Users/ssmoo/Desktop/coffee_cup.jpg'))
plt.figure(figsize = (8, 8))
plt.imshow(coffee_mask, cmap = plt.cm.gray, interpolation = 'bilinear')

# 워드클라우드
wc = wordcloud.WordCloud(width = 1000,
                         height = 600,
                         background_color = 'white',
                         font_path = 'C:/Users/ssmoo/Downloads/SangSangFlowerRoad.otf',
                         max_words = 100,
                         mask = coffee_mask)
plt.figure(figsize = (16, 12),
           dpi = 200)
plt.imshow(wc.generate_from_frequencies(freqdist))
plt.axis('off')
plt.show()
