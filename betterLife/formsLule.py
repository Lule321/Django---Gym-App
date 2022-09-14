from datetime import datetime
from .models import Klijent, Trening, Plan_Treninga, Stavka_Treninga
from django import forms

class FormaKlijentRegistracija(forms.Form):
    username = forms.CharField(max_length=60)
    password = forms.CharField(max_length = 60)
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)
    email = forms.EmailField(max_length=60)
    date_joined = forms.DateTimeField(initial=datetime.today)
    gender = forms.CharField(max_length=1)
    broj_clanske_karte = forms.IntegerField(min_value=0)
    datum_poslednje_uplate = forms.DateField(initial=datetime.today)
    slika = forms.ImageField()

class FormaJeloRegistracija(forms.Form):
    naziv = forms.CharField(max_length=60)
    kalorije = forms.IntegerField(min_value=0)
    sastojci = forms.CharField(widget=forms.Textarea)
    priprema = forms.CharField(widget=forms.Textarea)
    slika = forms.ImageField()

class FormaVezbaRegistracija(forms.Form):
    naziv = forms.CharField(max_length=60)
    opis = forms.CharField(widget=forms.Textarea)
    tip = forms.CharField(max_length=60)
    misici = forms.CharField(widget=forms.Textarea)
    slika = forms.ImageField()
    
class FormaTrenerPretraga(forms.Form):
    
    tekst = forms.CharField(max_length=60, required=False)


class FormaTreningRegistracija(forms.Form):
    tip = forms.CharField(max_length=60)
    dan = forms.DateField(initial=datetime.today)
    vreme = forms.TimeField(initial=datetime.now)
class FormaStavkaTreningaRegistracija(forms.ModelForm):
    class Meta:
        model = Stavka_Treninga
        fields = "__all__"

class FormaPlanTreninga(forms.ModelForm):
    class Meta:
        model = Plan_Treninga
        fields = "__all__"