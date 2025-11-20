from django import forms
from .models import Reserva, Sala

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['rut']
