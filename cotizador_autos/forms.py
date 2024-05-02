from django import forms
from .models import Modelos
from django.db import models
import datetime

#Opcion = [
    #('AUDI', 'AUDI'),
    #('BMW', 'BMW'),
    #('CHEVROLET', 'CHEVROLET'),
    #('CMC','CMC'),
    #('DODGE', 'DODGE'),
    #('FORD', 'FORD'),
    #('HONDA', 'HONDA'),
    #('HYUNDAI', 'HYUNDAI'),
    #('ISUZU', 'ISUZU'),
    #('JAGUAR', 'JAGUAR'),
    #('JEEP', 'JEEP'),
    #('KIA', 'KIA'),
    #('LAND ROVER', 'LAND ROVER'),
    #('LEXUS', 'LEXUS'),
    #('MAZDA', 'MZADA'),
    #('MERCEDES BENZ', 'MERCEDES BENZ'),
    #('MITSUBISHI', 'MITSUBISHI'),
    #('NISSAN', 'NISSAN'),
    #('PEUGEOT', 'PEUGEOT'),
    #('PORSCHE', 'PORSCHE'),
    #('QUANTUM', 'QUANTUM'),
    #('RAM', 'RAM'),
    #('RENAULT', 'RENAULT'),
    #('SCION', 'SCION'),
    #('SUZUKI', 'SUZUKI'),
    #('TOYOTA', 'TOYOTA'),
    #('VOLKSWAGEN', 'VOLKSWAGEN'),
    #('VOLVO', 'VOLVO'),
    #('ZOTYE', 'ZOTYE'),
#]
Opcion2 = [
    ('Si', 'Si'),
    ('No', 'No'),
]

current_year = datetime.datetime.now().year
Opciones_Año = [(year, year) for year in range(current_year + 1, current_year - 21, -1)]


class C_Intermediario2(forms.Form):
    Nombre = forms.CharField(label="Nombre de Empresa:", max_length=200, required=False)
    Int = forms.CharField(label="Intermediario:", max_length=200, required=False)
    Tel = forms.CharField(label="Teléfono:", max_length=200, required=False)
    Correo = forms.CharField(label="Correo electrónico:", max_length=200, required=False)
    Id = forms.CharField(label="IVD o CVD:", max_length=200, required=False) 
    
class form_CotizadorTAR(forms.Form):
    Sol = forms.CharField(label="Solicitante:", max_length=200)
    Mail = forms.CharField(label="Correo Electrónico", max_length=200, required=False)
    Cellphone = forms.CharField(label="Celular:", max_length=200)
    Marc = forms.ChoiceField(label="Marca:", choices=[], widget=forms.Select(attrs={'id': 'id_Marc'}))
    Model = forms.ChoiceField(label="Modelo:", choices=[], widget=forms.Select(attrs={'id': 'id_Model'}))
    Agen = forms.ChoiceField(label='Agencia:', choices=Opcion2, widget=forms.Select(attrs={'id': 'id_Agen'}))
    Año = forms.ChoiceField(label="Año de Fabricación:", choices=Opciones_Año, initial=current_year + 1, widget=forms.Select(attrs={'id': 'id_Año'}))
    Plac = forms.CharField(label="Placa:", max_length=100)
    Sum = forms.CharField(label="Suma Asegurada (Valor máximo: $115,000):", max_length=200)
    Rep = forms.ChoiceField(label="Cobertura de Llanta de Repuesto:", choices=Opcion2, widget=forms.Select(attrs={'id':'Rep'}))    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Marc'].choices = [('', 'Seleccione la Marca')] + list(Modelos.objects.values_list('marca', 'marca').distinct())

    def get_marca_choices(self):
        marcas = Modelos.objects.values_list('marca', 'marca').distinct()
        return marcas

class form_Blindaje(forms.Form):
    Blind = forms.CharField(label="Suma de Blindaje:", max_length=100, required=False)