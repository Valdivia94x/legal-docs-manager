from django import forms
from .models import Pagare, ContratoCredito, ContratoPrendaAcciones, ConvenioModificatorio


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
            'lugar_emision': forms.TextInput(attrs={'class': 'form-control'}),
            'acreedor_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'acreedor_domicilio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'deudor_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'deudor_domicilio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'monto_principal_texto': forms.TextInput(attrs={'class': 'form-control'}),
            'lugar_pago': forms.TextInput(attrs={'class': 'form-control'}),
            'clausula_aceleracion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'aval_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'aval_domicilio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'lugar_emision': 'Lugar de Emisión',
            'fecha_emision': 'Fecha de Emisión',
            'acreedor_nombre': 'Nombre del Acreedor',
            'acreedor_domicilio': 'Domicilio del Acreedor',
            'deudor_nombre': 'Nombre del Deudor',
            'deudor_domicilio': 'Domicilio del Deudor',
            'monto_principal': 'Monto Principal',
            'monto_principal_texto': 'Monto Principal (en texto)',
            'tasa_interes_anual': 'Tasa de Interés Anual (%)',
            'fecha_vencimiento': 'Fecha de Vencimiento',
            'lugar_pago': 'Lugar de Pago',
            'clausula_aceleracion': 'Cláusula de Aceleración',
            'aval_nombre': 'Nombre del Aval',
            'aval_domicilio': 'Domicilio del Aval',
            'estado': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases CSS a todos los campos
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
            'plazo_credito_fecha_vencimiento', 'pagos_intereses_fecha1', 'pagos_intereses_fecha2',
            'pagos_intereses_fecha3', 'pago_principal_fecha', 'tasa_interes_ordinaria',
            'tasa_interes_moratoria', 'banco_cuenta_numero', 'banco_nombre', 'banco_titular',
            'banco_clabe', 'domicilio_acreditante', 'domicilio_acreditado', 'aval_nombre',
            'aval_domicilio', 'estado'
        ]
        widgets = {
            'fecha_contrato': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'disposicion1_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'disposicion2_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'disposicion3_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'plazo_credito_fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pagos_intereses_fecha1': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pagos_intereses_fecha2': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pagos_intereses_fecha3': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pago_principal_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'monto_credito': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'disposicion1_importe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'disposicion2_importe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'disposicion3_importe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasa_interes_ordinaria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasa_interes_moratoria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'numero_disposiciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'domicilio_acreditante': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'domicilio_acreditado': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'aval_domicilio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'fecha_contrato': 'Fecha del Contrato',
            'lugar_contrato': 'Lugar del Contrato',
            'acreditante_razon_social': 'Razón Social del Acreditante',
            'acreditante_forma_legal': 'Forma Legal del Acreditante',
            'acreditante_representante': 'Representante del Acreditante',
            'acreditado_razon_social_original': 'Razón Social del Acreditado',
            'monto_credito': 'Monto del Crédito',
            'monto_credito_texto': 'Monto del Crédito (en texto)',
            'numero_disposiciones': 'Número de Disposiciones',
            'plazo_credito_fecha_vencimiento': 'Fecha de Vencimiento',
            'tasa_interes_ordinaria': 'Tasa de Interés Ordinaria (%)',
            'tasa_interes_moratoria': 'Tasa de Interés Moratoria (%)',
            'banco_cuenta_numero': 'Número de Cuenta',
            'banco_nombre': 'Nombre del Banco',
            'banco_titular': 'Titular de la Cuenta',
            'banco_clabe': 'CLABE Interbancaria',
            'domicilio_acreditante': 'Domicilio del Acreditante',
            'domicilio_acreditado': 'Domicilio del Acreditado',
            'aval_nombre': 'Nombre del Aval',
            'aval_domicilio': 'Domicilio del Aval',
            'estado': 'Estado',
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
        labels = {
            'fecha_contrato': 'Fecha del Contrato',
            'lugar_contrato': 'Lugar del Contrato',
            'numero_fideicomiso': 'Número del Fideicomiso',
            'fecha_fideicomiso': 'Fecha del Fideicomiso',
            'fecha_aprobacion_proyecto': 'Fecha de Aprobación del Proyecto',
            'descripcion_proyecto': 'Descripción del Proyecto',
            'deudor_nombre': 'Nombre del Deudor Prendario',
            'deudor_representante': 'Representante del Deudor',
            'acciones_pledged_cantidad': 'Cantidad de Acciones Pignoradas',
            'acciones_pledged_texto': 'Acciones Pignoradas (en texto)',
            'acreedor_nombre': 'Nombre del Acreedor Prendario',
            'delegado_fiduciario': 'Delegado Fiduciario',
            'fideicomitente_nombre': 'Nombre del Fideicomitente',
            'fideicomitente_representante': 'Representante del Fideicomitente',
            'domicilio_deudor': 'Domicilio del Deudor',
            'domicilio_acreedor': 'Domicilio del Acreedor',
            'domicilio_fideicomitente': 'Domicilio del Fideicomitente',
            'estado': 'Estado',
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
            'tasa_moratoria_mensual', 'pagos_estudios_num1', 'pagos_estudios_imp1',
            'pagos_estudios_num2', 'pagos_estudios_imp2', 'pagos_egreso_num',
            'pagos_egreso_imp', 'pago_egreso_ultimo', 'cuenta_numero', 'cuenta_banco',
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
            'pagos_estudios_imp1': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pagos_estudios_imp2': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pagos_egreso_imp': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pago_egreso_ultimo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pagos_estudios_num1': forms.NumberInput(attrs={'class': 'form-control'}),
            'pagos_estudios_num2': forms.NumberInput(attrs={'class': 'form-control'}),
            'pagos_egreso_num': forms.NumberInput(attrs={'class': 'form-control'}),
            'cursos_requeridos': forms.NumberInput(attrs={'class': 'form-control'}),
            'confidencialidad_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'beneficio_descripcion': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'fecha_convenio': 'Fecha del Convenio',
            'lugar_convenio': 'Lugar del Convenio',
            'inversionista_razon_social': 'Razón Social del Inversionista',
            'inversionista_representante': 'Representante del Inversionista',
            'contrato_original_fecha': 'Fecha del Contrato Original',
            'estudiante_nombre': 'Nombre del Estudiante',
            'estudiante_estado_civil': 'Estado Civil',
            'estudiante_nacionalidad': 'Nacionalidad',
            'estudiante_ocupacion': 'Ocupación',
            'estudiante_rfc': 'RFC del Estudiante',
            'estudiante_curp': 'CURP del Estudiante',
            'adeudo_principal_anterior': 'Adeudo Principal Anterior',
            'adeudo_principal_anterior_texto': 'Adeudo Anterior (en texto)',
            'luis_nombre': 'Nombre de Luis',
            'luis_rfc': 'RFC de Luis',
            'luis_curp': 'CURP de Luis',
            'lizette_nombre': 'Nombre de Lizette',
            'lizette_rfc': 'RFC de Lizette',
            'lizette_curp': 'CURP de Lizette',
            'aumento_monto': 'Monto del Aumento',
            'aumento_monto_texto': 'Monto del Aumento (en texto)',
            'inversion_total': 'Inversión Total',
            'inversion_total_texto': 'Inversión Total (en texto)',
            'adeudo_actualizado': 'Adeudo Actualizado',
            'pagare_ii_fecha': 'Fecha del Pagaré II',
            'dispo_periodo_inicio': 'Inicio del Periodo de Disposición',
            'dispo_periodo_fin': 'Fin del Periodo de Disposición',
            'cat_anual': 'CAT Anual (%)',
            'tasa_interes_mensual': 'Tasa de Interés Mensual (%)',
            'tasa_moratoria_mensual': 'Tasa Moratoria Mensual (%)',
            'pagos_estudios_num1': 'Número de Pagos Estudios 1',
            'pagos_estudios_imp1': 'Importe Pagos Estudios 1',
            'pagos_estudios_num2': 'Número de Pagos Estudios 2',
            'pagos_estudios_imp2': 'Importe Pagos Estudios 2',
            'pagos_egreso_num': 'Número de Pagos Egreso',
            'pagos_egreso_imp': 'Importe Pagos Egreso',
            'pago_egreso_ultimo': 'Último Pago Egreso',
            'cuenta_numero': 'Número de Cuenta',
            'cuenta_banco': 'Banco',
            'cuenta_titular': 'Titular de la Cuenta',
            'cuenta_clabe': 'CLABE',
            'cursos_requeridos': 'Cursos Requeridos',
            'beneficio_descripcion': 'Descripción del Beneficio',
            'confidencialidad_years': 'Años de Confidencialidad',
            'estado': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})
