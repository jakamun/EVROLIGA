import os
import re
import sys
import requests


def odpri_datoteko(file):
    with open(file, encoding='utf-8') as datoteka:
        return datoteka.read()


def poberi_vrstice(frontpage):
    '''Vrne seznam vrstic tabele, pobrane spletne strani'''
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
</div><div class="wp-module wp-module-statshome wp-module-79tiokf9mo5vuxib game-center-statshome"></div>

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



    
    
