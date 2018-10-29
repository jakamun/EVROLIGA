import os
import sys
import requests


def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)


def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')


# zanka s katero sem pobral podatke po posameznih sezonah za vsak parametr posebej
statisticni_podatki = [
    'Score', 'TotalRebounds', 'Assistances', 'Steals',
    'BlockFavour', 'Turnover', 'FoulsCommited'
    ]

for tekma in ['HomeGames', 'AwayGames']:
    for podatek in statisticni_podatki:
        for sezona in range(2000, 2018):
            url = (
                'http://www.euroleague.net/main/statistics?mode=Leaders'
                '&entity=Clubs&seasonmode=Single&seasoncode=E{}&cat={}&'
                'agg=Accumulated&misc={}'
                ).format(sezona, podatek, tekma)
            shrani_spletno_stran(url, 'spletne-strani\{}\{}-Sezona-{}.html'.format(tekma, podatek, sezona))


# tu se za prejete tocke po letih
for tekma in ['HomeGames', 'AwayGames']:
    for sezona in range(2000, 2018):
        url = (
            'http://www.euroleague.net/main/statistics?mode=Leaders&entity'
            '=Clubs&seasonmode=Single&seasoncode=E{}&cat=Score&agg'
            '=AccumulatedReverse&misc={}'
        ).format(sezona, tekma)
        shrani_spletno_stran(url, 'spletne-strani\{}\Prejete-tocke-Sezona-{}.html'.format(tekma, sezona))
