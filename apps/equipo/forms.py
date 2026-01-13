# apps/equipo/forms.py
from django import forms
from .models import Equipo

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = [
            'tipo', 'aec', 'marca', 'modelo', 'so',
            'procesador','tipo_ram', 'ram', 'tipo_disco', 'disco',
            'estado_disco','observaciones', 'ip', 'estado_equipo'
        ]

