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
        r'\d+?</td><td align="left">',
        re.DOTALL)
    odrezi = re.compile(
        r'</div><div class="wp-module wp-module-statshome '
        r'wp-module-79tiokf9mo5vuxib game-center-statshome"></div>',
        re.DOTALL)
    seznam_vrstic = vzorec.split(spletna_stran)
    seznam_vrstic = seznam_vrstic[1:]
    odrezano = seznam_vrstic[-1]
    seznam_vrstic[-1] = odrezi.split(odrezano)[0]
    return seznam_vrstic


def izloci_leto(frontpage):
    '''Izloci iz imena fila leto'''
    vzorec = r'.+?(?P<leto>\d+)\.html'
    ujemanje = re.search(vzorec, frontpage)
    leto = int(ujemanje.group(1))
    return leto


def izloci_statisticni_podatek(frontpage):
    '''Vrne nam katere vrste statisticni podatek nam predstavlja file'''
    vzorec = r'.*?(?P<stat>[A-Z]\w+?-?\w*?)-\w+?-\d*?.html'
    ujemanje = re.search(vzorec, frontpage)
    podatek = ujemanje.group(1)
    return podatek


def statistika_ekipe(ekipa, podatek):
    '''Vrne statistiko ekipe gleda na podatek ki nas zanima iz html'''
    vzorec = re.compile(
        r'<span class="hidden-xs">(?P<Klub>.+?)</span>'
        r'<span class="visible-xs">(?P<Kratica>.{3})</span>'
        r'\s*?</a></td><td align="right">(?P<St_tekem>\d+?)</td>'
        r'<td align="right">(?P<podatek>\d+?)</td>'
        r'<td align="right">(?P<Povprecje>\d+?\.?\d*?)</td>'
        r'<td align="right">(?P<Na_40_min>\d+?\.?\d*?)</td>',
        re.DOTALL)
    ujemanje = vzorec.search(ekipa)
    slovar = ujemanje.groupdict()
    slovar[podatek] = slovar.pop('podatek')
    return slovar


def statistika_sezone(frontpage):
    seznam_vrstic = razbij_na_ekipe(frontpage)
    seznam_podatkov = []
    leto = izloci_leto(frontpage)
    podatek = izloci_statisticni_podatek(frontpage)
    for vrstica in seznam_vrstic:
        podatki = statistika_ekipe(vrstica, podatek)
        podatki['Sezona'] = leto
        seznam_podatkov.append(podatki)
    return seznam_podatkov


def zdruzi_sezone(mapa, stat):
    '''Vrne seznam slovarjev za posamezen statisticni podatek za vse sezone'''
    datoteke = os.listdir(mapa)
    seznam = []
    for datoteka in datoteke:
        pot = os.path.join(mapa, datoteka)
        podatek = izloci_statisticni_podatek(datoteka)
        if stat == podatek:
            sezona = statistika_sezone(pot)
            seznam.extend(sezona)
    return seznam
