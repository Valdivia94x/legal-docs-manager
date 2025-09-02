
class PagareForm(forms.ModelForm):
    class Meta:
        model = Pagare
        fields = [
            'lugar_emision', 'fecha_emision', 'acreedor_nombre', 'acreedor_domicilio', 'acreedor_rfc',
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
        labels = {
            'lugar_emision': 'Lugar de Emisión',
            'fecha_emision': 'Fecha de Emisión',
            'acreedor_nombre': 'Nombre del Acreedor',
            'acreedor_domicilio': 'Domicilio del Acreedor',
            'acreedor_rfc': 'RFC del Acreedor',
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
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})
