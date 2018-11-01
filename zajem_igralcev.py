import re
import os


def odpri_datoteko(ime_datoteke):
    '''Vrne vsebino datoteke kot niz'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return datoteka.read()


def razbij_stran(frontpage):
    '''Vrne seznam, v katerem so elementi posamezna okna strani'''
    spletna_stran = odpri_datoteko(frontpage)
    vzorec = re.compile(
        r'<div role="tabpanel" class="tab-pane fade\s?.*?" id="[a-z]+?">',
        re.DOTALL
    )
    odrezi = re.compile(
        r'<div class="wp-module wp-module-customcodeportalmodulecont'
        r'rol wp-module-name-adunit wp-module-5n5xb87cdsime9op">',
        re.DOTALL
        )
    seznam_oken = vzorec.split(spletna_stran)
    seznam_oken = seznam_oken[1:]
    odrezano = seznam_oken[-1]
    seznam_oken[-1] = odrezi.split(odrezano)[0]
    return seznam_oken


def zajemi_ekipo(frontpage):
    '''Vrne seznam igralcev in trenerja'''
    ekipa = razbij_stran(frontpage)[0]
    vzorec = re.compile(
        r'<div class="item (player|coach)">',
        re.DOTALL
    )
    roster = vzorec.split(ekipa)[1:]
    return roster[::-1][::2][::-1]


def podatki_o_igralcu(igralec):
    '''Vrne nam slovar podatkov o igralcih'''
    vzorec = re.compile(
        r'<div class="name">.*?'
        r'<a href="/competition/players/showplayer\?'
        r'pcode=\w+?&amp;seasoncode=E(?P<leto>\d{4})">(?P<ime>.+?)</a>'
        r'.*?<span class="position">(?P<pozicija>\w+?)</span>'
        r'.*?<span class="country">(?P<narodnost>.+?)</span>'
        r'.*?<span class="birth">(?P<rojstvo>\d+?)</span>'
        r'.*?<span class="height">Height: (?P<visina>\d+\.?\d*?)</span>',
        re.DOTALL
    )
    ujemanje = vzorec.search(igralec)
    slovar = ujemanje.groupdict()
    return slovar


def podatki_o_trenerju(trener):
    '''Vrne nam podatke o trenerju'''
    vzorec = re.compile(
        r'<div class="name">.*?'
        r'<a href="/competition/coaches/showcoach\?pcode='
        r'\w+?&amp;seasoncode=E(?P<leto>\d{4})">(?P<ime>.+?)</a>'
        r'.*?<span class="title">(?P<funkcija>.+?)</span>'
        r'.*?<span class="country">(?P<narodnost>.+?)</span>'
        r'.*?<span class="birth">(?P<rojstvo>\d+?)</span>',
        re.DOTALL
    )
    ujemanje = vzorec.search(trener)
    slovar = ujemanje.groupdict()
    return slovar


def podatki_o_igralcih(frontpage):
    '''Vrne podatke o igralcih neke ekipe'''
    ekipa = zajemi_ekipo(frontpage)[:-1]
    seznam = []
    for igralec in ekipa:
        slovar = podatki_o_igralcu(igralec)
        seznam.append(slovar)
    return seznam
