from datetime import date, datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


"""role"""
class Korisnik(AbstractUser):
    gender = models.CharField(max_length=1)
    slika = models.ImageField(upload_to="imgs/korisnici", null=True)
    class Meta:
        db_table = "Korisnik"
        permissions = (
            ("trener", "treneru omogucava njegove funkcionalnosti"),
        )

class Trener(Korisnik):
    radnoVreme = models.CharField(null=True, max_length=30)
    class Meta:
        db_table = "Trener"
    def __str__(self):
        return f"IME: {self.username}  EMAIL: {self.email}"

class Klijent(Korisnik):
    #brojClanskeKarte = models.IntegerField(unique=True)
    pretplata = models.CharField(max_length=30)
    visina = models.IntegerField(null=True)
    tezina = models.IntegerField(null=True)
    godine = models.IntegerField(null=True)
    datumPoslednjeUplate = models.DateField(default=timezone.now)
    mojTrener = models.ForeignKey(Trener, on_delete=models.CASCADE, null=True) # stavio sam null na true za sad
    
    class Meta:
        db_table = "Klijent"


"""komunikacija"""

class Razgovor(models.Model):
    posiljalac = models.ForeignKey(Korisnik, on_delete=models.CASCADE, related_name="posiljalac")
    primalac = models.ForeignKey(Korisnik, on_delete=models.CASCADE, related_name="primalac")
    class Meta:
        db_table = "Razgovor"

class Poruka(models.Model):
    redniBroj = models.IntegerField(default=1)
    tekst = models.CharField(max_length=256, blank=True)
    razgovor = models.ForeignKey(Razgovor, on_delete=models.CASCADE, null=False)
    procitana = models.BooleanField(default=True)
    datum = models.DateTimeField(default= timezone.now)
    class Meta:
        db_table = "Poruka"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        ret = super(Poruka, self).save()
        poruke = Poruka.objects.filter(razgovor=self.razgovor)
        poruke = poruke.order_by("redniBroj")
        #self.redniBroj = poruke.last().redniBroj + 1
        return ret

class Pitanje(models.Model):
    tekst = models.CharField(max_length=256, blank=True)
    class Meta:
        db_table = "Pitanje"

class Odgovor(models.Model):
    korisnik = models.ForeignKey(Korisnik, on_delete=models.CASCADE)
    pitanje = models.ForeignKey(Pitanje, on_delete=models.CASCADE)
    tekst = models.CharField(max_length=256, blank=True)
    class Meta:
        db_table = "Odgovor"

"""ishrana"""
class Plan_Ishrane(models.Model):
    korisnik = models.ForeignKey(Korisnik, on_delete=models.CASCADE)
    class Meta:
        db_table = "Plan_Ishrane"

class Jelo(models.Model):
    naziv = models.CharField(max_length=30)
    kalorije = models.IntegerField()
    sastojci = models.CharField(max_length=256)
    priprema = models.CharField(max_length=512)
    slika = models.ImageField(upload_to="imgs/jela", null=True)
    class Meta:
        db_table = "Jelo"

class Stavka_Ishrane(models.Model):
    planIshrane = models.ForeignKey(Plan_Ishrane, on_delete=models.CASCADE)
    jelo = models.ForeignKey(Jelo, on_delete=models.CASCADE)
    kolicina = models.IntegerField()
    dan = models.DateField()
    vreme = models.TimeField()
    class Meta:
        db_table = "Stavka_Ishrane"

"""trening"""
class Sprava(models.Model):
    naziv = models.CharField(max_length=30)
    opis = models.CharField(max_length=256, null=True)
    stanje = models.BooleanField(default=True)
    datumNabavke = models.DateField()
    kolicina = models.IntegerField()
    slika = models.ImageField(upload_to="imgs/inventar", null=True)
    class Meta:
        db_table = "Sprava"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.datumNabavke == None:
            self.datumNabavke = timezone.now()
        return super(Sprava, self).save()

class Vezba(models.Model):
    naziv = models.CharField(max_length=30)
    opis = models.CharField(max_length=256, null=True)
    tip = models.CharField(max_length=30, null=True)
    misici = models.CharField(max_length=64)
    sprava = models.ForeignKey(Sprava, on_delete=models.CASCADE, null=True, blank=True)
    slika = models.ImageField(upload_to="imgs/vezbe", null=True)
    class Meta:
        db_table = "Vezba"

class Plan_Treninga(models.Model):
    korisnik = models.ForeignKey(Korisnik, on_delete=models.CASCADE)
    class Meta:
        db_table = "Plan_Treninga"

class Trening(models.Model):
    planTreninga = models.ForeignKey(Plan_Treninga, on_delete=models.CASCADE)
    tip = models.CharField(max_length=30, null=True) 
    dan = models.DateField(null=True)
    vreme = models.TimeField(null=True)
    #aktivan = models.BooleanField(default=False)
    def __str__(self):
        ret = str(self.dan.weekday())
        stavke = Stavka_Treninga.objects.filter(trening = self)
        for stavka in stavke:
            ret += "\n" + stavka.vezba.naziv
        ret += "\n"
        return ret
    class Meta:
        db_table = "Trening"


class Stavka_Treninga(models.Model):
    redniBroj = models.IntegerField(default=0)
    brojPonavljanja = models.CharField(max_length = 50) #izmenio u charField da bi se lakse napisalo
    tezina = models.CharField(max_length = 50) #izmenio u charField da bi se lakse napisalo
    trening = models.ForeignKey(Trening, on_delete=models.CASCADE)
    vezba = models.ForeignKey(Vezba, on_delete=models.CASCADE)
    def __str__(self):
        return "{0} - {1} - tezina: {2}".format(self.brojPonavljanja, self.vezba.naziv, self.tezina)
    class Meta:
        db_table = "Stavka_Treninga"