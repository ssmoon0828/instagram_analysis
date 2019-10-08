#%% import module

# basic module
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

# crawling module
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver

#%% crawling

# 
# set driver
driver = webdriver.Chrome('C:/Users/a/Desktop/chromedriver.exe')
driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')

# login
def instagram_login():
    '''
    ID랑 PW를 입력받아 인스타그램에 로그인 할 수 있게 해준다.
    '''
    ID = input('ID : ')
    PW = input('PW : ')
    driver.find_element_by_name('username').send_keys(ID)
    driver.find_element_by_name('password').send_keys(PW)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]').click()
    try:
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click()
    except:
        None

time.sleep(1)
instagram_login()

# find post about hashtag
def find_posts(hashtag):
    '''
    해시태그를 문자열로 입력받아 해시태그에 대응하는 게시물을 보여준다.
    '''
    url = 'https://www.instagram.com/explore/tags/' + hashtag + '/'
    driver.get(url)

find_posts('맛집스타그램')

num_post = driver.find_element_by_class_name('g47SY').text

post_list = driver.find_elements_by_class_name('_9AhH0')
post_list = driver.find_elements_by_tag_name('a')

# 게시물 클릭 후 뒤로가기
for i in range(len(post_list)):
    post_list[i].click()
    time.sleep(1)
    driver.back()

# 스크롤 내리기
for i in range(1):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")





def get_loc():
    '''
    게시물에 입력된 주소를 반환한다.
    주소가 입력되어있지 않을 때는 None값을 반환한다.
    '''       
    loc_class = driver.find_element_by_class_name('JF9hh')
    try:
        loc_name = loc_class.find_element_by_tag_name('a')
        print(loc_name.text)
    except:
        print('None')

get_loc()

def get_comments():
    '''
    게시물에 달린 댓글들을 뽑아낸다.
    답글달기로 숨겨진 댓글들도 뽑아내야한다(미완)
    '''
    doc_class = driver.find_elements_by_class_name('C4VMK')
    for i in range(len(doc_class)):
        doc_write = doc_class[i].find_element_by_tag_name('span')
        print(doc_write.text)

get_comments()
