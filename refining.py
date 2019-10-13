#%% import module

# basic module
import numpy as np
import pandas as pd
import  matplotlib.pyplot as plt

# refining module
import re

#%%
matjib = pd.read_csv('C:/Users/ssmoo/맛집스타그램.csv')
a = matjib['hashtag_list'][11]

hashtag_compile = re.compile('[가-힣]*맛집')
hashtag_compile.findall(a)
matjib['matjib'] = hashtag_compile.findall(matjib['hashtag_list'])
