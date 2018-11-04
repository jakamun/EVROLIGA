import zajem_statistike as statistika
import zajem_ekipe as ekipa
import csv
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


# zapisem csv in naredim json kjer so vsi podatki skupaj
seznam_statistike = []

for tekma in ['HomeGames', 'AwayGames']:
    mapa = 'spletne-strani\\{}'.format(tekma)
    podatki = statistika.zdruzi_statistiko(mapa)
    seznam_statistike.extend(podatki)

kam_zapisi = 'podatki\\statistika-ekip.csv'
zapisi_csv(seznam_statistike, kam_zapisi)

# naredi csv datoteke za vse igralce in trenerje
mapa = 'spletne-strani\\ekipe'
osebe = ekipa.igralci_in_trenerji(mapa)
igralci = osebe['igralci']
trenerji = osebe['trenerji']
zapis_igralcev = 'podatki\\{}.csv'.format('igralci')
zapis_trenerjev = 'podatki\\{}.csv'.format('trenerji')
zapisi_csv(igralci, zapis_igralcev)
zapisi_csv(trenerji, zapis_trenerjev)

# naredi csv datoteke za vse tekme od zacetka evrolige
tekme = ekipa.vse_tekme(mapa)
zapisi_tekme = 'podatki\\tekme.csv'
zapisi_csv(tekme, zapisi_tekme)
