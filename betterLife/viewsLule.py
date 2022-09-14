from datetime import datetime
import datetime as datetime1 # meni treba nesto sa timedelta
from email import header
#import this
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ImageField
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from betterLife.formsLule import FormaJeloRegistracija, FormaKlijentRegistracija, FormaPlanTreninga, FormaTrenerPretraga, FormaTreningRegistracija, FormaVezbaRegistracija, FormaStavkaTreningaRegistracija

from betterLife.pomocne_funkcije import header_trener, trener_header_klijenti_pregled, trener_upakuj_jela_za_prikaz, trener_upakuj_klijente_za_prikaz, trener_upakuj_vezbe_za_prikaz
from .pomocne_klase import *
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required, permission_required
#from .formPanta import TrenerForm, KlijentForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist

def test_table_view(request: HttpRequest):
    template = loader.get_template("table_views\\table_base.html")
    nav1 = LinkPolje("Trener", "https://www.w3schools.com/python/python_classes.asp")
    nav2 = LinkPolje("Klijent", "https://docs.python.org/3/library/venv.html")
    nav3 = LinkPolje("Izloguj se", "#")
    tekst1 = TekstualnoPolje("tekst1")
    tekst2 = TekstualnoPolje("tekst2")
    tekst3 = TekstualnoPolje("tekst3")
    link1 = LinkPolje("link1", "#")
    link2 = LinkPolje("link2", "#")
    link3 = LinkPolje("link3", "#")
    header1 = TekstualnoPolje("header1")
    header2 = TekstualnoPolje("header2")
    header3 = LinkPolje("header3", "#")
    rows = [[tekst1, link1, tekst2],[link2, tekst3, link3]]
    lista_labele = [nav1, nav2, nav3]
    header_row = [header1, header2, header3]
    form = SearchForm(request.POST)
    context = {
        "form": form,
        'lista_labele':lista_labele,
        'rows':rows,
        'header_row': header_row,
    }
    return HttpResponse(template.render(context, request))


"""Lule-trener pogled"""
def trener_pregled_klijenata(request: HttpRequest):
    template = loader.get_template("trener\\trener_pregled_klijenata.html")
    formaTrenerPretraga = FormaTrenerPretraga(request.POST or None)

    if formaTrenerPretraga.is_valid():
        klijenti = Klijent.objects.filter(mojTrener=request.user).filter(first_name__contains = formaTrenerPretraga.cleaned_data["tekst"])
    else:
        klijenti = Klijent.objects.filter(mojTrener = request.user)
    rows = trener_upakuj_klijente_za_prikaz(klijenti)
    lista_labele = header_trener(1)
    context = {
        'lista_labele':lista_labele,
        'forma_pretraga_klijenta' : formaTrenerPretraga,
        'rows': rows,
    }
    return HttpResponse(template.render(context,request))

def trener_klijenti_reg_test(request:HttpRequest):
    template = loader.get_template("trener\\forma_reg_klijent.html")
    if request.method == "POST":
        formaKlijentRegistracija = FormaKlijentRegistracija(request.POST, request.FILES)
    else:
        formaKlijentRegistracija = FormaKlijentRegistracija()
    print(formaKlijentRegistracija.errors)
    if formaKlijentRegistracija.is_valid():
        noviKlijent = Klijent()
        noviKlijent.username = formaKlijentRegistracija.cleaned_data["username"]
        noviKlijent.password = formaKlijentRegistracija.cleaned_data["password"]
        noviKlijent.first_name = formaKlijentRegistracija.cleaned_data["first_name"]
        noviKlijent.last_name = formaKlijentRegistracija.cleaned_data["last_name"]
        noviKlijent.mojTrener = None
        noviKlijent.is_superuser = False
        noviKlijent.email = formaKlijentRegistracija.cleaned_data["email"]
        noviKlijent.date_joined = formaKlijentRegistracija.cleaned_data["date_joined"]
        noviKlijent.gender = formaKlijentRegistracija.cleaned_data["gender"]
        noviKlijent.brojClanskeKarte = formaKlijentRegistracija.cleaned_data["broj_clanske_karte"]
        noviKlijent.datumPoslednjeUplate = formaKlijentRegistracija.cleaned_data["datum_poslednje_uplate"]
        noviKlijent.slika = formaKlijentRegistracija.cleaned_data["slika"]
        print(formaKlijentRegistracija.cleaned_data["slika"])
        noviKlijent.save()
        return redirect("trener_pregled_klijenata")
    else:
        context = {'formaKlijentRegistracija':formaKlijentRegistracija,}
    return HttpResponse(template.render(context, request))

def trener_pregled_klijenta(request: HttpRequest, id):

    #inicijalizacija
    treninzi_po_danima_inverz = None
    id_plan_treninga = None
    lista_stavki_po_danima_inverz = None
    id_plan_ishrane = None


    klijent: Klijent = Klijent.objects.get(id=id)
    if klijent.mojTrener.korisnik_ptr_id != request.user.id:
        return redirect("trener_pregled_klijenata")
    template = loader.get_template("trener\\trener_pregled_klijenta.html")

    klijent = Klijent.objects.get(korisnik_ptr_id=id)
    postoji_plan_treninga : bool = False

    if Plan_Treninga.objects.filter(korisnik = klijent):
        postoji_plan_treninga = True
        plan_treninga = Plan_Treninga.objects.get(korisnik=klijent)

        id_plan_treninga = plan_treninga.id

        plan_treninga = Trening.objects.filter(planTreninga = plan_treninga).order_by('vreme')


        treninzi_po_danima = [None, None, None, None, None, None, None]
        redovi = [0,0,0,0,0,0,0]
        max_redova = 0
        for trening in plan_treninga:
            i = trening.dan.weekday()
            if(treninzi_po_danima[i] == None):
                treninzi_po_danima[i] = [trening]
            else:
                treninzi_po_danima[i].append(trening)
            redovi[i] += 1

        for br in redovi:
            if br > max_redova:
                max_redova = br


        for i in range(0, len(treninzi_po_danima)):
            if max_redova > 0 and treninzi_po_danima[i] == None:
                treninzi_po_danima[i] = list()
                for j in range(0, max_redova):
                    treninzi_po_danima[i].append(None)
            elif treninzi_po_danima[i] != None and max_redova > len(treninzi_po_danima[i]):
                for j in range(0, max_redova - len(treninzi_po_danima[i])):
                    treninzi_po_danima[i].append(None)

        treninzi_po_danima_inverz = list()

        for i in range(0, max_redova):
            treninzi_po_danima_inverz.append(list())
            for j in range(0, len(treninzi_po_danima)):
                treninzi_po_danima_inverz[i].append(treninzi_po_danima[j][i])

        

        for i in range(0, len(treninzi_po_danima_inverz)):
            for j in range(0, len(treninzi_po_danima_inverz[0])):
                if(treninzi_po_danima_inverz[i][j] != None):
                    treningFor : Trening = treninzi_po_danima_inverz[i][j]
                    stavkeFor = Stavka_Treninga.objects.filter(trening=treningFor).order_by("redniBroj")
                    treningIStavke = TreningIStavke(treningFor, stavkeFor)
                    treninzi_po_danima_inverz[i][j] = treningIStavke
        



    lista_labele = header_trener(2)

    #Chat deo
    razgovor:Razgovor = None
    razgovorId = -1
    razgovorKlijent: Razgovor = None
    razgovorKlijentId = -1
    if Razgovor.objects.filter(posiljalac_id = request.user.id, primalac_id = id).exists():
        razgovor = Razgovor.objects.get(posiljalac_id = request.user.id, primalac_id = id)
    else:
        razgovor = Razgovor()
        razgovor.posiljalac = klijent.mojTrener
        razgovor.primalac = klijent
        razgovor.save()
    razgovorId = razgovor.pk
    
    if Razgovor.objects.filter(posiljalac_id = id, primalac_id = request.user.id).exists():
        razgovorKlijent = Razgovor.objects.get(posiljalac_id = id, primalac_id = request.user.id)
        razgovorKlijentId = razgovorKlijent.pk
    
    poruke = Poruka.objects.filter(Q(razgovor_id = razgovorId) | Q(razgovor_id = razgovorKlijentId)).order_by("-datum")

    for poruka in poruke:
        if poruka.razgovor.pk == razgovorKlijentId:
            poruka.procitana = True
            poruka.save()
    

    #Plan ishrane jela
    postoji_plan_ishrane = False
    lista_stavki_po_danima_inverz = []
    plan_ishrane: Plan_Ishrane = None
    if Plan_Ishrane.objects.filter(korisnik_id = id).exists():
        postoji_plan_ishrane = True
        plan_ishrane= Plan_Ishrane.objects.get(korisnik_id = id)
        id_plan_ishrane = plan_ishrane.id

        stavke_ishrane = Stavka_Ishrane.objects.filter(planIshrane_id = plan_ishrane.id).order_by("vreme")

        lista_stavki_po_danima = [None, None, None, None, None, None, None]
        lista_br_stavki_po_danu = [0, 0, 0, 0, 0, 0, 0]

        for stavka_ishrane in stavke_ishrane:
            dan = stavka_ishrane.dan.weekday()
            if lista_stavki_po_danima[dan] == None:
                lista_stavki_po_danima[dan] = list()
            lista_stavki_po_danima[dan].append(stavka_ishrane)
            lista_br_stavki_po_danu[dan] += 1
        
        najveci_broj_linija: int = 0

        for i in range(0, len(lista_br_stavki_po_danu)):
            if najveci_broj_linija < lista_br_stavki_po_danu[i]:
                najveci_broj_linija = lista_br_stavki_po_danu[i]

        lista_stavki_po_danima_inverz = list()

        for i in range (0, najveci_broj_linija):
            lista_stavki_po_danima_inverz.append(list())
            #j: int = 0
            for j in range(0, 7):
                if lista_stavki_po_danima[j] == None or len(lista_stavki_po_danima[j]) <= i:
                    lista_stavki_po_danima_inverz[i].append(None)
                else:
                    lista_stavki_po_danima_inverz[i].append(lista_stavki_po_danima[j][i])

        #print(lista_stavki_po_danima_inverz)

    context = {
    'klijent':klijent, 
    'lista_labele': lista_labele,
    'treninzi_po_danima_inverz': treninzi_po_danima_inverz,
    'range': range(0, 7),
    'id_plan_treninga': id_plan_treninga,
    'poruke' : poruke,
    'razgovor': razgovor,
    'lista_stavki_po_danima_inverz': lista_stavki_po_danima_inverz,
    'id_plan_ishrane': id_plan_ishrane,
    'postoji_plan_treninga': postoji_plan_treninga,
    'postoji_plan_ishrane' : postoji_plan_ishrane,
    }
    return HttpResponse(template.render(context, request))


def trener_pregled_profila(request: HttpRequest):
    template = loader.get_template("trener\\trener_pregled_profil.html")
    lista_labele = header_trener(1)

    trener: Trener = Trener.objects.get(korisnik_ptr_id= request.user.id)

    context = {
        'lista_labele': lista_labele,
        'trener': trener,
    }

    return HttpResponse(template.render(context, request))


def trener_pregled_jela(request: HttpRequest):
    template = loader.get_template("trener\\trener_pregled_jela.html")

    formaTrenerPretraga = FormaTrenerPretraga(request.POST or None)
    if formaTrenerPretraga.is_valid():
        jela = Jelo.objects.filter(naziv__contains= formaTrenerPretraga.cleaned_data["tekst"])
    else:
        jela = Jelo.objects.all()

    lista_labele = header_trener(1)

    rows = trener_upakuj_jela_za_prikaz(jela)
    context = {
        'lista_labele': lista_labele,
        'forma_pretraga_jela': formaTrenerPretraga,
        'rows': rows,
    }

    return HttpResponse(template.render(context, request))




def trener_jelo_reg_test(request: HttpRequest):
    template = loader.get_template("trener\\forma_reg_jelo.html")
    if(request.method == "POST"):
        formaJeloRegistracija = FormaJeloRegistracija(request.POST, request.FILES)
    else:
        formaJeloRegistracija = FormaJeloRegistracija()
    if formaJeloRegistracija.is_valid():
        novoJelo = Jelo()
        novoJelo.naziv = formaJeloRegistracija.cleaned_data["naziv"]
        novoJelo.kalorije = formaJeloRegistracija.cleaned_data["kalorije"]
        novoJelo.priprema = formaJeloRegistracija.cleaned_data["priprema"]
        novoJelo.sastojci = formaJeloRegistracija.cleaned_data["sastojci"]
        novoJelo.slika = formaJeloRegistracija.cleaned_data["slika"]
        novoJelo.save()
        return redirect("trener_pregled_jela")
    context = {
        'formaJeloRegistracija':formaJeloRegistracija,
    }
    return HttpResponse(template.render(context, request))


def trener_pregled_jelo(request:HttpRequest, id):
    template =loader.get_template("trener\\trener_pregled_jelo.html")
    jelo = Jelo.objects.get(id=id)
    lista_labele = header_trener(2)
    context = {
        'jelo':jelo,
        'lista_labele':lista_labele,
    }
    return HttpResponse(template.render(context,request))


def trener_pregled_vezbi(request: HttpRequest):
    template = loader.get_template("trener\\trener_pregled_vezbi.html")

    formaTrenerPretraga = FormaTrenerPretraga(request.POST or None)

    if formaTrenerPretraga.is_valid():
        vezbe = Vezba.objects.filter(naziv__contains=formaTrenerPretraga.cleaned_data["tekst"])
    else:
        vezbe = Vezba.objects.all()

    lista_labele = header_trener(1)
    rows = trener_upakuj_vezbe_za_prikaz(vezbe)

    context = {
        'lista_labele':lista_labele,
        'forma_pretraga_vezbe': formaTrenerPretraga,
        'rows' : rows,
    }

    return HttpResponse(template.render(context, request))


def trener_vezba_reg_test(request: HttpRequest):
    template = loader.get_template("trener\\forma_reg_vezba.html")
    if(request.method == "POST"):
        formaVezbaRegistracija = FormaVezbaRegistracija(request.POST, request.FILES)
    else:
        formaVezbaRegistracija = FormaVezbaRegistracija()
    if formaVezbaRegistracija.is_valid():
        novaVezba = Vezba()
        novaVezba.naziv = formaVezbaRegistracija.cleaned_data["naziv"]
        novaVezba.misici = formaVezbaRegistracija.cleaned_data["misici"]
        novaVezba.opis = formaVezbaRegistracija.cleaned_data["opis"]
        novaVezba.tip = formaVezbaRegistracija.cleaned_data["tip"]
        novaVezba.slika = formaVezbaRegistracija.cleaned_data["slika"]
        novaVezba.sprava = None
        novaVezba.save()
        return redirect("trener_pregled_vezbi")
    context = {
        'formaVezbaRegistracija':formaVezbaRegistracija,
    }
    return HttpResponse(template.render(context, request))

def trener_pregled_vezbe(request: HttpRequest, id):
    template = loader.get_template("trener\\trener_pregled_vezbe.html")
    lista_labele = header_trener(2)
    vezba = Vezba.objects.get(id=id)
    context = {
        "lista_labele": lista_labele,
        "vezba": vezba,
    }
    return HttpResponse(template.render(context, request))


def trener_logout_req(request: HttpRequest):
    logout(request)
    return redirect('home')

def trener_plan_treninga_reg_test(request:HttpRequest):
    template = loader.get_template("trener\\forma_reg.html")
    formaPlanTreninga = FormaPlanTreninga(request.POST or None)
    if formaPlanTreninga.is_valid():
        formaPlanTreninga.save()
        return redirect("trener_pregled_klijenata")
    context = {
        "forma":formaPlanTreninga
    }

    return HttpResponse(template.render(context,request))

def trener_trening_reg_test(request:HttpRequest):
    template = loader.get_template("trener\\forma_reg.html")
    formaTrening = FormaTreningRegistracija(request.POST or None)
    if formaTrening.is_valid():
        trening = Trening()
        trening.planTreninga = Plan_Treninga.objects.get(id=1)
        trening.vreme = formaTrening.cleaned_data["vreme"]
        trening.dan = formaTrening.cleaned_data["dan"]
        trening.tip = formaTrening.cleaned_data["tip"]
        trening.save()
        return redirect("trener_pregled_klijenata")
    context = {
        "forma":formaTrening
    }

    return HttpResponse(template.render(context,request))

def trener_stavka_treninga_reg_test(request:HttpRequest):
    template = loader.get_template("trener\\forma_reg.html")
    formaStavkaTreninga = FormaStavkaTreningaRegistracija(request.POST or None)
    if formaStavkaTreninga.is_valid():
        formaStavkaTreninga.save()
        return redirect("trener_pregled_klijenata")
    context={
        'forma': formaStavkaTreninga,
    }

    return HttpResponse(template.render(context, request))


def trener_dodaj_trening(request: HttpRequest, dan:int, id_plan_treninga: int):

    plan_treninga = Plan_Treninga.objects.get(id=id_plan_treninga)
    idKlijenta =  plan_treninga.korisnik_id
    klijent: Klijent = Klijent.objects.get(korisnik_ptr_id = idKlijenta)
    if request.user.id != klijent.mojTrener.korisnik_ptr_id or dan >= 7 or dan < 0:
        return redirect("trener_pregled_klijenata")

    if(request.method == "POST"):
        trening: Trening = Trening()
        trening.planTreninga = plan_treninga
        trening.vreme = request.POST["vreme"]
        trening.tip = request.POST["tip"]
        datum = datetime.today()
        razlika = dan - datum.weekday()
        if razlika < 0:
            razlika += 7
        
        trening.dan = datum + datetime1.timedelta(days=razlika)

        trening.save()

        #return redirect("trener_izmeni_trening", trening_id= trening.id)
        return redirect("trener_pregled_klijenta", id=idKlijenta)
    else:
        template = loader.get_template("trener\\trener_dodaj_trening.html")
        lista_labele = header_trener(3)
        context = {
            "lista_labele": lista_labele,
        }
        return HttpResponse(template.render(context, request))


def trener_izmeni_trening(request: HttpRequest, trening_id: int):
    trening: Trening = Trening.objects.get(id=trening_id)
    klijent: Klijent = Klijent.objects.get(korisnik_ptr_id = trening.planTreninga.korisnik_id)
    if request.user.id != klijent.mojTrener.korisnik_ptr_id:
        return redirect("trener_pregled_klijenata")
    
    if request.method == "POST":
        brojPotencijalnihStavki = int(request.POST["brojStavki"])
        listaUzetihRednihBrojeva = list()
        listaIzmenjenih = list()
        listaIzbrisanih = list()
        #listaRednihBrojevaIzmenjenih = list() 
        vremeIzmeni = request.POST["vremePromena"]
        novoVreme = request.POST["vreme"]

        for i in range(1, brojPotencijalnihStavki + 1):
            print("POST: ", request.POST)
            if ("redniBroj-" + str(i)) in request.POST:
                trenutniRedniBroj = request.POST["redniBroj-" + str(i)]
                trenutniRedniBroj: int = int(trenutniRedniBroj)
                trenutniBrojPonavljanja: str = request.POST["brojPonavljanja-" + str(i)]
                trenutnaVezba: int = int(request.POST["stavka-vezbaId-" + str(i)])
                trenutnaTezina: str = request.POST["tezina-" + str(i)]
                trenutniIzmenjen: str = request.POST["promena-" + str(i)]
                listaUzetihRednihBrojeva.append(trenutniRedniBroj)
                if(trenutniIzmenjen != "false"):
                    objekatZaIzmenu: Stavka_Treninga = None
                    if(Stavka_Treninga.objects.filter(redniBroj= i, trening_id= trening.id).exists()):
                        objekatZaIzmenu = Stavka_Treninga.objects.get(redniBroj = i, trening_id= trening.id)
                    else:
                        objekatZaIzmenu = Stavka_Treninga()
                    
                    #listaRednihBrojevaIzmenjenih.append(trenutniRedniBroj)
                    objekatZaIzmenu.redniBroj = trenutniRedniBroj
                    objekatZaIzmenu.brojPonavljanja = trenutniBrojPonavljanja
                    objekatZaIzmenu.vezba = Vezba.objects.get(id= trenutnaVezba)
                    objekatZaIzmenu.tezina = trenutnaTezina
                    objekatZaIzmenu.trening = trening
                    listaIzmenjenih.append(objekatZaIzmenu)
            else:
                if Stavka_Treninga.objects.filter(redniBroj=i, trening_id= trening.id).exists():
                    listaIzbrisanih.append(Stavka_Treninga.objects.get(redniBroj=i, trening_id = trening.id))
        
        sveURedu = True
        redniBrojeviUzeti = list()
        for j in range (0, len(listaUzetihRednihBrojeva)):
            redniBrojeviUzeti.append(0)
        
        for j in range(0, len(listaUzetihRednihBrojeva)):
            if(listaUzetihRednihBrojeva[j] <= len(redniBrojeviUzeti) and listaUzetihRednihBrojeva[j] > 0 and redniBrojeviUzeti[listaUzetihRednihBrojeva[j] - 1] == 0):
                redniBrojeviUzeti[listaUzetihRednihBrojeva[j] - 1] += 1
            else:
                sveURedu = False

        if sveURedu:
            for i in range(0,len(listaIzmenjenih)):
                #listaIzmenjenih[i].redniBroj = listaRednihBrojevaIzmenjenih[i]
                listaIzmenjenih[i].save()
            for objekat in listaIzbrisanih:
                objekat.delete()
            if vremeIzmeni != "false":
                trening.vreme = novoVreme
                trening.save()
        
        return redirect("trener_pregled_klijenta", id= klijent.korisnik_ptr_id)




    else:
        stavke = Stavka_Treninga.objects.filter(trening_id=trening_id).order_by("redniBroj")



        template = loader.get_template("trener\\trener_izmeni_trening.html")

        vreme = trening.vreme
        hour = str(vreme.hour)
        minute = str(vreme.minute)
        if len(hour) == 1:
            hour = "0" + hour
        if len(minute) == 1:
            minute = "0" + minute

        vreme = hour + ":" + minute

        lista_labele = header_trener(2)

        context = {
            'lista_labele': lista_labele,
            'trening': trening,
            'stavke' : stavke,
            'vreme' : vreme,
            'broj_stavki': len(stavke),
        }
        return HttpResponse(template.render(context, request))


def trener_izmeni_trening_pretraga(request: HttpRequest, id_trening: int):

    if request.method == "POST":
        pretraga = request.POST["pretraga"]
        rezultat = list()
        if pretraga != "":
            vezbe = Vezba.objects.filter(naziv__icontains=pretraga)
            
            for vezba in vezbe:
                if vezba.slika != None:
                    data = {
                        'id': vezba.id,
                        'naziv': vezba.naziv,
                        'slika': str(vezba.slika),
                    }
                else:
                    data = {
                        'id': vezba.id,
                        'naziv': vezba.naziv,
                        'slika': "imgs/vezbe/vezbaBezSlike.png",
                    }


                rezultat.append(data)

        return JsonResponse(rezultat, safe=False)

    else:
        return HttpResponse("greska")


def trener_posalji_poruku(request: HttpRequest, id_klijenta: int):

    klijent: Klijent = Klijent.objects.get(korisnik_ptr_id= id_klijenta)

    if(request.user.id != klijent.mojTrener.korisnik_ptr_id):
        return HttpResponse("Invalid access")

    if request.method != "POST":
        return HttpResponse("Invalid method")

    if Razgovor.objects.filter(posiljalac_id = request.user.id, primalac_id = id_klijenta).exists():
        razgovor: Razgovor = Razgovor.objects.get(posiljalac_id = request.user.id, primalac_id = id_klijenta)
    
        poruka: Poruka = Poruka()

        poruka.razgovor = razgovor
        poruka.procitana = False
        poruka.redniBroj = Poruka.objects.filter(razgovor_id = razgovor.pk).count() + 1
        poruka.datum = datetime.now()
        poruka.tekst = request.POST["poruka"]
        listaPoruka: list = list()
        poruka.save()


        if Razgovor.objects.filter(primalac_id = request.user.id, posiljalac_id = id_klijenta).exists():
            razgovorKlijent: Razgovor = Razgovor.objects.get(primalac_id = request.user.id, posiljalac_id = id_klijenta)

            porukeKlijent = Poruka.objects.filter(razgovor_id = razgovorKlijent.pk, procitana = False).order_by("-datum")
            for porukaKlijent in porukeKlijent:
                porukaKlijent.procitana = True
                porukaKlijent.save()
                data = {
                    "tekst": porukaKlijent.tekst,
                    "tudja": 1,
                }
                listaPoruka.append(data)
        
        data = {
            "tekst": poruka.tekst,
            "tudja": 0,
        }

        listaPoruka.append(data)

        return JsonResponse(listaPoruka, safe=False)
    else:
        return HttpResponse("Razgovor ne postoji!")

def trener_osvezi_chat(request: HttpRequest, id_klijenta: int):
    klijent: Klijent = Klijent.objects.get(korisnik_ptr_id= id_klijenta)

    if(request.user.id != klijent.mojTrener.korisnik_ptr_id):
        return HttpResponse("Invalid access")

    if request.method != "POST":
        return HttpResponse("Invalid method")

    listaPoruka = list()

    if Razgovor.objects.filter(primalac_id = request.user.id, posiljalac_id = id_klijenta).exists():
        razgovorKlijent: Razgovor = Razgovor.objects.get(primalac_id = request.user.id, posiljalac_id = id_klijenta)

        porukeKlijent = Poruka.objects.filter(razgovor_id = razgovorKlijent.pk, procitana = False).order_by("-datum")
        for porukaKlijent in porukeKlijent:
            porukaKlijent.procitana = True
            porukaKlijent.save()
            data = {
                "tekst": porukaKlijent.tekst,
                "tudja": 1,
            }
            listaPoruka.append(data)
    
    return JsonResponse(listaPoruka, safe=False)


def trener_izbrisi_trening(request: HttpRequest, id_klijenta: int):
    klijent: Klijent = Klijent.objects.get(korisnik_ptr_id= id_klijenta)

    if(request.user.id != klijent.mojTrener.korisnik_ptr_id):
        return HttpResponse("Invalid access")

    if request.method != "POST":
        return HttpResponse("Invalid method")

    id_treninga = request.POST["id_treninga"]
    
    trening: Trening = Trening.objects.get(id=id_treninga)
    if trening.planTreninga.korisnik.id != klijent.korisnik_ptr_id:
        return HttpResponse("Nije to klijentov trening")

    trening.delete()

    return HttpResponse("Success!")

def trener_izmeni_obrok(request: HttpRequest, id_stavka_ishrane: int):

    stavka_ishrane: Stavka_Ishrane = Stavka_Ishrane.objects.get(id=id_stavka_ishrane)

    plan_ishrane: Plan_Ishrane = stavka_ishrane.planIshrane

    klijent: Klijent = Klijent.objects.get(korisnik_ptr_id = plan_ishrane.korisnik.id)

    if klijent.mojTrener.korisnik_ptr_id != request.user.id:
        return HttpResponse("Dati trener nije ovlascen za promenu ovog obroka")

    if request.method == "POST":
        idNovogJela: int = int(request.POST["id-stavka"])
        stavka_ishrane.jelo = Jelo.objects.get(id=idNovogJela)
        stavka_ishrane.kolicina = int(request.POST["kolicina"])
        stavka_ishrane.vreme =  request.POST["vreme"]
        stavka_ishrane.save() 
        return redirect("trener_pregled_klijenta", klijent.korisnik_ptr_id)
    else:
        template = loader.get_template("trener\\trener_izmeni_obrok.html")

        vreme = stavka_ishrane.vreme
        hour = str(vreme.hour)
        minute = str(vreme.minute)
        if len(hour) == 1:
            hour = "0" + hour
        if len(minute) == 1:
            minute = "0" + minute

        vreme = hour + ":" + minute

        lista_labele = header_trener(2)
        context ={
            "lista_labele":lista_labele,
            "stavka_ishrane": stavka_ishrane,
            "vreme": vreme,
        }

        return HttpResponse(template.render(context, request))


def trener_izmeni_obrok_pretraga(request: HttpRequest, id_stavka_ishrane: int):

    if request.method != "POST":
        return HttpResponse("Invalid method!")
    
    tekst = request.POST["tekst"]

    jela = Jelo.objects.filter(naziv__contains=tekst)

    lista_jela = list()

    for jelo in jela:
        if jelo.slika != None:
            data ={
                'naziv': jelo.naziv,
                'id': jelo.id,
                'slika': str(jelo.slika),
            }
        else:
            data ={
                'naziv': jelo.naziv,
                'id': jelo.id,
                'slika': "imgs/jela/jeloBezSlike.jpg",
            }
        lista_jela.append(data)
    

    return JsonResponse(lista_jela, safe=False)

def trener_dodaj_obrok(request: HttpRequest, dan: int, id_plan_ishrane):

    plan_ishrane: Plan_Ishrane = Plan_Ishrane.objects.get(id=id_plan_ishrane)

    klijent: Klijent = Klijent.objects.get(korisnik_ptr_id=plan_ishrane.korisnik.id)

    if klijent.mojTrener.korisnik_ptr_id != request.user.id:
        return HttpResponse("Klijent sa datim planom ishrane nije Vas!")
    
    if request.method != "POST":
        return HttpResponse("Invalid method!")

    stavka_ishrane = Stavka_Ishrane()
    stavka_ishrane.vreme = datetime1.time(0,0,0)
    stavka_ishrane.kolicina = 0
    datum = datetime.today()
    razlika = dan - datum.weekday()
    if razlika < 0:
        razlika += 7
    
    stavka_ishrane.dan = datum + datetime1.timedelta(days=razlika)
    stavka_ishrane.jelo = Jelo.objects.all().first()
    stavka_ishrane.planIshrane = plan_ishrane
    stavka_ishrane.save()
    id: int = stavka_ishrane.id

    return redirect("trener_izmeni_obrok", id)


def trener_izbrisi_obrok(request: HttpRequest, id_klijenta: int):

    klijent: Klijent = Klijent.objects.get(korisnik_ptr_id=id_klijenta)

    if request.user.id != klijent.mojTrener.korisnik_ptr_id:
        return HttpResponse("Nije tvoj klijent!")
    if request.method != "POST":
        return HttpResponse("Invalid method!")
    
    id_obrok = request.POST["id_obrok"]

    stavka_ishrane: Stavka_Ishrane = Stavka_Ishrane.objects.get(id= id_obrok)
    if stavka_ishrane.planIshrane.korisnik.id != klijent.korisnik_ptr_id:
        return HttpResponse("Nije klijentov plan ishrane!")
    
    stavka_ishrane.delete()

    return HttpResponse("Success!")