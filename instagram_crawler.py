#%% import module

# basic module
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

# crawling module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#%% def function

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

def find_posts(hashtag):
    '''
    해시태그를 문자열로 입력받아 해시태그에 대응하는 게시물을 보여준다.
    '''
    url = 'https://www.instagram.com/explore/tags/' + hashtag + '/'
    driver.get(url)

def get_urls(max_num_posts = 100000):
    '''
    해시태그에 대응하는 게시물들의 url 정보들을 가져와 list 형태로 반환한다.
    '''
    num_post = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/header/div[2]/div/div[2]/span/span').text
    num_post = int(num_post.replace(',', ''))
    
    if num_post <= max_num_posts:
        max_num_posts = num_post

    body = driver.find_element_by_tag_name("body")
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)  
    
    url_list = []
    
    while len(url_list) <= max_num_posts :
        
        for i in range(1, 9):
            post_line = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[' + str(i) + ']')
            a_tag_list = post_line.find_elements_by_tag_name('a')
            
            for i in range(3):
                url = a_tag_list[i].get_attribute('href')
                
                if len(url_list) < 51:
                    if url not in url_list:
                        url_list.append(url)
                    else:
                        pass
                else:
                    if url not in url_list[-50 :]:
                        url_list.append(url)
                    else:
                        pass
            
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    
    return url_list

def get_loc():
    '''
    게시물의 장소 정보를 반환한다.
    '''
    try:
        loc = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[2]/div[2]/a').text
        
        return loc
    except:
        
        return ''

def get_likes():
    '''
    게시물의 좋아요 수를 반환한다.
    '''
    try:
        likes = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/div/button/span').text
        
        return int(likes)
    except:
        
        return 0
    
def get_comments():
    '''
    게시물의 코멘트들을 반환한다.
    해시태그와 해시태그가 아닌 커멘트들을 분리할 필요가 있을까?
    분리할 필요가 있다면 span 태그가 아닌 원본을 뽑아 정제해야 할 듯
    '''
    comments_class = driver.find_elements_by_class_name('C4VMK')
    comments = ''
    for i in range(len(comments_class)):
        comment =  comments_class[i].find_element_by_tag_name('span').text
        comments += comment + ' ' 
    
    return comments

def make_df(url_list):
    '''
    url list를 받아 url에 대응하는 위치, 좋아요 수, 코멘트에 관한 정보를
    데이터프레임 형태로 만들어준다.
    '''
    
    loc_list = []
    likes_list = []
    comments_list = []
    
    for url in url_list:
        driver.get(url)
        
        # 위치 리스트 생성
        loc = get_loc()
        loc_list.append(loc)
        
        # 좋아요 수 리스트 생성
        likes = get_likes()
        likes_list.append(likes)
        
        # 코멘트 리스트 생성
        comments = get_comments()
        comments_list.append(comments)
    
    df = pd.DataFrame({'url' : url_list,
                       'loc' : loc_list,
                       'like' : likes_list,
                       'comments' : comments_list})
    
    return df

#%% crawling
    # url 변수 추가 필요(merge 시킬때 필요)

driver = webdriver.Chrome('C:/Users/ssmoo/Desktop/chromedriver.exe')
driver.implicitly_wait(5)
driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
time.sleep(1)
instagram_login()
time.sleep(2)
find_posts('맛집스타그램')
time.sleep(1)
url_list = get_urls(100)
start_time = time.time()
df = make_df(url_list)
end_time = time.time()
print('learning time : ', end_time - start_time)
# try except 구문을 써서 좋아요 수와 위치정보에서 결측값이 있는 오류를 해결했지만
# 속도가 너무 느려졌다...해결할 방법 없을까?

