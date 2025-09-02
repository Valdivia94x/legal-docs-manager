from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ActaAsamblea, ActaSesionConsejo, Pagare, ContratoCredito, ContratoPrendaAcciones, ConvenioModificatorio

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellidos')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

# Existing forms for ActaAsamblea and ActaSesionConsejo would go here
# For brevity, I'll include just the new forms

class PagareForm(forms.ModelForm):
    class Meta:
        model = Pagare
        fields = [
            'lugar_emision', 'fecha_emision', 'acreedor_nombre', 'acreedor_domicilio',
            'deudor_nombre', 'deudor_domicilio', 'monto_principal', 'monto_principal_texto',
            'tasa_interes_anual', 'fecha_vencimiento', 'lugar_pago', 'clausula_aceleracion',
            'aval_nombre', 'aval_domicilio', 'estado'
        ]
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'monto_principal': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasa_interes_anual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'acreedor_domicilio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'deudor_domicilio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'clausula_aceleracion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'aval_domicilio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})


class ContratoCreditoForm(forms.ModelForm):
    class Meta:
        model = ContratoCredito
        fields = [
            'fecha_contrato', 'lugar_contrato', 'acreditante_razon_social', 'acreditante_forma_legal',
            'acreditante_representante', 'acreditado_razon_social_original', 'monto_credito',
            'monto_credito_texto', 'numero_disposiciones', 'disposicion1_fecha', 'disposicion1_importe',
            'disposicion2_fecha', 'disposicion2_importe', 'disposicion3_fecha', 'disposicion3_importe',
            'plazo_credito_fecha_vencimiento', 'tasa_interes_ordinaria', 'tasa_interes_moratoria',
            'banco_cuenta_numero', 'banco_nombre', 'banco_titular', 'banco_clabe',
            'domicilio_acreditante', 'domicilio_acreditado', 'aval_nombre', 'aval_domicilio', 'estado'
        ]
        widgets = {
            'fecha_contrato': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'disposicion1_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'disposicion2_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'disposicion3_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'plazo_credito_fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'monto_credito': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'disposicion1_importe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'disposicion2_importe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'disposicion3_importe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasa_interes_ordinaria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasa_interes_moratoria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'domicilio_acreditante': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'domicilio_acreditado': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'aval_domicilio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})


class ContratoPrendaAccionesForm(forms.ModelForm):
    class Meta:
        model = ContratoPrendaAcciones
        fields = [
            'fecha_contrato', 'lugar_contrato', 'numero_fideicomiso', 'fecha_fideicomiso',
            'fecha_aprobacion_proyecto', 'descripcion_proyecto', 'deudor_nombre',
            'deudor_representante', 'acciones_pledged_cantidad', 'acciones_pledged_texto',
            'acreedor_nombre', 'delegado_fiduciario', 'fideicomitente_nombre',
            'fideicomitente_representante', 'domicilio_deudor', 'domicilio_acreedor',
            'domicilio_fideicomitente', 'estado'
        ]
        widgets = {
            'fecha_contrato': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fideicomiso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_aprobacion_proyecto': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'acciones_pledged_cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion_proyecto': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'domicilio_deudor': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'domicilio_acreedor': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'domicilio_fideicomitente': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})


class ConvenioModificatorioForm(forms.ModelForm):
    class Meta:
        model = ConvenioModificatorio
        fields = [
            'fecha_convenio', 'lugar_convenio', 'inversionista_razon_social',
            'inversionista_representante', 'contrato_original_fecha', 'estudiante_nombre',
            'estudiante_estado_civil', 'estudiante_nacionalidad', 'estudiante_ocupacion',
            'estudiante_rfc', 'estudiante_curp', 'adeudo_principal_anterior',
            'adeudo_principal_anterior_texto', 'luis_nombre', 'luis_rfc', 'luis_curp',
            'lizette_nombre', 'lizette_rfc', 'lizette_curp', 'aumento_monto',
            'aumento_monto_texto', 'inversion_total', 'inversion_total_texto',
            'adeudo_actualizado', 'pagare_ii_fecha', 'dispo_periodo_inicio',
            'dispo_periodo_fin', 'cat_anual', 'tasa_interes_mensual',
            'tasa_moratoria_mensual', 'cuenta_numero', 'cuenta_banco',
            'cuenta_titular', 'cuenta_clabe', 'cursos_requeridos', 'beneficio_descripcion',
            'confidencialidad_years', 'estado'
        ]
        widgets = {
            'fecha_convenio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'contrato_original_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pagare_ii_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dispo_periodo_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dispo_periodo_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'adeudo_principal_anterior': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'aumento_monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'inversion_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'adeudo_actualizado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cat_anual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasa_interes_mensual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasa_moratoria_mensual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'beneficio_descripcion': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})
