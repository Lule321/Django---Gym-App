from django.contrib.admin.views.decorators import staff_member_required
from email import header
#import this
from django import views
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ImageField
from django.http import HttpRequest, HttpResponse
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



# da bih sve svoje stavio na jedno mesto
from . import viewsLule

"""Admin"""
def admin_logout(request):
    logout(request)
    return redirect("../")

def admin_index(request: HttpRequest):
    context = {
        "name": request.user.username
    }
    return render(request, "administrator/admin_index.html", context)

"""Inventar (rekviziti)"""
def sprava(request, sprava_id):
    sprava = Sprava.objects.get(pk=sprava_id)

    context = {
        "sprava": sprava
    }
    return render(request, "administrator/sprava.html", context)

def sprava_change(request, sprava_id):
    sprava = Sprava.objects.get(pk=sprava_id)
    form = AddInventoryForm(data=request.POST or None, files=request.FILES, instance=sprava)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("admin_sprava", sprava_id=sprava.id)

    context = {
        "form" : form,
        "sprava": sprava
    }
    return render(request, "administrator/sprava_change.html", context)

def sprava_delete(request):
    sprava_id = request.POST.get("sprava_id")
    if sprava_id:
        sprava = Sprava.objects.get(pk=sprava_id)
        if request.user.is_superuser:
            sprava.delete()
    return redirect("admin_inventory_view")


def inventory_view(request):
    form = SearchForm(request.POST or None)

    inventory = []
    if request.method == "POST":
        if form.is_valid():
            keyword = form.cleaned_data.get("keyword")
            inventory = Sprava.objects.filter(Q(naziv__icontains=keyword) | Q(opis__icontains=keyword))
        else:
            inventory = Sprava.objects.order_by("naziv")

    elif request.method == "GET":
        inventory = Sprava.objects.order_by("naziv")

    slike = []
    for sprava in inventory:
        if sprava.slika != None:
            polje = SlikaPolje(sprava.naziv, "../sprava/" + str(sprava.id), sprava.slika.url)
            slike.append(polje)
    rows = []
    row = []
    for i in range(len(slike)):
        row.append(slike[i])
        if (i % 6 == 5 or i == len(slike) - 1):
            rows.append(row)
            row = []

    nav1 = LinkPolje("Main", "../")
    nav2 = LinkPolje("Klijent", "https://docs.python.org/3/library/venv.html")
    nav3 = LinkPolje("Izloguj se", "#")
    lista_labele = [nav1, nav2, nav3]

    context = {
        "form": form,
        'lista_labele': lista_labele,
        'rows': rows
    }
    return render(request, "administrator/inventory_view.html", context)

def inventory_add(request):
        if(request.user.is_superuser):
            form = AddInventoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect("admin_inventory_view")

            context = {
                "form": form
            }
            return render(request, "administrator/inventory_add.html", context)
        else:
            return redirect("home")

"""Jela"""
def jelo(request, jelo_id):
    jelo = Jelo.objects.get(pk=jelo_id)

    context = {
        "jelo": jelo
    }
    return render(request, "administrator/jelo.html", context)

def jelo_change(request, jelo_id):
    jelo = Jelo.objects.get(pk=jelo_id)
    form = AddMealForm(data=request.POST or None, files=request.FILES, instance=jelo)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("admin_jelo", jelo_id=jelo.id)

    context = {
        "form" : form,
        "jelo": jelo
    }
    return render(request, "administrator/jelo_change.html", context)

def jelo_delete(request):
    jelo_id = request.POST.get("jelo_id")
    if jelo_id:
        jelo = Jelo.objects.get(pk=jelo_id)
        #if request.user.is_superuser:
        jelo.delete()
    return redirect("admin_meals_view")

def meals_view(request):
    form = SearchForm(request.POST or None)

    jela = []
    if request.method == "POST":
        if form.is_valid():
            keyword = form.cleaned_data.get("keyword")
            jela = Jelo.objects.filter(Q(naziv__icontains=keyword) | Q(priprema__icontains=keyword) | Q(sastojci__icontains=keyword))
        else:
            jela = Jelo.objects.order_by("naziv")

    elif request.method == "GET":
        jela = Jelo.objects.order_by("naziv")

    slike = []
    for jelo in jela:
        if jelo.slika != None:
            polje = SlikaPolje(jelo.naziv, "../jelo/" + str(jelo.id), jelo.slika.url)
            slike.append(polje)
    rows = []
    row = []
    for i in range(len(slike)):
        row.append(slike[i])
        if (i % 3 == 2 or i == len(slike) - 1):
            rows.append(row)
            row = []

    nav1 = LinkPolje("Main", "../")
    nav2 = LinkPolje("Klijent", "https://docs.python.org/3/library/venv.html")
    nav3 = LinkPolje("Izloguj se", "#")
    lista_labele = [nav1, nav2, nav3]

    context = {
        "form": form,
        'lista_labele': lista_labele,
        'rows': rows
    }
    return render(request, "administrator/meals_view.html", context)

def meal_add(request):
    if True:  # if(request.user.is_superuser):
        form = AddMealForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_meals_view")

        context = {
            "form": form
        }
        return render(request, "administrator/meal_add.html", context)
    else:
        return redirect("home")

"""Klijenti"""
def clients_view(request):
    form = SearchForm(request.POST or None)

    klijenti = []
    if request.method == "POST":
        if form.is_valid():
            keyword = form.cleaned_data.get("keyword")
            klijenti = Klijent.objects.filter(Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(email__icontains=keyword))
        else:
            klijenti = Klijent.objects.order_by("last_name")

    elif request.method == "GET":
        klijenti = Klijent.objects.order_by("last_name")

    slike = []
    for klijent in klijenti:
        if klijent.slika != "" and klijent.slika != None:
            polje = SlikaPolje(klijent.first_name + " " + klijent.last_name, "../client/" + str(klijent.id), klijent.slika.url)
            slike.append(polje)
    rows = []
    row = []
    for i in range(len(slike)):
        row.append(slike[i])
        if (i % 3 == 2 or i == len(slike) - 1):
            rows.append(row)
            row = []

    nav1 = LinkPolje("Main", "../")
    nav2 = LinkPolje("Klijent", "https://docs.python.org/3/library/venv.html")
    nav3 = LinkPolje("Izloguj se", "#")
    lista_labele = [nav1, nav2, nav3]

    context = {
        "form": form,
        'lista_labele': lista_labele,
        'rows': rows
    }
    return render(request, "administrator/clients_view.html", context)

def admin_client(request, client_id):
    klijent = Klijent.objects.get(pk=client_id)

    context = {
        "klijent": klijent
    }
    return render(request, "administrator/client.html", context)

def client_change(request, client_id):
    klijent = Klijent.objects.get(pk=client_id)
    form = ChangeUserForm(data=request.POST or None, files=request.FILES, instance=klijent)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("admin_client", client_id=klijent.id)

    context = {
        "form": form,
        "klijent": klijent
    }
    return render(request, "administrator/client_change.html", context)

def client_remove(request):
    client_id = request.POST.get("client_id")
    if client_id:
        klijent = Klijent.objects.get(pk=client_id)
        #if request.user.is_superuser:
        klijent.delete()
    return redirect("admin_clients_view")

"""Treneri"""
def trainers_view(request):
    form = SearchForm(request.POST or None)

    treneri = []
    if request.method == "POST":
        if form.is_valid():
            keyword = form.cleaned_data.get("keyword")
            treneri = Trener.objects.filter(
                Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword) | Q(email__icontains=keyword))
        else:
            treneri = Trener.objects.order_by("last_name")

    elif request.method == "GET":
        treneri = Trener.objects.order_by("last_name")

    slike = []
    for trener in treneri:
        if trener.slika != "" and trener.slika != None:
            polje = SlikaPolje(trener.first_name + " " + trener.last_name, "../trainer/" + str(trener.id),
                               trener.slika.url)
            slike.append(polje)
    rows = []
    row = []
    for i in range(len(slike)):
        row.append(slike[i])
        if (i % 3 == 2 or i == len(slike) - 1):
            rows.append(row)
            row = []

    nav1 = LinkPolje("Main", "../")
    nav2 = LinkPolje("Klijent", "https://docs.python.org/3/library/venv.html")
    nav3 = LinkPolje("Izloguj se", "#")
    lista_labele = [nav1, nav2, nav3]

    context = {
        "form": form,
        'lista_labele': lista_labele,
        'rows': rows
    }
    return render(request, "administrator/trainers_view.html", context)

def admin_trainer(request, trainer_id):
    trener = Trener.objects.get(pk=trainer_id)
    context = {
        "trener": trener
    }
    return render(request, "administrator/trainer.html", context)

def trainer_verify(request):
    trener_id = request.POST.get("trener_id")
    if trener_id:
        trener = Trener.objects.get(pk=trener_id)
        # if request.user.is_superuser:
        trener.verifikovan = True;
        trener.save()
    return redirect("admin_trainers_view")

def trainer_remove(request):
    trener_id = request.POST.get("trener_id")
    if trener_id:
        trener = Trener.objects.get(pk=trener_id)
        # if request.user.is_superuser:
        trener.delete()
    return redirect("admin_trainers_view")

def test_image_table(request):
    nav1 = LinkPolje("Trener", "https://www.w3schools.com/python/python_classes.asp")
    nav2 = LinkPolje("Klijent", "https://docs.python.org/3/library/venv.html")
    nav3 = LinkPolje("Izloguj se", "#")
    lista_labele = [nav1, nav2, nav3]
    #slike = (SlikaPolje(sprava.naziv, "https://google.com", sprava.slika) for sprava in Sprava.objects.all())
    slike = []
    for sprava in Sprava.objects.all():
        if sprava.slika != None:
            #slike.append(sprava)
            polje = SlikaPolje(sprava.naziv, "https://www.google.com", sprava.slika.url)
            slike.append(polje)
    rows = []
    row = []
    for i in range(len(slike)):
        row.append(slike[i])
        if(i%3 == 2 or i == len(slike)-1):
            rows.append(row)
            row = []
    form = SearchForm(request.POST)
    context = {
        "form": form,
        'lista_labele': lista_labele,
        'rows': rows
    }
    return render(request, "table_views/images_table_base.html", context)
    nav1 = LinkPolje("Trener", "https://www.w3schools.com/python/python_classes.asp")
    nav2 = LinkPolje("Klijent", "https://docs.python.org/3/library/venv.html")
    nav3 = LinkPolje("Izloguj se", "#")
    lista_labele = [nav1, nav2, nav3]
    #slike = (SlikaPolje(sprava.naziv, "https://google.com", sprava.slika) for sprava in Sprava.objects.all())
    slike = []
    for sprava in Sprava.objects.all():
        if sprava.slika != None:
            #slike.append(sprava)
            polje = SlikaPolje(sprava.naziv, "https://www.google.com", sprava.slika.url)
            slike.append(polje)
    rows = []
    row = []
    for i in range(len(slike)):
        row.append(slike[i])
        if(i%3 == 2 or i == len(slike)-1):
            rows.append(row)
            row = []
    form = SearchForm(request.POST)
    context = {
        "form": form,
        'lista_labele': lista_labele,
        'rows': rows
    }
    return render(request, "table_views/images_table_base.html", context)

"""Panta gost"""

def registerT(request):

    form = TrenerForm(data=request.POST or None, files = request.FILES or None)
    #print(form.errors)
    if form.is_valid():
        user:Trener = form.save()
        
        permission = Permission.objects.get(name="treneru omogucava njegove funkcionalnosti")
        user.user_permissions.add(permission)
        user.save()
        #login(request, user)
        return redirect('home') #stavio sam da mi udje na pocetnu
    context = {
        'form': form,
        'errors': form.errors.as_text()
    }
    return render(request, 'Gost/registerT.html', context)

def registerK(request):

    form = None
    if request.method == "POST":
        form = KlijentForm(request.POST, request.FILES)
        #print(request.FILES)
    else:
        form = KlijentForm()
    #print(form.errors)
    #print(form.errors.as_data())
    #print(form.errors.as_text())
    if form.is_valid():
        #print("ovde1")
        user: Klijent = form.save()
        #user.save()

        if  "trening" in user.pretplata:
            plan_treninga: Plan_Treninga = Plan_Treninga()
            plan_treninga.korisnik = user
            plan_treninga.save()

        if "ishrana" in user.pretplata:
            plan_ishrane: Plan_Ishrane = Plan_Ishrane()
            plan_ishrane.korisnik = user
            plan_ishrane.save()
        
        #user = form.save()
        #login(request, user)
        return redirect('home') #stavio sam da mi udje na pocetnu
    context = {
        'form': form,
        'errors': form.errors.as_text()
    }
    return render(request, 'Gost/registerK.html', context)

def home(request: HttpRequest):
    form = AuthenticationForm(request=request, data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("pocetna")
    context = {
        'form': form
    }
    return render(request, 'Gost/home.html', context)

def logout_req(request: HttpRequest):
    logout(request)
    return redirect('home')

def treneriP(request):
    treneri= Trener.objects.all()
    template = loader.get_template('Gost/treneriP.html')
    context = {
        'treneri': treneri
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url='home')
def pocetna(requset: HttpRequest):
    if requset.user.is_superuser:
        return redirect('admin_index')
    if requset.user.has_perm("betterLife.trener"):
       return redirect("trener_pregled_klijenata")
    if not requset.user.is_anonymous:
        return redirect("klijent_profil")
    return render(requset, 'Klijent/pocetna.html')


def pitanja(request):
    pitanja = Pitanje.objects.all()
    context = {
        'pitanja': pitanja
    }
    return render(request, 'Gost/pitanja.html', context)

def treninziP(requset: HttpRequest):
    return render(requset, 'Gost/treninziP.html')

def treninziPK(requset: HttpRequest):

    return render(requset, 'Klijent/treninziPK.html')


def Onama(requset: HttpRequest):
    return render(requset, 'Gost/Onama.html')

def Usluge(requset: HttpRequest):
    return render(requset, 'Gost/Usluge.html')

#def pitanja(requset: HttpRequest):
#    return render(requset, 'Gost/pitanja.html')

class MyPasswordCganheView(PasswordChangeView):
    template_name = 'password-change.html'
    success_url = reverse_lazy('users:password-change-done-view')

class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset-done.html'
"""Kraj Panta"""

"""Cakara"""

def KlijentPlanIshrane(request: HttpRequest):

    context = {

    }
    return render(request, "Klijent\PlanIshrane.html", context)

def KlijentGrupniTreninzi(request: HttpRequest):

    context = {

    }
    return render(request, "Klijent\GrupniTreninzi.html", context)

def KlijentTrener(request: HttpRequest):
    IDKlijent = request.user.id
    #IDKlijent = 4
    KlijentMoj = Klijent.objects.get(id=IDKlijent)
    MojTrener = KlijentMoj.mojTrener
    print(MojTrener.first_name)
    context = {
        'trener': MojTrener
    }
    return render(request, "Klijent\Trener.html", context)

def KlijentProfil(request: HttpRequest):
    context = {

    }
    return render(request, "Klijent\PregledProfila.html", context)

def KlijentTreningPlan(request: HttpRequest):
    IDKlijent = request.user.id
    #IDKlijent = 4
    KlijentMoj = Klijent.objects.get(id=IDKlijent)
    TreningPlan = Plan_Treninga.objects.get(korisnik=KlijentMoj)
    Treninzi = Trening.objects.filter(planTreninga=TreningPlan)
    Vezbe = [[], [], [], [], [], [], []]
    treninzi = [[], [], [], [], [], [], []]
    dani = ["Ponedeljak", "Utorak", "Sreda", "Četvrtak", "Petak", "Subota", "Nedelja"]
    max_treninga = 0;
    for trening in Treninzi:
        dan = trening.dan.weekday()
        Vezbe[dan].append(Stavka_Treninga.objects.filter(trening=trening))
        treninzi[dan].append(trening)
        newmax = len(treninzi[dan])
        if newmax > max_treninga:
            max_treninga = newmax

    for i in range(7):
        while i < len(treninzi) and len(treninzi[i]) == 0:
            treninzi.pop(i)
            Vezbe.pop(i)
            dani.pop(i)
        while i < len(treninzi) and len(treninzi[i]) < max_treninga:
            treninzi[i].append(None)
            Vezbe[i].append(None)
    trevez = []
    for i in range(len(treninzi)):
        trevez.append(zip(treninzi[i], Vezbe[i]))

    context = {
        'vezbe': Vezbe,
        'treningPlan': TreningPlan,
        'treninzi': treninzi,
        'dani': dani,
        'max_dan': range(max_treninga),
        'b_dana': range(7),
        'treninzi_vezbe': zip(trevez, dani)

    }
    return render(request, "Klijent\TreningPlan.html", context)

def KlijentIzmenaPlana(request: HttpRequest):

    context = {

    }
    return render(request, "Klijent\IzmenaPlana.html", context)


"""Kraj Cakara"""


"""Lule"""
def test_table_view(request: HttpRequest):
    return viewsLule.test_table_view(request);


"""Lule-trener pogled"""
@permission_required("betterLife.trener")
def trener_pregled_klijenata(request: HttpRequest):
    return viewsLule.trener_pregled_klijenata(request)

@permission_required("betterLife.trener")
def trener_klijenti_reg_test(request:HttpRequest):
    return viewsLule.trener_klijenti_reg_test(request)

@permission_required("betterLife.trener")
def trener_pregled_klijenta(request: HttpRequest, id):
    return viewsLule.trener_pregled_klijenta(request, id)

@permission_required("betterLife.trener")
def trener_pregled_profila(request: HttpRequest):
    return viewsLule.trener_pregled_profila(request)

@permission_required("betterLife.trener")
def trener_pregled_jela(request: HttpRequest):
    return viewsLule.trener_pregled_jela(request)

@permission_required("betterLife.trener")
def trener_jelo_reg_test(request: HttpRequest):
    return viewsLule.trener_jelo_reg_test(request)

@permission_required("betterLife.trener")
def trener_pregled_jelo(request:HttpRequest, id):
    return viewsLule.trener_pregled_jelo(request, id)

@permission_required("betterLife.trener")
def trener_pregled_vezbi(request: HttpRequest):
    return viewsLule.trener_pregled_vezbi(request)

@permission_required("betterLife.trener")
def trener_vezba_reg_test(request: HttpRequest):
    return viewsLule.trener_vezba_reg_test(request)

@permission_required("betterLife.trener")
def trener_pregled_vezbe(request: HttpRequest, id):
    return viewsLule.trener_pregled_vezbe(request, id)

@permission_required("betterLife.trener")
def trener_logout_req(request: HttpRequest):
    logout(request)
    return redirect('home')

@permission_required("betterLife.trener")
def trener_plan_treninga_reg_test(request:HttpRequest):

    return viewsLule.trener_plan_treninga_reg_test(request)

@permission_required("betterLife.trener")
def trener_trening_reg_test(request:HttpRequest):
    return viewsLule.trener_trening_reg_test(request)

@permission_required("betterLife.trener")
def trener_stavka_treninga_reg_test(request:HttpRequest):
    return viewsLule.trener_stavka_treninga_reg_test(request)
"""Kraj Lule"""

@permission_required("betterLife.trener")
def trener_dodaj_trening(request: HttpRequest, dan:int, id_plan_treninga: int):
    return viewsLule.trener_dodaj_trening(request, dan, id_plan_treninga)

@permission_required("betterLife.trener")
def trener_izmeni_trening(request: HttpRequest, id_trening: int):
    return viewsLule.trener_izmeni_trening(request, id_trening)

@permission_required("betterLife.trener")
def trener_izmeni_trening_pretraga(request: HttpRequest, id_trening: int):
    return viewsLule.trener_izmeni_trening_pretraga(request, id_trening)

@permission_required("betterLife.trener")
def trener_posalji_poruku(request: HttpRequest, id_klijenta: int):
    return viewsLule.trener_posalji_poruku(request, id_klijenta)


@permission_required("betterLife.trener")
def trener_izbrisi_trening(request: HttpRequest, id_klijenta: int):
    return viewsLule.trener_izbrisi_trening(request, id_klijenta)

@permission_required("betterLife.trener")
def trener_osvezi_chat(request: HttpRequest, id_klijenta: int):
    return viewsLule.trener_osvezi_chat(request, id_klijenta)

@permission_required("betterLife.trener")
def trener_izmeni_obrok(request: HttpRequest, id_stavka_ishrane: int):
    return viewsLule.trener_izmeni_obrok(request, id_stavka_ishrane)

@permission_required("betterLife.trener")
def trener_izmeni_obrok_pretraga(request: HttpRequest, id_stavka_ishrane: int):
    return viewsLule.trener_izmeni_obrok_pretraga(request, id_stavka_ishrane)

@permission_required("betterLife.trener")
def trener_dodaj_obrok(request: HttpRequest, dan: int, id_plan_ishrane: int):
    return viewsLule.trener_dodaj_obrok(request, dan, id_plan_ishrane)

@permission_required("betterLife.trener")
def trener_izbrisi_obrok(request: HttpRequest, id_klijenta: int):
    return viewsLule.trener_izbrisi_obrok(request, id_klijenta)