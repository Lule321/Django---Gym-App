from urllib import response
from django.http import HttpResponse
from django.test import TestCase, Client
from .models import Klijent, Korisnik, Plan_Ishrane, Plan_Treninga, Trener

# Create your tests here.

class GostTestLule(TestCase):
    
    def test_klijent_register_get(self):
        c: Client = Client()
        response: HttpResponse = c.get('/registerK/')
        flag: bool = "REGISTRACIJA KLIJENT" in str(response.content)
        self.assertTrue(flag)
        flag: bool = "Visina" in str(response.content)
        self.assertTrue(flag)

        flag: bool = "<input type=\"file\" name=\"slika\" accept=\"image/*\" id=\"id_slika\">" in str(response.content)
        self.assertTrue(flag)

    def test_klijent_register_post_success(self):
        c: Client = Client()

        response: HttpResponse = c.post('/registerK/', data={"username": "klijent1", "password1": "sifra123", "password2": "sifra123", "first_name":"ime", "last_name":"prezime", "email":"neki@gmail.com", "visina":"188", "pretplata":"trening/ishrana"})

        self.assertEqual(response.status_code, 302)

        postojiKlijent: bool = Klijent.objects.filter(username="klijent1").exists()
        self.assertTrue(postojiKlijent)    
        klijent: Klijent = Klijent.objects.get(username= "klijent1")
        
        self.assertTrue(klijent.check_password("sifra123"))
        self.assertEqual(klijent.email, "neki@gmail.com")
        self.assertEqual(klijent.first_name, "ime")
        self.assertEqual(klijent.last_name, "prezime")
        self.assertEqual(klijent.visina, 188)

        flag: bool = Plan_Ishrane.objects.filter(korisnik_id=klijent.korisnik_ptr_id).exists()
        self.assertTrue(flag)
        flag = Plan_Treninga.objects.filter(korisnik_id= klijent.korisnik_ptr_id).exists()
        self.assertTrue(flag)
    
    def napraviKlijenta(self,username, password, first_name, last_name, email, visina, pretplata):
        return Klijent.objects.create(username=username, password=password, first_name= first_name, last_name = last_name, email= email, visina= visina, pretplata=pretplata)

    def test_klijent_register_not_success(self):
        c: Client = Client()

        self.napraviKlijenta("klijent2", "sifra123", "ime1", "prezime1", "imejl@imejl", 177, "ishrana")

        response: HttpResponse = c.post('/registerK/', data={"username": "klijent2", "password1": "sifra123", "password2": "sifra123", "first_name":"ime", "last_name":"prezime", "email":"neki@gmail.com", "visina":"188", "pretplata":"ishrana"})

        self.assertEqual(200, response.status_code)

        count: int = Klijent.objects.filter(username="klijent2").count()

        self.assertEqual(count, 1)

        klijent: Klijent = Klijent.objects.get(username="klijent2")

        self.assertEqual(klijent.first_name, "ime1")

    def test_home_get(self):

        c: Client = Client()
        response: HttpResponse = c.get('/')

        self.assertEquals(200, response.status_code)

        sadrzaj: str = str(response.content)

        flag: bool = "GOLD" in sadrzaj
        self.assertTrue(flag)
        flag: bool = "<input type=\"submit\" value=\"Login\">" in sadrzaj
        self.assertTrue(flag)

    def napraviTrenera(self, username, password, first_name, last_name, email):
        Trener.objects.create(username=username, password=password, first_name=first_name, last_name=last_name, email=email)

    def test_treneri_pregled_get(self):

        self.napraviTrenera("trener1", "sifra123", "ime1", "prezime1", "trener1@gmail.com")
        self.napraviTrenera("trener2", "sifra123", "ime2", "prezime2", "trener2@gmail.com")

        c : Client = Client()
        response: HttpResponse = c.get('/treneriP/')

        self.assertEquals(200, response.status_code)


        sadrzaj = str(response.content)

        flag: bool = "trener1" in sadrzaj
        self.assertTrue(flag)
        flag = "trener1@gmail.com" in sadrzaj
        self.assertTrue(flag)
        flag = "trener2" in sadrzaj
        self.assertTrue(flag)
        flag = "trener2@gmail.com" in sadrzaj
        self.assertTrue(flag)

    def test_o_nama_get(self):
        c: Client = Client()

        response: HttpResponse = c.get('/Onama/')

        self.assertEquals(200, response.status_code)

        sadrzaj = str(response.content)
        flag: bool = "Deo za vas opis" in sadrzaj
        self.assertTrue(flag)
    
    def test_treninzi_pregled_get(self):
        c: Client = Client()

        response: HttpResponse = c.get('/treninziP/')

        self.assertEquals(200, response.status_code)

        sadrzaj: str = str(response.content)
        flag: bool = "Ponedeljak" in sadrzaj

        self.assertTrue(flag)
        flag = "Vreme" in sadrzaj
        self.assertTrue(flag)

        flag = "Petak" in sadrzaj
        self.assertTrue(flag)

    def test_usluge_get(self):
        c: Client = Client()

        response: HttpResponse = c.get('/Usluge/')
        self.assertEqual(200, response.status_code)

        sadrzaj: str = str(response.content)
        flag: bool = "U sklopu nasih spotrskih objekata klijenti mogu da uzvaju" in sadrzaj

        self.assertTrue(flag)

    def test_trener_register_get(self):
        c : Client = Client()

        response: HttpResponse = c.get('/registerT/')
        self.assertEqual(200, response.status_code)

        sadrzaj: str = str(response.content)

        flag: bool = "REGISTRACIJA TRENER" in sadrzaj
        self.assertTrue(flag)
        flag = "Visina" in sadrzaj
        self.assertFalse(flag)
        flag = "<input type=\"file\" name=\"slika\" accept=\"image/*\" id=\"id_slika\">" in sadrzaj
        self.assertTrue(flag)
    
    def test_trener_register_success(self):
        c : Client = Client()

        response: HttpResponse = c.post("/registerT/", data={"username": "trener3", "password1": "sifra123", "password2": "sifra123", "first_name":"ime", "last_name":"prezime", "email":"neki@gmail.com"} )

        self.assertEqual(response.status_code, 302)

        flag: bool = Trener.objects.filter(username="trener3").exists()

        self.assertTrue(flag)

        trener: Trener = Trener.objects.get(username="trener3")

        self.assertTrue(trener.check_password("sifra123"))
        self.assertTrue(trener.email, "neki@gmail.com")


    def test_trener_register_not_success(self):
        c: Client = Client()
        self.napraviTrenera("trener4", "sifra123", "ime4", "prezime4", "mejl@gmail.com")

        response: HttpResponse = c.post("/registerT/", data={"username": "trener4", "password1": "sifra123", "password2": "sifra123", "first_name":"ime", "last_name":"prezime", "email":"neki@gmail.com"})

        self.assertEqual(response.status_code, 200)

        count: int = Trener.objects.filter(username="trener4").count()

        self.assertEqual(1, count)

        trener: Trener = Trener.objects.get(username="trener4")

        self.assertEqual(trener.first_name, "ime4")
        self.assertEqual(trener.email, "mejl@gmail.com")

    
    def test_korsinik_login_not_success(self):
        c: Client = Client()

        response: HttpResponse = c.post("/", data={"username": "klijent4", "password":"sifra123"})

        self.assertEqual(response.status_code, 200)

        sadrzaj = str(response.content)

        flag: bool = "Login" in sadrzaj
        self.assertTrue(flag)

        flag = "Brinete se kako poceti?" in sadrzaj
        self.assertTrue(flag)


    
    def test_klijent_login_success(self):
        
        klijent: Klijent = self.napraviKlijenta("klijent3", "sifra123", "ime", "prezime", "lule@email.com", 144, "trening")
        klijent.set_password("sifra123")
        klijent.save()

        c: Client = Client()

        response: HttpResponse = c.post("/", data={"username": "klijent3", "password":"sifra123"})

        self.assertEqual(response.status_code, 302)
        


    def test_trener_login_success(self):
        trener: Trener = self.napraviTrenera("trener5", "sifra123", "ime", "prezime", "mejl@gmail.com")
        trener.set_password("sifra123")

        c: Client = Client()

        response: HttpResponse = c.post("/", data={"username":"trener5", "password":"sifra123"})

        self.assertEqual(response.status_code, 302)

    def test_admin_login_success(self):
         pass
         """korisnik: Korisnik = Korisnik.objects.create(username="admin1", password="sifra123", first_name="ime", last_name="prezime", email="lule@gmail.com", is_staff = True, is_superuser= True, is_active = True, gender="M")
         korisnik.set_password("sifra123")
         korisnik.save()

         c: Client = Client()

         response: HttpResponse = c.post("/", data={"username": "admin1", "password": "sifra123"})
         self.assertEqual(response.status_code, 302)"""

    
    