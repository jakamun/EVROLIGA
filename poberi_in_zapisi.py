import zajemi_podatke as zajem
import csv
import json


url_evrolige = re.compile(r'http://www.euroleague.net/main/statistics\?mode='
                          r'Leaders&entity=Clubs&seasonmode=Single'
                          r'&seasoncode=E2000&phasetypecode=PO%20%20%20%20%20'
                          r'%20%20%20&cat=Score&agg=Accumulated')


podatki = zajem.statistika_sezone('podatki\evro.html')
