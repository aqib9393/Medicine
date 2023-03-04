#All required Libraries
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
driver=webdriver.Chrome()
driver.maximize_window()
    #All pages urls
pagelst=['https://www.farmaciasespecializadas.com/especialidades/category/alta-especialidad-1/',
         'https://www.farmaciasespecializadas.com/medicamentos-generales/category/medicamentos-1/',
         'https://www.farmaciasespecializadas.com/art%C3%ADculos-de-medici%C3%B3n/category/equipos-de-medicion-1/',
         'https://www.farmaciasespecializadas.com/bienestar-sexual/category/salud-sexual/',
         'https://www.farmaciasespecializadas.com/cuidado-personal/category/cuidado-personal/',
         'https://www.farmaciasespecializadas.com/dermacosm%C3%A9ticos/category/dermatologia-1/',
         'https://www.farmaciasespecializadas.com/vitaminas-y-suplementos/category/vitaminicos-y-nutricionales/']

pagelnght=[62,279,29,3,22,51,21]

allLinks=[]
category=[]
for idx, page in enumerate(pagelst):
    for x in range(pagelnght[idx]):
        driver.get(page+str(x+1))
        driver.implicitly_wait(5)
        sleep(1)
        #webdriver(driver,3).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#figure > a')))
        links=WebDriverWait(driver,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#figure > a')))
        for link in links:
            allLinks.append(link.get_attribute('href'))
            category.append(str(page+str(x+1)).split('/')[3])