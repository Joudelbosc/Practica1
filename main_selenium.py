from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())


driver.get("https://www.meff.es/esp/")
time.sleep(2)

driver.find_element_by_class_name("btn-desplegable").click()

"""start_date = driver.find_element_by_name("ctl00$ctl00$Contenido$Contenido$Desde$Desde_Fecha")
start_date.clear() # clear any value that was in the field before (if you don't clear, will append the new string sent.)
start_date.send_keys("08/17/2018")"""
#search = driver.find_elements_by_name("ctl00$ctl00$Contenido$Contenido$Desde$Desde_Fecha")
#print(search)
#search.send("30/09/2020")
#search.send_keys(Keys.RETURN)

desplegable = driver.find_element_by_id("despleg-menu")

search = desplegable.find_element_by_class_name("form-control")

search.send_keys("precios de cierre")

desplegable.find_element_by_class_name("btn").click()

time.sleep(2)


try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "main"))
    )

    articles = main.find_elements_by_tag_name("article")
except:
    driver.quit()



time.sleep(5)


driver.quit()


