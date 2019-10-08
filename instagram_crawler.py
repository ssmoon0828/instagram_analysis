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
def find_post(hashtag):
    url = 'https://www.instagram.com/explore/tags/' + hashtag + '/'
    driver.get(url)

find_post('맛집스타그램')