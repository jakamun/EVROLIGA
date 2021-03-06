import os
import sys
import requests
import zajem_statistike as statistika


def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)


def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print('Shranjujem {} ...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')


# zanka s katero sem pobral podatke
# po posameznih sezonah za vsak parametr posebej
statisticni_podatki = [
    'Score', 'TotalRebounds', 'Assistances', 'Steals',
    'BlocksFavour', 'Turnovers', 'FoulsCommited'
    ]

for tekma in ['HomeGames', 'AwayGames']:
    for podatek in statisticni_podatki:
        for sezona in range(2000, 2018):
            url = (
                'http://www.euroleague.net/main/statistics?mode=Leaders'
                '&entity=Clubs&seasonmode=Single&seasoncode=E{}&cat={}&'
                'agg=Accumulated&misc={}'
                ).format(sezona, podatek, tekma)
            shrani_spletno_stran(
                url,
                'spletne-strani\\{}\\{}-Sezona-{}.html'.format(
                    tekma,
                    podatek,
                    sezona
                    )
                )


# tu se za prejete tocke po sezonah
for tekma in ['HomeGames', 'AwayGames']:
    for sezona in range(2000, 2018):
        url = (
            'http://www.euroleague.net/main/statistics?mode=Leaders&entity'
            '=Clubs&seasonmode=Single&seasoncode=E{}&cat=Score&agg'
            '=AccumulatedReverse&misc={}'
        ).format(sezona, tekma)
        shrani_spletno_stran(
            url,
            'spletne-strani\\{}\\Prejete-tocke-Sezona-{}.html'.format(
                tekma,
                sezona
                )
            )


# najprej poberem kratice in leta in jih vrnem v seznamu naborov
# potem pa s pomocjo tega seznama shranim spletne strani
def kratice_in_leta(mapa, stat):
    '''Vrne seznam naborov v katerem je kratica kluba in leto'''
    podatki = statistika.zdruzi_sezone(mapa, stat)
    seznam = []
    for slovar in podatki:
        nabor = (slovar['Kratica'], slovar['Sezona'])
        seznam.append(nabor)
    return seznam


kratice = kratice_in_leta('spletne-strani\\AwayGames', 'Assistances')

for nabor in kratice:
    kratica = nabor[0]
    leto = nabor[1]
    url = (
        'http://www.euroleague.net/competition/teams/'
        'showteam?clubcode={}&seasoncode=E{}'
    ).format(kratica, leto)
    shrani_spletno_stran(
        url,
        'spletne-strani\\ekipe\\{}-{}.html'.format(
            kratica,
            leto
            )
    )
