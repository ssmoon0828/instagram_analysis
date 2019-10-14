#%% import module

# basic module
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import re

# crawling module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#%% def function

def instagram_login(ID, PW):
    '''
    ID랑 PW를 입력받아 인스타그램에 로그인 할 수 있게 해준다.
    '''
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
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
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
        body.send_keys(Keys.PAGE_UP)
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    
    return url_list

def get_date():
    time_tag = driver.find_element_by_tag_name('time')
    date = time_tag.get_attribute('datetime')[:10]
    
    return date

def get_loc():
    '''
    게시물의 장소 정보를 반환한다.
    '''
    loc_list = driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div/article/header/div[2]/div[2]/div[2]/a').text
    
    if len(loc_list) == 0:
        
        return ''
    else:
        
        return

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
    '''
    replies = driver.find_elements_by_class_name('EizgU')
    
    if len(replies) == 0:
        comments_class = driver.find_elements_by_class_name('C4VMK')
        comments = ''

        for i in range(len(comments_class)):
            comment =  comments_class[i].find_element_by_tag_name('span').text
            comments += comment + ' ' 
        
        return comments
    else:
        for i in range(len(replies)):
            replies[i].click()

        comments_class = driver.find_elements_by_class_name('C4VMK')
        comments = ''

        for i in range(len(comments_class)):
            comment =  comments_class[i].find_element_by_tag_name('span').text
            comments += comment + ' ' 
        
        return comments


def get_hashtag(text):
    '''
    게시물에서 반환받은 코멘트로부터 해시태그들을 추출하여 리스트로 반환한다.
    '''
    hashtag_regex = "#([0-9a-zA-Z가-힣]*)"
    hashtag_compile = re.compile(hashtag_regex)
    hashtag_list = hashtag_compile.findall(text)
    
    return hashtag_list
    
def make_df(url_list):
    '''
    url list를 받아 url에 대응하는 위치, 좋아요 수, 코멘트에 관한 정보를
    데이터프레임 형태로 만들어준다.
    '''
    
    refined_url_list = []
    date_list = []
    # loc_list = []
    # likes_list = []
    comments_list = []
    hashtag_list_list = []
    
    for url in url_list:
        
        try:
            driver.get(url)
            
            # 날짜 리스트 생성
            date = get_date()
            date_list.append(date)
            
            # 위치 리스트 생성 (시간이 오래걸려 뺌)
            # loc = get_loc()
            # loc_list.append(loc)
            
            # 좋아요 수 리스트 생성 (시간이 오래걸릴 뿐더러 분석에 불필요하다고 판단하여 뺌)
            # likes = get_likes()
            # likes_list.append(likes)
            
            # 코멘트 리스트 생성
            comments = get_comments()
            comments_list.append(comments)
            
            # 해시태그 리스트 생성
            hashtag_list = get_hashtag(comments)
            hashtag_list = str(hashtag_list).replace("'", '').replace('[', '').replace(']', '')
            hashtag_list_list.append(hashtag_list)
            
            # 삭제되지 않은 게시물의 url 리스트 생성
            refined_url_list.append(url)
        
        except:
            pass
        
    df = pd.DataFrame({'url' : refined_url_list,
                       'date' : pd.to_datetime(date_list),
                       # 'loc' : loc_list,
                       # 'likes' : likes_list,
                       'comments' : comments_list,
                       'hashtag_list' : hashtag_list_list})
    
    return df


 
#%% crawling

# set parameter
chrome_driver_path = 'C:/Users/a/Desktop/chromedriver.exe' # 크롬 드라이버 위치
#hashtag_list = ['먹스타그램', '맛스타그램', '맛집', '먹스타', '맛있다그램', '먹부림', '푸드스타그램'] # 추출하고 싶은 게시물안에 속한 해시태그 리스트
hashtag_list = ['맛집스타그램'] # 추출하고 싶은 게시물안에 속한 해시태그 리스트
ID = 'ssmoooooon' # ID
PW = '**********' # PW (github에 올릴때 반드시 가리고 올릴것!!)
num_post = 100 # 추출하고 싶은 게시물의 수

# crawling start!

for hashtag in hashtag_list:

    # 드라이버 생성
    driver = webdriver.Chrome(chrome_driver_path)
    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    driver.implicitly_wait(1)
    time.sleep(3)
    
    # 로그인
    instagram_login(ID, PW)
    time.sleep(3)
    
    # 해시태그 검색
    find_posts(hashtag)
    time.sleep(3)
    
    start_url_search_time = time.time()
    url_list = get_urls(num_post)
    end_url_search_time = time.time()
    
    start_make_df_time = time.time()
    df = make_df(url_list)
    end_make_df_time = time.time()
    
    print('[' + hashtag + ']')
    print('url search time : ', end_url_search_time - start_url_search_time)
    print('make df time : ', end_make_df_time - start_make_df_time)
    print()
    
    df.to_csv(hashtag + '.csv', index = False)
    driver.close()