from django import forms
from .models import Livre

class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'date_publication', 'disponible', 'image']
        widgets = {
            'date_publication': forms.DateInput(attrs={'type': 'date'}),
        }