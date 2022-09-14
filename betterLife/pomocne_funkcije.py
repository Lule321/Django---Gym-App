from django.http import HttpRequest

from betterLife.models import Jelo
from .pomocne_klase import *

def header_trener(i):
    str = ""
    for j in range (0,i):
        str += "../"
    polje1 = LinkPolje("Klijenti", str + "pregled_klijenata/")
    polje2 = LinkPolje("Vezbe", str + "pregled_vezbi/")
    polje3 = LinkPolje("Jela", str + "pregled_jela/")
    polje_pretposlednje = LinkPolje("Profil",  str + "pregled_profila/")
    polje_poslednje = LinkPolje("Izloguj se", str + "logout_req/")
    return [polje1, polje2, polje3, polje_pretposlednje, polje_poslednje]


def trener_header_klijenti_pregled():
    polje1 = TekstualnoPolje("Broj Clanske Karte")
    polje2 = TekstualnoPolje("Ime")
    polje3 = TekstualnoPolje("Prezime")
    polje4 = TekstualnoPolje("Pol")
    poljePoslednje = LinkPolje("Pregled", "#")
    return [polje1, polje2, polje3, polje4, poljePoslednje]


def trener_upakuj_klijente_za_prikaz(klijenti):
    rows = list()
    row = None
    i = 0
    for klijent in klijenti:
        if i % 4 == 0:
            row = list()
            rows.append(row)
        i += 1
        if(klijent.slika):
            slikaPolje = SlikaPolje(klijent.first_name, "../pregled_klijenta/" + str(klijent.id), klijent.slika.url)
        else:
            slikaPolje = SlikaPolje(klijent.first_name, "../pregled_klijenta/" + str(klijent.id), "../../media/imgs/korisnici/profilnaBezSlike.png")
        row.append(slikaPolje)
    return rows


def trener_upakuj_jela_za_prikaz(jela):
    rows = list()
    row = None
    i = 0
    for jelo in jela:
        if i % 4 == 0:
            row = list()
            rows.append(row)
        i+=1
        if(jelo.slika):
            slikaPolje = SlikaPolje(jelo.naziv, "../pregled_jelo/" + str(jelo.id), jelo.slika.url)

        else:
            slikaPolje = SlikaPolje(jelo.naziv, "../pregled_jelo/" + str(jelo.id), "../../media/imgs/jela/jeloBezSlike.jpg")
        row.append(slikaPolje)
    return rows

def trener_upakuj_vezbe_za_prikaz(vezbe):
    rows = list()
    row = None
    i = 0
    for vezba in vezbe:
        if i % 4 == 0:
            row = list()
            rows.append(row)
        i+=1
        if(vezba.slika):
            slikaPolje = SlikaPolje(vezba.naziv, "../pregled_vezbe/" + str(vezba.id), vezba.slika.url)

        else:
            slikaPolje = SlikaPolje(vezba.naziv, "../pregled_vezbe/" + str(vezba.id), "../../media/imgs/vezbe/vezbaBezSlike.png")
        row.append(slikaPolje)
    return rows