from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import locale
import re
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Emmagatzemem la data actual i posem l'idioma en castellà, ja que les dates que haurem de parcejar estaran en castellà:
dt = datetime.now()
locale.setlocale(locale.LC_ALL, 'es_ES.utf8')

# Utilitzem Selenium per a anar a trobar les dades:
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.meff.es/esp/")
time.sleep(3)
driver.find_element_by_class_name("btn-desplegable").click()

button_cookies = driver.find_element_by_id("CookiesOk")
button_cookies.click()

desplegable = driver.find_element_by_id("despleg-menu")
search = desplegable.find_element_by_class_name("form-control")
search.send_keys("precios de cierre")
desplegable.find_element_by_class_name("btn").click()

time.sleep(0.5)

driver.find_element_by_class_name("media-heading").click()

table_driver = driver.find_element_by_id("Contenido_Contenido_tblDatos")
table_str = table_driver.get_attribute('innerHTML')
driver.quit()

# Una vegada que hem trobat les dades i les hem assignat a una variable en format d'string, la parcejem per a separar
# i organitzar les dades en un DataFrame, que guardarem posteriorment:
regex = '<td.+'
table_rows_list = re.findall(regex, table_str)

rows = []
date = []
value1 = []
value2 = []
for row in table_rows_list:

    row = str(row)
    m = re.search('(<td class="Destacado text-left">Día (.+?)</td>)', row)

    if m:
        day = re.search('((.+?)-)', m.group(2))
        month = re.search('(-(.+?)-)', m.group(2))
        year = re.search('(\w{3}-(.+?)$)', m.group(2))

        # El parceig de la data el posem amb un try, ja que canvia si l'executem a Linux o Windows:
        try:
            date.append(datetime.strptime(day.group(2) + "-" + month.group(2) + ".-" + year.group(2), '%d-%b-%Y'))
        except ValueError:
            date.append(datetime.strptime(day.group(2) + "-" + month.group(2) + "-" + year.group(2), '%d-%b-%Y'))

        v1 = re.search('(<td class="Sep">&nbsp;</td><td>(.+?)</td><td class=)', row).group(2).replace(',', '.')
        v2 = re.search('(<td class="Sep">&nbsp;</td><td>(.+?)</td><td class=)', row[int(len(row) / 2):]).group(2) \
            .replace(',', '.')
        try:
            value1.append(float(v1))
        except ValueError:
            value1.append(None)
        try:
            value2.append(float(v2))
        except ValueError:
            value2.append(None)
    # Com que sempre comença amb els dies i posa els resums al final, podem fer un break i així no acaba de fer tot el
    # bucle, quan ja no quedin dies per parcejar. Si no sempre fos així, podríem filtrar al principi només les rows que
    # contenen dies (files que comencen amb la paraula 'Día'):
    else:
        break

d = {'Dia': date, 'Preu Base (€)': value1, 'Preu Pic (€)': value2}
df_futures = pd.DataFrame(data=d)

# Posem la variable 'Dia' com a index i esborrem la columna antiga:
df_futures.index = df_futures['Dia']
del df_futures['Dia']

# Guardem les dades en un CSV, amb el títol començant pel període dels futurs que recullen les dades:
df_futures.to_csv('./{}_{}_dfFutures.csv'.format(str(df_futures.index[1].date()), str(df_futures.index[-1].date())))

# Guardem i mostrem per pantalla el contingut del dataset resumit en un gràfic dels preus base i pic dels futurs, en
# funció del dia (imatge adjunta al punt 5 del PDF):
df_futures.plot()
plt.xlabel('Data')
plt.ylabel('Precios de cierre (€)')
plt.title('Futuros eléctricos {} a {}'.format(str(df_futures.index[1].date()), str(df_futures.index[-1].date())))
plt.savefig('{}_{}_Futurs_elec.png'.format(str(df_futures.index[1].date()), str(df_futures.index[-1].date())))
plt.show()