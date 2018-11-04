import os
import re


def odpri_datoteko(frontpage):
    '''Vrne vsebino datoteke kot niz'''
    with open(frontpage, encoding='utf-8') as datoteka:
        return datoteka.read()


def razbij_na_ekipe(frontpage):
    '''Vrne seznam ekip'''
    spletna_stran = odpri_datoteko(frontpage)
    vzorec = re.compile(
        r'<td class="IndividualStatsRank" align="center">'
        r'\d+?</td><td align="left">(.*?)</tr>',
        re.DOTALL)
    seznam_vrstic = vzorec.findall(spletna_stran)
    return seznam_vrstic


def izloci_leto(frontpage):
    '''Izloci iz imena frontpaga leto'''
    vzorec = r'.+?(?P<leto>\d+)\.html'
    ujemanje = re.search(vzorec, frontpage)
    leto = int(ujemanje.group(1))
    return leto


def izloci_statisticni_podatek(frontpage):
    '''Vrne vrsto statisticnega podatka ki je v frontpage'''
    vzorec = r'.*?(?P<stat>[A-Z]\w+?-?\w*?)-\w+?-\d*?.html'
    ujemanje = re.search(vzorec, frontpage)
    podatek = ujemanje.group(1)
    return podatek


def izloci_lokacijo(frontpage):
    '''Vrne nam podatek ali klub gostoval ali gostil'''
    vzorec = r'.*?(HomeGames|AwayGames).*?'
    ujemanje = re.search(vzorec, frontpage)
    lokacija = ujemanje.group(1)
    return lokacija


def uredi_statistiko(statistika):
    '''Spremeni nize stevil v stevila'''
    statistika['st_tekem'] = int(statistika['st_tekem'])
    statistika['podatek'] = int(statistika['podatek'])
    statistika['povprecje'] = float(statistika['st_tekem'])
    statistika['na_40_min'] = float(statistika['na_40_min'])
    if statistika['kje'] == 'HomeGames':
        statistika['kje'] = 'doma'
    else:
        statistika['kje'] = 'v gosteh'
    return statistika


def posloveni_podatek(slovar):
    '''Posloveni vrsto podatka'''
    if slovar['vrsta_podatka'] == 'Score':
        slovar['vrsta_podatka'] = 'dane tocke'
    elif slovar['vrsta_podatka'] == 'Assistances':
        slovar['vrsta_podatka'] = 'podaje'
    elif slovar['vrsta_podatka'] == 'Prejete-tocke':
        slovar['vrsta_podatka'] = 'prejete tocke'
    elif slovar['vrsta_podatka'] == 'Turnovers':
        slovar['vrsta_podatka'] = 'izgubljene zoge'
    elif slovar['vrsta_podatka'] == 'Steals':
        slovar['vrsta_podatka'] = 'ukradene zoge'
    elif slovar['vrsta_podatka'] == 'FoulsCommited':
        slovar['vrsta_podatka'] = 'osebne napake'
    elif slovar['vrsta_podatka'] == 'BlocksFavour':
        slovar['vrsta_podatka'] = 'blokade'
    elif slovar['vrsta_podatka'] == 'TotalRebounds':
        slovar['vrsta_podatka'] = 'skoki'
    return slovar


def statistika_ekipe(ekipa, podatek, sezona, kje):
    '''Vrne statistiko ekipe gleda na podatek ki je zapisan v datoteki'''
    slovar = {'vrsta_podatka': podatek, 'sezona': sezona, 'kje': kje}
    vzorec = re.compile(
        r'<span class="hidden-xs">(?P<klub>.+?)</span>'
        r'<span class="visible-xs">(?P<kratica>.{3})</span>'
        r'\s*?</a></td><td align="right">(?P<st_tekem>\d+?)</td>'
        r'<td align="right">(?P<podatek>\d+?)</td>'
        r'<td align="right">(?P<povprecje>\d+?\.?\d*?)</td>'
        r'<td align="right">(?P<na_40_min>\d+?\.?\d*?)</td>',
        re.DOTALL)
    ujemanje = vzorec.search(ekipa)
    slovar = dict(slovar, **ujemanje.groupdict())
    uredi_statistiko(slovar)
    posloveni_podatek(slovar)
    return slovar


def statistika_sezone(frontpage):
    '''Vrne statistiko ekip za posamezno sezono'''
    seznam_vrstic = razbij_na_ekipe(frontpage)
    seznam_podatkov = []
    leto = izloci_leto(frontpage)
    podatek = izloci_statisticni_podatek(frontpage)
    lokacija = izloci_lokacijo(frontpage)
    for vrstica in seznam_vrstic:
        podatki = statistika_ekipe(vrstica, podatek, leto, lokacija)
        seznam_podatkov.append(podatki)
    return seznam_podatkov


def zdruzi_statistiko(mapa):
    '''Vrne seznam slovarjev za vse statisticne podatke po sezonah'''
    datoteke = os.listdir(mapa)
    seznam = []
    for datoteka in datoteke:
        pot = os.path.join(mapa, datoteka)
        statistika = statistika_sezone(pot)
        seznam.extend(statistika)
    return seznam
