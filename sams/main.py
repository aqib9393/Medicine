#All required Libraries
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
options = webdriver.ChromeOptions() 
options.add_argument("start-maximized")
options.add_argument("--auto-open-devtools-for-tabs")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

driver.maximize_window()

driver.get('https://www.sams.com.mx/sitemap')

page=[]
for x in range(1,5):
    page.append(driver.find_element_by_xpath('//*[@id="page-ng"]/div/div/div/div/div[3]/div[18]/div[2]/div[1]/div/a['+str(x)+']').get_attribute('href'))
for x in range(1,4):
    page.append(driver.find_element_by_xpath('//*[@id="page-ng"]/div/div/div/div/div[3]/div[18]/div[2]/div[2]/div/a['+str(x)+']').get_attribute('href'))
for x in range(1,7):
    page.append(driver.find_element_by_xpath('//*[@id="page-ng"]/div/div/div/div/div[3]/div[18]/div[2]/div[3]/div/a['+str(x)+']').get_attribute('href'))
for x in range(1,5):
    page.append(driver.find_element_by_xpath('//*[@id="page-ng"]/div/div/div/div/div[3]/div[18]/div[2]/div[4]/div/a['+str(x)+']').get_attribute('href'))

allLinks=[]
for singlepage in page:
    driver.get(singlepage)
    links=driver.find_elements_by_css_selector('a.item-image')
    for lnk in links:
        allLinks.append(lnk.get_attribute('href'))

allData=[]

for url in allLinks:   
        driver.get(url)
        #category

        cat=WebDriverWait(driver,2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,' span > a')))
            #cat=driver.find_elements_by_css_selector('div.desktop.header-padding>div>ol>li')
        _category=cat[-1].text
            
        
        #price
        _price=WebDriverWait(driver,2).until(EC.presence_of_element_located((By.CLASS_NAME,'prod-price-special'))).text
        #_price=driver.find_element_by_class_name('prod-price-special').text
        #name
        _product=WebDriverWait(driver,2).until(EC.presence_of_element_located((By.CLASS_NAME,'prod-name'))).text
        #_product=driver.find_element_by_class_name('prod-name').text
        price=_price[:-2]+'.'+_price[-2:]
        #cut price
        try:
            _cutPrice=WebDriverWait(driver,2).until(EC.presence_of_element_located((By.CLASS_NAME,'price-before-label'))).text
            #_cutPrice=driver.find_element_by_class_name('price-before-label').text
        except:
            _cutPrice=''
        #description
        _description=WebDriverWait(driver,2).until(EC.presence_of_element_located((By.CLASS_NAME,'inner-htmlContent'))).text
        #_description= driver.find_element_by_class_name('inner-htmlContent').text.replace('\n',' ')
        #image
        images=[]
        _image=WebDriverWait(driver,2).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.main-image>img'))).get_attribute('src')
        #_image=driver.find_element_by_css_selector('div.main-image>img').get_attribute('src')
        images.append(_image)
        for x in range(1,4):
            images.append(_image[:-5]+'-'+str(x)+'m.jpg')

        d1={
                "Pharmacyname":"Sam's Club",
                "URL":url,
                "Category":_category,
                "Product":_product,
                "Price":price,
                "CutPrice":_cutPrice,
                "Image":images,
                'Amount':float(price.replace('$','')),
                "ExtraInfo":{  
                    _description
                        }
                    } 
        allData.append(d1)