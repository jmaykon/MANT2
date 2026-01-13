from django import forms
from apps.mantenimiento.models import Ticket

class AtenderTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['diagnostico', 'solucion_aplicada', 'observaciones_tecnicas', 'comentario_usuario']
        widgets = {
            'diagnostico': forms.Textarea(attrs={'placeholder': 'Diagnóstico', 'class': 'border rounded p-2'}),
            'solucion_aplicada': forms.Textarea(attrs={'placeholder': 'Solución aplicada', 'class': 'border rounded p-2'}),
            'observaciones_tecnicas': forms.Textarea(attrs={'placeholder': 'Observaciones técnicas', 'class': 'border rounded p-2'}),
            'comentario_usuario': forms.Textarea(attrs={'placeholder': 'Comentario del usuario', 'class': 'border rounded p-2'}),
        }
