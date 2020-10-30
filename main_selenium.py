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


desplegable = driver.find_element_by_id("despleg-menu")

search = desplegable.find_element_by_class_name("form-control")

search.send_keys("precios de cierre")

desplegable.find_element_by_class_name("btn").click()

time.sleep(2)

# No se si fa res.
"""try:
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "main"))
    )

except:
    driver.quit()
"""

driver.find_element_by_class_name("media-heading").click()

time.sleep(5)

for table in driver.find_elements_by_class_name("Precios"):
    data = [item.text for item in table.find_elements_by_class_name("Destacado text-left")]
    print(data)

driver.quit()


