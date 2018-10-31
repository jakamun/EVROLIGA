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

statisticni_podatki = [
    'Score', 'TotalRebounds', 'Assistances', 'Steals',
    'BlocksFavour', 'Turnovers', 'FoulsCommited', 'Prejete-tocke'
    ]

for tekma in ['HomeGames', 'AwayGames']:
    mapa = 'spletne-strani\\{}'.format(tekma)
    for podatek in statisticni_podatki:
        zapisi = 'podatki\\{}\\{}.csv'.format(tekma, podatek)
        data = statistika.zdruzi_sezone(mapa, podatek)
        zapisi_csv(data, zapisi)
