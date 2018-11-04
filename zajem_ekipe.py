import re
import os


def odpri_datoteko(ime_datoteke):
    '''Vrne vsebino datoteke kot niz'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return datoteka.read()


def razdeli_na_okna(frontpage):
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


# tu sem zajel mostva klubov
def zajemi_ekipo(frontpage):
    '''Vrne seznam igralcev in trenerja'''
    ekipa = razdeli_na_okna(frontpage)[0]
    vzorec = re.compile(
        r'<div class="name">(.+?</div>.+?)</div>',
        re.DOTALL
    )
    mostvo = vzorec.findall(ekipa)
    return mostvo


def pridobi_kratico(frontpage):
    '''Vrne kratico kluba ki se nahaja v imenu datoteke'''
    vzorec = r'.*?([A-Z]{3})-\d{4}.html'
    kratica = re.search(vzorec, frontpage)
    klub = kratica.group(1)
    return klub


def uredi_podatke_osebe(oseba):
    '''Uredi podatke trenerja ali pa igralca'''
    oseba['sezona'] = int(oseba['sezona'])
    oseba['rojstvo'] = int(oseba['rojstvo'])
    if 'visina' in oseba.keys():
        oseba['visina'] = float(oseba['visina'].replace(',', '.'))
        if int(oseba['visina']) == 0:
            oseba['visina'] = None
    return oseba


def podatki_o_igralcu(igralec, kratica):
    '''Vrne nam slovar podatkov o igralcih'''
    slovar = {'klub': kratica}
    vzorec = re.compile(
        r'<a href="/competition/players/showplayer\?'
        r'pcode=.+?&amp;seasoncode=E(?P<sezona>\d{4})">(?P<ime>.+?)</a>'
        r'.*?<span class="position">(?P<pozicija>\w*?)</span>'
        r'.*?<span class="country">(?P<narodnost>.+?)</span>'
        r'.*?<span class="birth">(?P<rojstvo>\d+?)</span>'
        r'.*?<span class="height">Height: (?P<visina>\d+\.?\d*?)</span>',
        re.DOTALL
    )
    ujemanje = vzorec.search(igralec).groupdict()
    slovar = dict(slovar, **ujemanje)
    uredi_podatke_osebe(slovar)
    return slovar


def podatki_o_trenerju(trener, kratica):
    '''Vrne nam podatke o trenerju'''
    slovar = {'klub': kratica}
    vzorec = re.compile(
        r'<a href="/competition/coaches/showcoach\?pcode='
        r'.+?&amp;seasoncode=E(?P<sezona>\d{4})">(?P<ime>.+?)</a>'
        r'.*?<span class="title">(?P<funkcija>.+?)</span>'
        r'.*?<span class="country">(?P<narodnost>.+?)</span>'
        r'.*?<span class="birth">(?P<rojstvo>\d+?)</span>',
        re.DOTALL
    )
    ujemanje = vzorec.search(trener).groupdict()
    slovar = dict(slovar, **ujemanje)
    uredi_podatke_osebe(slovar)
    return slovar


def mostvo(frontpage):
    '''Naredi slovar v katerem so igralci in trener'''
    kratica = pridobi_kratico(frontpage)
    roster = zajemi_ekipo(frontpage)
    igralci = roster[:-1]
    trener = podatki_o_trenerju(roster[-1], kratica)
    slovar = {'trener': trener}
    seznam_igralcev = []
    for igralec in igralci:
        player = podatki_o_igralcu(igralec, kratica)
        seznam_igralcev.append(player)
    slovar['igralci'] = seznam_igralcev
    return slovar


def igralci_in_trenerji(mapa):
    '''Vrne vse trenerje in igralce vseh sezon'''
    datoteke = os.listdir(mapa)
    slovar = {'igralci': [], 'trenerji': []}
    for datoteka in datoteke:
        pot = os.path.join(mapa, datoteka)
        roster = mostvo(pot)
        slovar['igralci'].extend(roster['igralci'])
        slovar['trenerji'].append(roster['trener'])
    return slovar


# tu so funkcije za zajem tekem
def razdeli_po_fazah(frontpage):
    '''Vrne seznam tekem pa fazah tekmovanja'''
    tekme = razdeli_na_okna(frontpage)[1]
    vzorec = r'<div class="TeamPhaseGamesMainContainer">'
    seznam_faz = re.split(vzorec, tekme)
    seznam_faz = seznam_faz[1:]
    return seznam_faz


def katera_faza(faza):
    '''Vrne niz ki pove kera faza tekmovanja je to'''
    vzorec = r'<span class="TeamPhaseGamesTitle">(.+?)</span>'
    ujemanje = re.findall(vzorec, faza)
    return ujemanje[0]


def zajemi_tekme(faza):
    '''Vrne seznam podatkov o tekmah ene faze'''
    vzorec = re.compile(
        r'<tr class="\w*?">(.+?)</tr>',
        re.DOTALL
    )
    tekma = vzorec.findall(faza)
    return tekma


def uredi_tekmo(tekma):
    tekma['st_tekme'] = int(tekma['st_tekme'])
    if tekma['kje'] == 'at':
        tekma['kje'] = 'v gosteh'
    else:
        tekma['kje'] = 'doma'
    return tekma


def podatki_o_tekmi(tekma, leto):
    '''Vrne slovar podatkov o posamezni tekmi'''
    slovar = {'sezona': leto}
    vzorec = re.compile(
        r'<td class="GameNumberContainer">(?P<st_tekme>\d*?)</td>'
        r'.*?<td class="WinLoseContainer">.*?<span>(?P<zmaga>W|L)</span>.*?'
        r'<span class="TeamPhaseGameVersusTypeContainer">(?P<kje>vs|at)'
        r'</span>&nbsp;<span>(?P<nasprotnik>.*?)</span>'
        r'.*?<span>(?P<rezultat>.*?)</span>',
        re.DOTALL
    )
    podatki = vzorec.search(tekma)
    slovar = dict(slovar, **podatki.groupdict())
    uredi_tekmo(slovar)
    return slovar


def tekme_faze(faza, klub, leto):
    '''Vrne seznam slovarjev tekem ene faze tekmovanja'''
    tekme = zajemi_tekme(faza)
    seznam = []
    del_tekmovanja = katera_faza(faza)
    for tekma in tekme:
        slovar = {'klub': klub, 'faza': del_tekmovanja}
        slovar = dict(slovar, **podatki_o_tekmi(tekma, leto))
        seznam.append(slovar)
    return seznam


def leto_datoteke(frontpage):
    '''Izloci iz imena frontpaga leto'''
    vzorec = r'.+?(?P<leto>\d+)\.html'
    ujemanje = re.search(vzorec, frontpage)
    leto = int(ujemanje.group(1))
    return leto


def vse_tekme_kluba(frontpage):
    '''Vrne rezultate vseh tekem v vseh fazah'''
    faze = razdeli_po_fazah(frontpage)
    seznam = []
    kratica = pridobi_kratico(frontpage)
    sezona = leto_datoteke(frontpage)
    for faza in faze:
        tekme = tekme_faze(faza, kratica, sezona)
        seznam.extend(tekme)
    return seznam


def vse_tekme(mapa):
    '''Vrne vse tekme neke sezone'''
    datoteke = os.listdir(mapa)
    seznam = []
    for datoteka in datoteke:
        pot = os.path.join(mapa, datoteka)
        tekme_kluba = vse_tekme_kluba(pot)
        seznam.extend(tekme_kluba)
    return seznam
