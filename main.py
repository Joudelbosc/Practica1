# -*- coding: utf-8 -*-
import locale
import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime
from tempfile import NamedTemporaryFile

dt = datetime.now()
print(dt.strftime("%A, %d-%b-%Y"))
locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
print(dt.strftime("%A, %d-%b-%Y"))

fhand = urllib.request.urlopen('http://www.meff.es/esp/Derivados-Commodities/Precios-Cierre')

url = "http://www.meff.es/esp/Derivados-Commodities/Precios-Cierre"
soup = BeautifulSoup(fhand, features="html.parser")

rows = []
date = []
value1 = []
value2 = []

for row in soup.findAll('table')[0].tbody.findAll('tr'):

    row = str(row)
    # Aquesta línia no fa res --- rows.append(row)
    m = re.search('(<td class="Destacado text-left">Día (.+?)</td>)', row)
    print("ROWWW:   " + row[int(len(row)/2):])

    if m:
        day = re.search('((.+?)-)', m.group(2))
        month = re.search('(-(.+?)-)', m.group(2))
        year = re.search('(\w{3}-(.+?)$)', m.group(2))
        date.append(datetime.strptime(day.group(2) + "-" + month.group(2) + ".-" + year.group(2), '%d-%b-%Y'))
        v1 = re.search('(<td class="Sep">\xa0</td><td>(.+?)</td><td class=)', row).group(2).replace(',', '.')
        v2 = re.search('(<td class="Sep">\xa0</td><td>(.+?)</td><td class=)', row[int(len(row)/2):]).group(2)\
            .replace(',', '.')
        try:
            value1.append(float(v1))
        except ValueError:
            value1.append(float(0))
        try:
            value2.append(float(v2))
        except ValueError:
            value2.append(float(0))
    # Si sempre comença amb els dies i posa els resums al final, podem fer un break i així no acaba de fer tot el bucle,
    # quan ja no quedin dies per parsejar. Si no sempre fos així, podríem filtrar al principi només les rows que
    # contenen dies (files que comencen amb la paraula 'Día'):
    else:
        break

d = {'Dia': date, 'Base': value1, 'Pic': value2}
df_futures = pd.DataFrame(data=d)

# PER QUÈ ESTÀ REPETIT DUES VEGADES LA SEGÜENT LÍNIA?
df_futures.index = df_futures['Dia']
del df_futures['Dia']

# PASSAR AQUESTA COLUMNA A DATA, PENSO QUE ÉS MÉS EFICIENT FENT-HO A DALT, JA QUE TREBALLEM AMB LLISTES, EN COMPTES DE
# DATAFRAME!
# df_futures.index = pd.to_datetime(df_futures.index, format="%d-%b-%Y")

print(df_futures)
df_futures.to_csv('./dfFutures.csv')


