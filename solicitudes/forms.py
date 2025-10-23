from django import forms
from .models import Solicitud

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'rut', 'nombres', 'apellidos', 'direccion',
            'telefono', 'comuna'
        ]
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9', 'required': True}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56912345678', 'required': True}),
            'comuna': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }


class SolicitudAdminForm(forms.ModelForm):
    """
    Formulario para administradores que incluye el campo de estado.
    """
    class Meta:
        model = Solicitud
        fields = [
            'rut', 'nombres', 'apellidos', 'direccion',
            'telefono', 'comuna', 'estado'
        ]
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9', 'required': True}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56912345678', 'required': True}),
            'comuna': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'estado': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }
