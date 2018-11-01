import zajem_statistike as statistika
import csv
import json
import os


def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)


def zapisi_csv(data, ime_datoteke):
    kljuci = data[0].keys()
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8', newline='') as datoteka:
        writer = csv.DictWriter(datoteka, fieldnames=kljuci)
        writer.writeheader()
        for slovar in data:
            writer.writerow(slovar)


def zapisi_json(podatki, ime_datoteke):
    '''Zapise podatke v json datoteko'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
        json.dump(podatki, datoteka, indent=4, ensure_ascii=False)


statisticni_podatki = [
    'Score', 'TotalRebounds', 'Assistances', 'Steals',
    'BlocksFavour', 'Turnovers', 'FoulsCommited', 'Prejete-tocke'
    ]

zdruzeno = {}

for tekma in ['HomeGames', 'AwayGames']:
    mapa = 'spletne-strani\\{}'.format(tekma)
    slovar = {}
    for podatek in statisticni_podatki:
        zapisi = 'podatki\\statistika\\{}\\{}.csv'.format(tekma, podatek)
        data = statistika.zdruzi_sezone(mapa, podatek)
        slovar[podatek] = data
        zapisi_csv(data, zapisi)
    zdruzeno[tekma] = slovar

zapisi_json(zdruzeno, 'podatki\\statistika\\celotna-statistika.json')
