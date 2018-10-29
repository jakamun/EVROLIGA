import os
import re
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


def odpri_datoteko(file):
    with open(file, encoding='utf-8') as datoteka:
        return datoteka.read()


def poberi_vrstice(frontpage):
    '''Vrne seznam vrstic tabele, pobrane spletne strani'''
    spletna_stran = odpri_datoteko(frontpage)
    vzorec = re.compile(r'<td class="IndividualStatsRank" align="center">\d+?</td><td align="left">', re.DOTALL)
    odrezi = re.compile(r'</div><div class="wp-module wp-module-statshome wp-module-79tiokf9mo5vuxib game-center-statshome"></div>', re.DOTALL)
    seznam_vrstic = vzorec.split(spletna_stran)
    seznam_vrstic = seznam_vrstic[1:]
    odrezano = seznam_vrstic[-1]
    seznam_vrstic[-1] = odrezi.split(odrezano)[0]
    return seznam_vrstic


def statistika_ekipe(ekipa):
    vzorec = re.compile(r'<span class="hidden-xs">(?P<klub>.+?)</span><span class="visible-xs">.{3}</span>'
                        r'\s*?</a></td><td align="right">(?P<tekme>\d+?)</td>'
                        r'<td align="right">(?P<tocke>\d+?)</td>'
                        r'<td align="right">(?P<povprecje>\d+?\.?\d*?)</td>'
                        r'<td align="right">(?P<na_40_minut>\d+?\.?\d*?)</td>',
                        re.DOTALL)
    ujemanje = vzorec.search(ekipa)
    slovar = ujemanje.groupdict()
    return slovar


def statistika_sezone(frontpage):
    seznam_vrstic = poberi_vrstice(frontpage)
    seznam_podatkov = []
    for vrstica in seznam_vrstic:
        podatki = statistika_ekipe(vrstica)
        seznam_podatkov.append(podatki)
    return seznam_podatkov



    
    