# EVROLIGA

Za zadnjih nekaj sezon bom analiziral evroligaške klube.
Podatke bom pobral z uradne spletne strani  
[Evrolige](http://www.euroleague.net/).

### Za vsak klub bom pogledal:
  - Na katerem mestu je končal posamezno sezono,
  - kateri trener jih je vodil, 
  - kateri igralci so igrali za ta klub, 
  - koliko točk, asistenc, skokov... so dali,
  - kako so igrali na gostujočih in domačih tekmah.
 
 
 ### Hipoteze:
  - Kateri igralci in trenerji so bili v klubih, ki so bili prvaki?
  - Kateri klubi so najuspesnejši v tem tekmovanju?
  - Kaj je bolj pomembno za uspešno sezono dober napad ali dobra obramba?
  - Ali je bolje odigrajo nekoliko slabše redni del sezone in prihranijo nekaj moči za končnico ali, da igrajo redni del s polno močjo in po zaslugi visoke uvrstitve v rednem delu dobijo lažje nasprotnike v končnici?

## Opis tabel
Vse datoteke vsebujejo kratico kluba.

### Statistika-ekip:
*V tej csv datoteki so shranjene vse vrste statističnih podatkov po sezonah za vsak klub posebej.*
- 1.stolpec: Vrsta statisticega podatka (podaje, skoki, podaje, itd.)
- 2.stolpec: Sezona
- 3.stolpec: Kje so igrali doma ali v gosteh
- 4.stolpec: Klub
- 5.stolpec: Kratica kluba
- 6.stolpec: Stevilo tekem, ki so jih odigrali
- 7.stolpec: Vrednost statisticnega podatka
- 8.stolpec: Povprecje statisticnega podatka
- 9.stolpec: Koliksna je vrednost podatka na 40 minut

### Tekme:
*Tu so rezultati vseh tekem od zacetka tekmovanja do lanske sezone.*
- 1.stolpec: Kratica kluba
- 2.stolpec: Faza tekmovanja (redni del, koncnica, itd.)
- 3.stolpec: Stevilka tekme oz. koliko tekem je klub pred to tekmo ze odigral
- 4.stolpec: Ali so zmagali ali izgubili
- 5.stolpec: Ali so igrali v gosteh ali doma
- 6.stolpec: Nasprotnik
- 7.stolpec: Rezultat

### Igralci:
*Kateri igralci so igrali za kateri klub po sezonah*
- 1.stolpec: Kratica kluba
- 2.stolpec: Sezona
- 3.stolpec: Ime igralca
- 4.stolpec: Igralni položaj
- 5.stolpec: Narodnost
- 6.stolpec: Datum rojstva
- 7.stolpec: Visina v metrih

### Trenerji:
*Kateri igralci so igrali za kateri klub po sezonah*
- 1.stolpec: Kratica kluba
- 2.stolpec: Sezona
- 3.stolpec: Ime trenerja
- 4.stolpec: Funkcija
- 5.stolpec: Narodnost
- 6.stolpec: Datum rojstva
