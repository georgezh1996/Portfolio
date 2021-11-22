# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 09:42:08 2021

@author: georgez
"""


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import requests 
import re
import time
import unidecode




url='https://www.forbes.com/forbes-400/'

rawTable=[]
ids=[]
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.maximize_window()
#find details on list website and ids for profiles 

profileStub='https://www.forbes.com/profile/'
driver.get(url)

while True:
    htmlResults=driver.find_elements(By.CLASS_NAME,'table__row')
    for i in range(len(htmlResults)):
        rawTable.append(htmlResults[i].text)
        ids.append(htmlResults[i].get_attribute('id'))
    try:
        driver.find_element(By.CSS_SELECTOR,'.pagination-btn.pagination-btn--next').click()
    except:
        break

driver.quit()

rawTable=pd.DataFrame(rawTable,columns=['rawData'])
rawTable=rawTable['rawData'].str.split('\n',expand=True)
rawTable.columns=['Rank','Name','Net Worth','Age','State','Source of Wealth','Philanthropic Score']
rawTable['Net Worth']=rawTable['Net Worth'].replace(' ','',regex=True)

def scrapeProfile(url):
    profileData=pd.DataFrame(columns = ['realTimeWealth','profile','url'])
    driver = webdriver.Chrome(service=s)
    driver.get(url)
    profileSummary=driver.find_element(By.CLASS_NAME,'profile-text').text
    realTimeWealth=driver.find_element(By.CLASS_NAME,'profile-info__item-value').text
    driver.quit()
    if realTimeWealth is None:
        realTimeWealth=''
    profileData.loc[0]=[realTimeWealth,profileSummary,url]
    return profileData

profileDataAll=pd.DataFrame(columns = ['Real Time Wealth','Profile','url'])

for i in range(len(ids)):
    profileData=scrapeProfile(profileStub+ids[i]+'/')
    profileDataAll=profileDataAll.append(profileData)
    time.sleep(1)
    print("Finished "+str(i+1)+" profiles out of "+str(len(ids)))
 
profileDataAll.reset_index(drop=True, inplace=True)
profiles=pd.concat([rawTable,profileDataAll],axis=1)    
profiles=profiles[['Rank','Name','Net Worth','Real Time Wealth','Age','State','Source of Wealth','Philanthropic Score','Profile','url']]

profiles.to_csv('Forbes400Rich.csv',index=False)