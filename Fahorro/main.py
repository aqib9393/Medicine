#All required Libraries
from selenium import webdriver
from time import sleep
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient

#Database Url
cluster=MongoClient('DB URL')

#Web driver path
driver = webdriver.Edge('..//msedgedriver.exe')

#All pages urls
pagelst=['https://www.fahorro.com/derma/productos-dermocosmeticos.html', 'https://www.fahorro.com/bebes.html','https://www.fahorro.com/promociones/vitaminas-app.html',
'https://www.fahorro.com/bienestar-sexual.html','https://www.fahorro.com/higiene-personal.html', 'https://www.fahorro.com/higiene-bucal.html','https://www.fahorro.com/hombre.html',
'https://www.fahorro.com/farmacia.html', 'https://www.fahorro.com/me-quiero-bien.html','https://www.fahorro.com/bebidas-y-snacks.html',
'https://www.fahorro.com/diabetes-2.html','https://www.fahorro.com/me-quiero-bien/prevencion.html']

#All pages length
pagelnght=[11,8,4,3,14,3,2,65,5,3,4,1]

#store all pages url in list
page_url=[]
cpage=[]
for alpages in range(0,len(pagelst)):
    for page in range(1,pagelnght[alpages]+1):
        url=pagelst[alpages]+'?p='+str(page)+'&product_list_limit=90'
        print(url)
        driver.get(url)
        driver.implicitly_wait(10)
        img=driver.find_elements(By.CSS_SELECTOR,'div.imagen-producto-listado > a')
        for y in img:
            page_url.append(y.get_attribute('href'))
            cpage.append(url)

#add page list to dataframe
df=pd.DataFrame()
df['Current Page']=cpage
df['page_url']=page_url

#run all pages and get price, product, and etc.
alldata=[]
for x in range(len(df)):
        print(x)
        driver.get(df['page_url'][x])
        driver.implicitly_wait(5)
        _product=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CSS_SELECTOR,'span.base'))).text
        _price=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CSS_SELECTOR,'span.price'))).text
        try:
            _img=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'magnify-opaque'))).get_attribute('src')
        except:
            _img=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'fotorama__img'))).get_attribute('src')
        try:

            WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID,'tab-label-additional-title'))).click()
        except:
            pass
        _extra=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.TAG_NAME,'tbody'))).text
        
        _category=df['Current Page'][0].split('?p')[0]
        _category=_category.split('.html')[0]
        _category=_category.split('.com/')[1]
        
        #insert every data in json format
        d1={
            "URL":df['page_url'][x],
            "Category":_category,
            "Product":_product,
            "Price":_price,
            "Image":_img,
            "ExtraInfo":{
                
                }
            }   
        extra={}
        ex=_extra.split('\n')
        for y in range(0,len(ex)):
            word=' '
            word=word.join(ex[y].split(' ')[:-1])
            extra.update({str(word):str(ex[y].split(' ')[-1])})
        d1['ExtraInfo'].update(extra)
        #add all json data into list
        alldata.append(d1)

#call Database
db=cluster['Data']
#Call databse collection
collection=db['fahorro']
#insert all data into collection
collection.insert_many(alldata)