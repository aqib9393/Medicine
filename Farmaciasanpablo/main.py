from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient
cluster=MongoClient('mongodb+srv://scrapper:H57jHSsM4KT1eqPG@webscrapper.3uveefb.mongodb.net/scrapper?retryWrites=true&w=majority')
driver = webdriver.Edge('msedgedriver.exe')
pagelst=['https://www.farmaciasanpablo.com.mx/medicamentos/c/06?pageSize=48&currentPage=']
pagelnght=[1]
def xpath(path):
    return WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,path))).text

allPages=[]
for x in range(0,len(pagelst)):
    for y in range(0,pagelnght[x]+1):
        driver.get(pagelst[x]+str(y))
        driver.implicitly_wait(5)
        pages=WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'a.row')))
        for z in pages:
            allPages.append(z.get_attribute('href'))

Data=[]

for page in allPages:
    print(page)
    driver.get(page)
    driver.implicitly_wait(10)
    driver.implicitly_wait(10)
    _url=driver.current_url
    #_category=xpath('/html/body/app-root/cx-storefront/main/cx-page-layout/cx-page-slot[3]/app-product-intro/div/div/span')
    _category=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > app-root > cx-storefront > main > cx-page-layout > cx-page-slot.Summary-Desk-Right.has-components > app-product-intro > div > div > span'))).text
    _imgurl=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'imgPDP'))).get_attribute('src')
    _product=xpath('/html/body/app-root/cx-storefront/main/cx-page-layout/cx-page-slot[3]/app-product-summary/div/div/div[1]/h3')
    try:        
        _price=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'h3.priceTotal'))).text
    except:
        _price=''   
            #extra info
    _extra=xpath('/html/body/app-root/cx-storefront/main/cx-page-layout/cx-page-slot[4]/app-product-information/div/div')
    extra={}
    ex=_extra.split('\n')
    d1={
            "URL":_url,
            "Category":_category,
            "Product":_product,
            "Price":_price,
            "Image":_imgurl,
            "ExtraInfo":{
                
                }
            }   
    for y in range(0,len(ex),2):
        extra.update({ex[y].replace(" ","_"):ex[y+1]})
        d1['ExtraInfo'].update(extra)
    Data.append(d1)
db=cluster['Data']
collection=db['farmaciasanpablo']
collection.insert_many(Data)