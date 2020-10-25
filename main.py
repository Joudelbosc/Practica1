# -*- coding: utf-8 -*-
import re
from tempfile import NamedTemporaryFile

from bs4 import BeautifulSoup

import locale
import urllib.request

import pandas as pd
from datetime import datetime

fhand = urllib.request.urlopen('http://www.meff.es/esp/Derivados-Commodities/Precios-Cierre')

url = "http://www.meff.es/esp/Derivados-Commodities/Precios-Cierre"
soup = BeautifulSoup(fhand)

rows = []
date = []
value = []



for row in soup.findAll('table')[0].tbody.findAll('tr'):

    row = str(row)
    rows.append(row)
    m = re.search('(<td class="Destacado text-left">Día (.+?)</td>)', row)

    if m:

        date.append(m.group(2))
        v = re.search('(class="Sep"> </td><td>(.+?)</td><td class=)', row).group(2).replace(',','.')
        re.search('(<td class="Sep"> </td><td>(.*?)</td><td class="DifSb">)', row).group(2)
        #print(d)
        value.append(v)


d = {'date':date, 'value': value}
df_futures = pd.DataFrame(data=d)
df_futures['value'] = df_futures.value.astype(float)

df_futures.index = df_futures['date']
df_futures.index = df_futures['date']
del df_futures['date']
locale.setlocale(locale.LC_ALL, 'es_ES.utf8')
df_futures.index = pd.to_datetime(df_futures.index, format="%d-%b-%Y")

print(df_futures)