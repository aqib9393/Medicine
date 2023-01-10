from selenium import webdriver
from pymongo import MongoClient
from time import sleep
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
driver = webdriver.Edge('..//msedgedriver.exe')
cluster=MongoClient('mongodb+srv://scrapper:H57jHSsM4KT1eqPG@webscrapper.3uveefb.mongodb.net/scrapper?retryWrites=true&w=majority')
pagelst=['https://tiendaenlinea.benavides.com.mx/semana-del-bebe.html?p=','https://tiendaenlinea.benavides.com.mx/promociones.html?p=','https://tiendaenlinea.benavides.com.mx/salud.html?p=',
'https://tiendaenlinea.benavides.com.mx/farmacia.html?p=','https://tiendaenlinea.benavides.com.mx/prevencion.html?p=','https://tiendaenlinea.benavides.com.mx/marca-propia.html?p=',
'https://tiendaenlinea.benavides.com.mx/salud-sexual.html?p=','https://tiendaenlinea.benavides.com.mx/bebes/alimentos.html?p=','https://tiendaenlinea.benavides.com.mx/cuidado-personal-y-belleza.html?p='
,'https://tiendaenlinea.benavides.com.mx/dermocosmeticos.html?p=','https://tiendaenlinea.benavides.com.mx/alimentos-y-hogar.html?p=','https://tiendaenlinea.benavides.com.mx/child-care.html?p=']
pagelnght=[5,6,4,23,1,4,1,2,10,2,3,2]
driver.get('https://tiendaenlinea.benavides.com.mx/semana-del-bebe.html')
driver.implicitly_wait(5)
driver.find_element(By.CSS_SELECTOR,'button.buton-region').click()
webPage=[]
pageUrl=[]
for x in range(0,len(pagelst)):
    for y in range(1,pagelnght[x]+1):
        print(x)
        url=pagelst[x]+str(y)
        driver.get(pagelst[x]+str(y))
        allpage=driver.find_elements(By.CSS_SELECTOR,'a.product')
        for z in allpage:
            pageUrl.append(z.get_attribute('href'))
            webPage.append(url)
category=[]
title=[]
price=[]
discount=[]
imgURL=[]
d1=[]
df=pd.DataFrame()
df['Web Page']=webPage
df['Page Url']=pageUrl

gotData=[]

for x in range(0,len(df)):
    print(x)
    driver.get(df['Page Url'][x])
    driver.implicitly_wait(3)
    _category=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CLASS_NAME,'categoriesproductdetail'))).text
    _product=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CLASS_NAME,'page-title'))).text
    _price=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CLASS_NAME,'price'))).text
    _cutPrice=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CLASS_NAME,'price-wrapper'))).text
    if _price==_cutPrice:
        _cutPrice=''
    try:
        _imgUrl=WebDriverWait(driver,2).until(EC.presence_of_element_located((By.CLASS_NAME,'fotorama__img'))).get_attribute('src')
    except:
        _imgUrl=WebDriverWait(driver,2).until(EC.presence_of_element_located((By.CLASS_NAME,'fotorama__img'))).get_attribute('src')
    WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID,'show-more-details'))).click()
    sleep(1)
    #extra
    _d1={}
    label=WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'th.label')))
    data=WebDriverWait(driver,3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'td.data')))
    for y in range(len(label)):
        _d1.update({label[y].text:data[y].text})

    d1={
       "URL":df['Page Url'][x], 
       "Category":_category,
        "Product":_product,
        "Price":_price,
        "Cut Price":_cutPrice,
        "Image":_imgUrl,  
        "ExtraInfo":{}
    }
    d1['ExtraInfo'].update(_d1)
    gotData.append(d1) 

db=cluster['Data']
collection=db['tiendaenlincea']
collection.insert_many(gotData)