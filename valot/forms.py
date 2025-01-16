from django import forms
from .models import Huone
from .models import Valo


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