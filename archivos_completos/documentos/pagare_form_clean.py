class PagareForm(forms.ModelForm):
    class Meta:
        model = Pagare
        fields = [
            'lugar_emision', 'fecha_emision', 'acreedor_nombre', 'acreedor_domicilio', 'acreedor_rfc',
            'deudor_nombre', 'deudor_domicilio', 'deudor_rfc', 'deudor_representante',
            'monto_numeric', 'monto_literal', 'moneda', 'concepto',
            'tipo_pago', 'num_pagos', 'periodicidad', 'lugar_pago', 'forma_pago',
            'tasa_interes_ordinario', 'base_intereses', 'tasa_interes_moratorio', 'gastos_admon',
            'prepago_permitido', 'dias_aviso_prepago', 'condicion_prepago',
            'tiene_garantia', 'descripcion_garantia', 'aval_nombre', 'aval_domicilio',
            'eventos_incumplimiento', 'clausula_aceleracion', 'jurisdiccion', 'ley_aplicable',
            'num_paginas', 'anexos', 'estado'
        ]
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'monto_numeric': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasa_interes_ordinario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasa_interes_moratorio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'gastos_admon': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'base_intereses': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_pagos': forms.NumberInput(attrs={'class': 'form-control'}),
            'dias_aviso_prepago': forms.NumberInput(attrs={'class': 'form-control'}),
            'num_paginas': forms.NumberInput(attrs={'class': 'form-control'}),
            'acreedor_domicilio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'deudor_domicilio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'descripcion_garantia': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'aval_domicilio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'eventos_incumplimiento': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'clausula_aceleracion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'anexos': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'tipo_pago': forms.Select(attrs={'class': 'form-select'}),
            'periodicidad': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'prepago_permitido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tiene_garantia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'lugar_emision': 'Lugar de Emision',
            'fecha_emision': 'Fecha de Emision',
            'acreedor_nombre': 'Nombre del Acreedor',
            'acreedor_domicilio': 'Domicilio del Acreedor',
            'acreedor_rfc': 'RFC del Acreedor',
            'deudor_nombre': 'Nombre del Deudor',
            'deudor_domicilio': 'Domicilio del Deudor',
            'deudor_rfc': 'RFC del Deudor',
            'deudor_representante': 'Representante del Deudor',
            'monto_numeric': 'Monto Principal',
            'monto_literal': 'Monto Principal (en texto)',
            'moneda': 'Moneda',
            'concepto': 'Concepto del Pagare',
            'tipo_pago': 'Tipo de Pago',
            'num_pagos': 'Numero de Pagos',
            'periodicidad': 'Periodicidad',
            'lugar_pago': 'Lugar de Pago',
            'forma_pago': 'Forma de Pago',
            'tasa_interes_ordinario': 'Tasa de Interes Ordinario (%)',
            'base_intereses': 'Base de Calculo (dias)',
            'tasa_interes_moratorio': 'Tasa de Interes Moratorio (%)',
            'gastos_admon': 'Gastos de Administracion',
            'prepago_permitido': 'Permitir Prepago',
            'dias_aviso_prepago': 'Dias de Aviso para Prepago',
            'condicion_prepago': 'Condicion de Prepago',
            'tiene_garantia': 'Tiene Garantia o Aval',
            'descripcion_garantia': 'Descripcion de la Garantia',
            'aval_nombre': 'Nombre del Aval',
            'aval_domicilio': 'Domicilio del Aval',
            'eventos_incumplimiento': 'Eventos de Incumplimiento',
            'clausula_aceleracion': 'Clausula de Aceleracion',
            'jurisdiccion': 'Jurisdiccion',
            'ley_aplicable': 'Ley Aplicable',
            'num_paginas': 'Numero de Paginas',
            'anexos': 'Anexos',
            'estado': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})
