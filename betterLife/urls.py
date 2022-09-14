#from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    #path("", views.inventory_view, name="home"),
    path('test_table_view/', views.test_table_view, name='test_table_view'),
    path("test_image_table/", views.test_image_table, name="test_image_table"),

    #gost
    path('registerT/', views.registerT, name="registerT"),
    path('registerK/', views.registerK, name="registerK"),
    path('treneriP/', views.treneriP, name="treneriP"),
    path('treninziP/', views.treninziP, name="treninziP"),
    path("treninziPK/", views.treninziPK, name="treninziPK"),
    path('pitanja/', views.pitanja, name='pitanja'),
    path('', views.home, name='home'),
    path('logout/', views.logout_req, name='logout_req'),
    path('pocetna/', views.pocetna, name="pocetna"),
    #path('accounts/', include('django.contrib.auth.urls')), #ne znam sto je panti ovo trebalo, ali kontam da cu saznati
    #path('change_passwor/', auth_views.PasswordResetView.as_view(), name='change_password'),

    #path('users/change-password/', views.MyPasswordCganheView.as_view(), name='password-change-view'),
    #path('users/change-password/done', views.MyPasswordResetDoneView.as_view(), name='password-change-done-view'),

    path('Onama/', views.Onama, name="Onama"),
    path('Usluge/', views.Usluge, name="Usluge"),

    #klijent
    path("klijent/plan_ishrane/", views.KlijentPlanIshrane, name="plan_ishrane"),
    path("klijent/grupni_treninzi/", views.KlijentGrupniTreninzi, name="grupni_treninzi"),
    path("klijent/trener/", views.KlijentTrener, name="klijent_trener_profil"),
    path("klijent/profil/", views.KlijentProfil, name="klijent_profil"),
    path("klijent/plan/", views.KlijentIzmenaPlana, name="trenutni_plan"),
    path("klijent/trening_plan/", views.KlijentTreningPlan, name="trening_plan"),


    #administrator
    path('test_table_view/', views.test_table_view, name='test_table_view'),
    path("test_image_table/", views.test_image_table, name="test_image_table"),
    path("administrator/", views.admin_index, name="admin_index"),
    path("administrator/inventory_view/", views.inventory_view, name = "admin_inventory_view"),
    path("administrator/inventory_add/", views.inventory_add, name = "admin_inventory_add"),
    path("administrator/sprava/<int:sprava_id>", views.sprava, name="admin_sprava"),
    path("administrator/sprava_change/<int:sprava_id>", views.sprava_change, name="admin_sprava_change"),
    path("administrator/sprava_delete/", views.sprava_delete, name="admin_sprava_delete"),
    path("administrator/meals_view/", views.meals_view, name="admin_meals_view"),
    path("administrator/meal_add/", views.meal_add, name="admin_meal_add"),
    path("administrator/jelo/<int:jelo_id>", views.jelo, name="admin_jelo"),
    path("administrator/jelo_change/<int:jelo_id>", views.jelo_change, name="admin_jelo_change"),
    path("administrator/jelo_delete/", views.jelo_delete, name="admin_jelo_delete"),
    path("administrator/clients_view/", views.clients_view, name="admin_clients_view"),
    path("administrator/trainers_view/", views.trainers_view, name="admin_trainers_view"),
    path("administrator/client/<int:client_id>", views.admin_client, name="admin_client"),
    path("administrator/client_change/<int:client_id>", views.client_change, name="admin_client_change"),
    path("administrator/client_remove", views.client_remove, name="admin_client_remove"),
    path("administrator/trainer/<int:trainer_id>", views.admin_trainer, name="admin_trainer"),
    path("administrator/trainer_verify/", views.trainer_verify, name="admin_trainer_verify"),
    path("administrator/trainer_remove/", views.trainer_remove, name="admin_trainer_remove"),


    #trener deo
    path("trener/pregled_klijenata/", views.trener_pregled_klijenata, name ="trener_pregled_klijenata"),
    path("trener/klijenti_reg_test/", views.trener_klijenti_reg_test, name="trener_klijenti_reg_test"),
    path("trener/pregled_klijenta/<int:id>/", views.trener_pregled_klijenta, name = "trener_pregled_klijenta"),
    path("trener/pregled_jela/", views.trener_pregled_jela, name= "trener_pregled_jela"),
    path("trener/jelo_reg_test/", views.trener_jelo_reg_test, name= "trener_jelo_reg_test"),
    path("trener/pregled_jelo/<int:id>/", views.trener_pregled_jelo, name="trener_pregled_jelo"),
    path("trener/pregled_vezbi/", views.trener_pregled_vezbi, name="trener_pregled_vezbi"),
    path("trener/vezba_reg_test/", views.trener_vezba_reg_test, name="trener_vezba_reg_test"),
    path("trener/pregled_vezbe/<int:id>/", views.trener_pregled_vezbe, name="trener_pregled_vezbe"),
    path("trener/logout_req/", views.trener_logout_req, name="trener_logout_req"),
    path("trener/plan_treninga_reg_test/", views.trener_plan_treninga_reg_test, name="trener_plan_treninga_reg_test"),
    path("trener/trening_reg_test/", views.trener_trening_reg_test, name="trener_trening_reg_test"),
    path("trener/stavka_treninga_reg_test/", views.trener_stavka_treninga_reg_test, name="trener_stavka_treninga_reg_test"),
    path("trener/dodaj_trening/<int:dan>/<int:id_plan_treninga>/", views.trener_dodaj_trening, name="trener_dodaj_trening"),
    path("trener/izmeni_trening/<int:id_trening>/", views.trener_izmeni_trening, name="trener_izmeni_trening"),
    path("trener/izmeni_trening/<int:id_trening>/pretraga/", views.trener_izmeni_trening_pretraga, name="trener_izmeni_trening_pretraga"),
    path("trener/pregled_klijenta/<int:id_klijenta>/posalji_poruku/", views.trener_posalji_poruku, name="trener_posalji_poruku"),
    path("trener/pregled_klijenta/<int:id_klijenta>/izbrisi/", views.trener_izbrisi_trening, name= "trener_izbrisi_trening"),
    path("trener/pregled_klijenta/<int:id_klijenta>/osvezi_chat/", views.trener_osvezi_chat, name="trener_osvezi_chat"),
    path("trener/izmeni_obrok/<int:id_stavka_ishrane>/", views.trener_izmeni_obrok, name="trener_izmeni_obrok"),
    path("trener/izmeni_obrok/<int:id_stavka_ishrane>/pretraga/", views.trener_izmeni_obrok_pretraga, name="trener_izmeni_obrok_pretraga"),
    path("trener/dodaj_obrok/<int:dan>/<int:id_plan_ishrane>/", views.trener_dodaj_obrok, name="trener_dodaj_obrok"),
    path("trener/pregled_klijenta/<int:id_klijenta>/izbrisi_obrok/", views.trener_izbrisi_obrok, name="trener_izbrisi_obrok"),
    path("trener/pregled_profila/", views.trener_pregled_profila, name="trener_pregled_profila"),
]