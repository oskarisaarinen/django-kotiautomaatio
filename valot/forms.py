from django import forms
from .models import Huone
from .models import Valo
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class HuoneForm(forms.ModelForm):
    class Meta:
        model = Huone
        fields = ['nimi']
        labels = {
            'nimi': 'Huoneen nimi',
        }

class ValoForm(forms.ModelForm):
    class Meta:
        model = Valo
        fields = ['nimi', 'tila', 'huone']
        labels = {
            'nimi': 'Valon nimi',
            'tila': 'Valon tila',
            'huone': 'Huone',
        }

class LisaaYllapitoKauttaja(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']  # Kentät

    def save(self, commit=True):
        
        user = super().save(commit=False)

        # Ylläpito
        user.is_staff = True
        user.is_superuser = True


        if commit:
            user.save()  # Lisää Kantaan
        return user

class SalasanaHyvaksynta(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control rounded-3'}))

class LisaaKauttaja(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
