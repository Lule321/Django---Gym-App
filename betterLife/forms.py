from tkinter import Image
from django.forms import *
from .models import *
from django.contrib.admin.forms import AuthenticationForm


class SearchForm(Form):
    keyword = CharField(max_length=50, label="", required=False)

class AddInventoryForm(ModelForm):
    class Meta:
        model = Sprava
        exclude = ["datumNabavke"]


class AddMealForm(ModelForm):
    class Meta:
        model = Jelo
        fields = "__all__"

class ChangeUserForm(ModelForm):
    class Meta:
        model = Klijent
        fields = ["pretplata"]

class AdminAuthenticationForm(AuthenticationForm):
    """
    A custom authentication form used in the admin app.
    """

    error_messages = {
        **AuthenticationForm.error_messages,
        "invalid_login": (
            "Please enter the correct %(username)s and password for a staff "
            "account. Note that both fields may be case-sensitive."
        ),
    }
    required_css_class = "required"

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise ValidationError(
                self.error_messages["invalid_login"],
                code="invalid_login",
                params={"username": self.username_field.verbose_name},
            )


"""Panta"""
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class KlijentForm(UserCreationForm):

    slika = ImageField(required=False)
    CHOICES = [
        ('trening', 'Trening'),
        ('ishrana', 'Ishrana'),
        ('trening/ishrana', 'Trening/Ishrana'),
        ('/', '/')
    ]
    pretplata = ChoiceField(widget=RadioSelect, choices=CHOICES)
    class Meta:
        model = Klijent
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'visina', 'slika', 'pretplata']


class TrenerForm(UserCreationForm):

    slika = ImageField(required=False)

    class Meta:
        model = Trener
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'slika']