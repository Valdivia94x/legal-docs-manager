from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ActaAsamblea, ActaSesionConsejo, Pagare, ContratoCredito, ContratoPrendaAcciones, ConvenioModificatorio
from .estatutos_sociedad import EstatutosSociedad
import json

class EstatutosSociedadForm(forms.ModelForm):
    # Campos personalizados para manejar JSON como texto
    objeto_social_texto = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        label='Objeto Social',
        help_text='Ingrese las cláusulas del objeto social (una por línea)',
    )
    
    clase_acciones_texto = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        label='Clases de Acciones',
        help_text='Ingrese la descripción de las clases de acciones (una por línea)',
    )
    class Meta:
        model = EstatutosSociedad
        fields = [
            'denominacion', 'forma_legal', 'domicilio', 'nacionalidad',
            'duracion_indefinida', 'convenio_admision_extranjeros',
            'capital_fijo_monto', 'capital_fijo_texto', 'acciones_serie_a', 'capital_variable_ilimitado',
            'libro_registro_acciones', 'derecho_preferencia',
            'procedimiento_transmision', 'periodicidad_asamblea', 'quorum_ordinaria', 'quorum_extraordinaria',
            'num_consejeros', 'suplentes_permitidos', 'num_comisarios', 'comisarios_suplentes',
            'ejercicio_inicio', 'ejercicio_fin', 'reserva_legal_pct', 'estado'
        ]
        widgets = {
            'capital_fijo_monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'acciones_serie_a': forms.NumberInput(attrs={'class': 'form-control'}),
            'quorum_ordinaria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quorum_extraordinaria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reserva_legal_pct': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'num_consejeros': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_comisarios': forms.NumberInput(attrs={'class': 'form-control'}),
            'domicilio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'procedimiento_transmision': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'duracion_indefinida': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'convenio_admision_extranjeros': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'capital_variable_ilimitado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'derecho_preferencia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'suplentes_permitidos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'comisarios_suplentes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'denominacion': 'Denominación Social',
            'forma_legal': 'Forma Legal',
            'domicilio': 'Domicilio Social',
            'nacionalidad': 'Nacionalidad',
            'objeto_social': 'Objeto Social',
            'duracion_indefinida': 'Duración Indefinida',
            'convenio_admision_extranjeros': 'Convenio de Admisión de Extranjeros',
            'capital_fijo_monto': 'Capital Fijo (Monto)',
            'capital_fijo_texto': 'Capital Fijo (en texto)',
            'acciones_serie_a': 'Acciones Serie A',
            'capital_variable_ilimitado': 'Capital Variable Ilimitado',
            'clase_acciones': 'Clases de Acciones',
            'libro_registro_acciones': 'Libro de Registro de Acciones',
            'derecho_preferencia': 'Derecho de Preferencia',
            'procedimiento_transmision': 'Procedimiento de Transmisión',
            'periodicidad_asamblea': 'Periodicidad de Asamblea',
            'quorum_ordinaria': 'Quórum Asamblea Ordinaria (%)',
            'quorum_extraordinaria': 'Quórum Asamblea Extraordinaria (%)',
            'num_consejeros': 'Número de Consejeros',
            'suplentes_permitidos': 'Suplentes Permitidos',
            'num_comisarios': 'Número de Comisarios',
            'comisarios_suplentes': 'Comisarios Suplentes',
            'ejercicio_inicio': 'Inicio del Ejercicio Social',
            'ejercicio_fin': 'Fin del Ejercicio Social',
            'reserva_legal_pct': 'Reserva Legal (%)',
            'estado': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si estamos editando una instancia existente, convertir JSON a texto
        if self.instance and self.instance.pk:
            if self.instance.objeto_social:
                if isinstance(self.instance.objeto_social, list):
                    self.fields['objeto_social_texto'].initial = '\n'.join(self.instance.objeto_social)
                elif isinstance(self.instance.objeto_social, dict):
                    self.fields['objeto_social_texto'].initial = '\n'.join(self.instance.objeto_social.values())
                else:
                    self.fields['objeto_social_texto'].initial = str(self.instance.objeto_social)
            
            if self.instance.clase_acciones:
                if isinstance(self.instance.clase_acciones, list):
                    self.fields['clase_acciones_texto'].initial = '\n'.join(self.instance.clase_acciones)
                elif isinstance(self.instance.clase_acciones, dict):
                    self.fields['clase_acciones_texto'].initial = '\n'.join(self.instance.clase_acciones.values())
                else:
                    self.fields['clase_acciones_texto'].initial = str(self.instance.clase_acciones)
        
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Convertir texto a JSON para objeto_social
        objeto_social_texto = self.cleaned_data.get('objeto_social_texto', '')
        if objeto_social_texto:
            # Convertir texto a lista (una línea por elemento)
            lineas = [linea.strip() for linea in objeto_social_texto.split('\n') if linea.strip()]
            instance.objeto_social = lineas
        else:
            instance.objeto_social = []
        
        # Convertir texto a JSON para clase_acciones
        clase_acciones_texto = self.cleaned_data.get('clase_acciones_texto', '')
        if clase_acciones_texto:
            # Convertir texto a lista (una línea por elemento)
            lineas = [linea.strip() for linea in clase_acciones_texto.split('\n') if linea.strip()]
            instance.clase_acciones = lineas
        else:
            instance.clase_acciones = []
        
        if commit:
            instance.save()
        return instance
