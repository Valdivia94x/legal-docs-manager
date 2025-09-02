from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ActaAsamblea, ActaSesionConsejo, Pagare, ContratoCredito, ContratoPrendaAcciones, ConvenioModificatorio
from .estatutos_sociedad import EstatutosSociedad
import json

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='Nombre')
    last_name = forms.CharField(max_length=30, required=True, label='Apellidos')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ActaAsambleaForm(forms.ModelForm):
    # Campos JSON como campos de texto para facilitar el llenado
    asistentes_texto = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        label='Asistentes',
        help_text='Lista de asistentes (uno por línea)'
    )
    
    orden_dia_texto = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label='Orden del Día y Resoluciones (JSON)',
        help_text='JSON con puntos del orden del día y resoluciones anidadas'
    )
    
    resoluciones_texto = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 8, 'class': 'form-control'}),
        label='Resoluciones',
        help_text='Resoluciones adoptadas (una por párrafo)'
    )
    
    nombramientos_texto = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        label='Nombramientos',
        help_text='Nombramientos realizados (uno por línea)'
    )
    
    dividendos_texto = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        label='Dividendos',
        help_text='Información sobre dividendos aprobados'
    )
    
    delegados_texto = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        label='Delegados',
        help_text='Delegados designados'
    )
    
    anexos_texto = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        label='Anexos',
        help_text='Descripción de anexos incluidos'
    )
    
    class Meta:
        model = ActaAsamblea
        fields = [
            'razon_social', 'tipo_asamblea', 'caracter', 'fecha', 'hora_inicio',
            'hora_cierre', 'lugar', 'porcentaje_capital_presente', 'convocatoria_omitida',
            'fundamento_convocatoria', 'presidente', 'secretario', 'escrutador',
            'comisario', 'metodo_votacion_general', 'estado'
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_cierre': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'lugar': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'fundamento_convocatoria': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'porcentaje_capital_presente': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0',
                'max': '100'
            }),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'caracter': forms.TextInput(attrs={'class': 'form-control'}),
            'presidente': forms.TextInput(attrs={'class': 'form-control'}),
            'secretario': forms.TextInput(attrs={'class': 'form-control'}),
            'escrutador': forms.TextInput(attrs={'class': 'form-control'}),
            'comisario': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_asamblea': forms.Select(attrs={'class': 'form-select'}),
            'metodo_votacion_general': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'convocatoria_omitida': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si estamos editando, poblar los campos de texto desde los JSON
        if self.instance and self.instance.pk:
            if self.instance.asistentes_json:
                if isinstance(self.instance.asistentes_json, list):
                    self.fields['asistentes_texto'].initial = '\n'.join(self.instance.asistentes_json)
                else:
                    self.fields['asistentes_texto'].initial = str(self.instance.asistentes_json)
            
            if self.instance.orden_dia_json:
                import json
                self.fields['orden_dia_texto'].initial = json.dumps(
                    self.instance.orden_dia_json, ensure_ascii=False, indent=2
                )
            
            if self.instance.resoluciones_json:
                if isinstance(self.instance.resoluciones_json, list):
                    self.fields['resoluciones_texto'].initial = '\n\n'.join(self.instance.resoluciones_json)
                else:
                    self.fields['resoluciones_texto'].initial = str(self.instance.resoluciones_json)
            
            if self.instance.nombramientos_json:
                if isinstance(self.instance.nombramientos_json, list):
                    self.fields['nombramientos_texto'].initial = '\n'.join(self.instance.nombramientos_json)
                else:
                    self.fields['nombramientos_texto'].initial = str(self.instance.nombramientos_json)
            
            if self.instance.dividendos_json:
                if isinstance(self.instance.dividendos_json, list):
                    self.fields['dividendos_texto'].initial = '\n'.join(self.instance.dividendos_json)
                else:
                    self.fields['dividendos_texto'].initial = str(self.instance.dividendos_json)
            
            if self.instance.delegados_json:
                if isinstance(self.instance.delegados_json, list):
                    self.fields['delegados_texto'].initial = '\n'.join(self.instance.delegados_json)
                else:
                    self.fields['delegados_texto'].initial = str(self.instance.delegados_json)
            
            if self.instance.anexos_json:
                if isinstance(self.instance.anexos_json, list):
                    self.fields['anexos_texto'].initial = '\n'.join(self.instance.anexos_json)
                else:
                    self.fields['anexos_texto'].initial = str(self.instance.anexos_json)
        
        # Aplicar clases CSS a todos los campos
        for field_name, field in self.fields.items():
            if field_name != 'convocatoria_omitida':
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})
    
    def clean_orden_dia_texto(self):
        import json
        data = self.cleaned_data['orden_dia_texto']
        if not data or not data.strip():
            return None
        try:
            return json.loads(data)
        except Exception as e:
            raise forms.ValidationError(f"JSON inválido: {e}")
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Convertir campos de texto a JSON
        asistentes_texto = self.cleaned_data.get('asistentes_texto', '')
        if asistentes_texto:
            instance.asistentes_json = [line.strip() for line in asistentes_texto.split('\n') if line.strip()]
        else:
            instance.asistentes_json = None
        
        # Convertir orden_dia_texto a JSON (ya validado en clean_orden_dia_texto)
        instance.orden_dia_json = self.cleaned_data.get('orden_dia_texto')
        
        resoluciones_texto = self.cleaned_data.get('resoluciones_texto', '')
        if resoluciones_texto:
            # Para resoluciones, dividir por párrafos (doble salto de línea)
            instance.resoluciones_json = [para.strip() for para in resoluciones_texto.split('\n\n') if para.strip()]
        else:
            instance.resoluciones_json = None
        
        nombramientos_texto = self.cleaned_data.get('nombramientos_texto', '')
        if nombramientos_texto:
            instance.nombramientos_json = [line.strip() for line in nombramientos_texto.split('\n') if line.strip()]
        else:
            instance.nombramientos_json = None
        
        dividendos_texto = self.cleaned_data.get('dividendos_texto', '')
        if dividendos_texto:
            instance.dividendos_json = [line.strip() for line in dividendos_texto.split('\n') if line.strip()]
        else:
            instance.dividendos_json = None
        
        delegados_texto = self.cleaned_data.get('delegados_texto', '')
        if delegados_texto:
            instance.delegados_json = [line.strip() for line in delegados_texto.split('\n') if line.strip()]
        else:
            instance.delegados_json = None
        
        anexos_texto = self.cleaned_data.get('anexos_texto', '')
        if anexos_texto:
            instance.anexos_json = [line.strip() for line in anexos_texto.split('\n') if line.strip()]
        else:
            instance.anexos_json = None
        
        if commit:
            instance.save()
        return instance


class EstatutosSociedadForm(forms.ModelForm):
    class Meta:
        model = EstatutosSociedad
        fields = [
            'denominacion', 'forma_legal', 'domicilio', 'nacionalidad',
            'objeto_social', 'duracion_indefinida', 'convenio_admision_extranjeros',
            'capital_fijo_monto', 'capital_fijo_texto', 'acciones_serie_a', 'capital_variable_ilimitado',
            'clase_acciones', 'libro_registro_acciones', 'derecho_preferencia',
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
            'objeto_social': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'clase_acciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
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
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})
        
        # Poblar campos de texto con datos JSON existentes si los hay
        if self.instance and self.instance.pk:
            if self.instance.asistentes_json:
                asistentes_lines = []
                for asistente in self.instance.asistentes_json:
                    if isinstance(asistente, dict):
                        line = f"{asistente.get('nombre', '')} - {asistente.get('acciones', '')} acciones - {asistente.get('porcentaje', '')}%"
                        asistentes_lines.append(line.strip(' - '))
                    else:
                        asistentes_lines.append(str(asistente))
                self.fields['asistentes_texto'].initial = '\n'.join(asistentes_lines)
            
            if self.instance.orden_dia_json:
                orden_lines = []
                for punto in self.instance.orden_dia_json:
                    if isinstance(punto, dict):
                        line = f"{punto.get('numero', '')}. {punto.get('titulo', '')}"
                        if punto.get('descripcion'):
                            line += f" - {punto.get('descripcion')}"
                        orden_lines.append(line)
                    else:
                        orden_lines.append(str(punto))
                self.fields['orden_dia_texto'].initial = '\n'.join(orden_lines)

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Procesar asistentes
        asistentes_texto = self.cleaned_data.get('asistentes_texto', '').strip()
        if asistentes_texto:
            asistentes_list = []
            for linea in asistentes_texto.split('\n'):
                if linea.strip():
                    partes = [p.strip() for p in linea.split(' - ')]
                    if len(partes) >= 3:
                        asistente = {
                            'nombre': partes[0],
                            'acciones': partes[1].replace(' acciones', ''),
                            'porcentaje': partes[2].replace('%', '')
                        }
                        asistentes_list.append(asistente)
                    else:
                        asistente = {'nombre': linea.strip()}
                        asistentes_list.append(asistente)
            instance.asistentes_json = asistentes_list if asistentes_list else None
        else:
            instance.asistentes_json = None
        
        # Procesar orden del día
        orden_dia_texto = self.cleaned_data.get('orden_dia_texto', '').strip()
        if orden_dia_texto:
            orden_list = []
            for i, linea in enumerate(orden_dia_texto.split('\n'), 1):
                if linea.strip():
                    if '. ' in linea:
                        numero_parte, resto = linea.split('. ', 1)
                        try:
                            numero = int(numero_parte)
                        except ValueError:
                            numero = i
                            resto = linea
                    else:
                        numero = i
                        resto = linea
                    
                    if ' - ' in resto:
                        titulo, descripcion = resto.split(' - ', 1)
                    else:
                        titulo = resto
                        descripcion = ''
                    
                    punto = {
                        'numero': numero,
                        'titulo': titulo.strip(),
                        'descripcion': descripcion.strip()
                    }
                    orden_list.append(punto)
            instance.orden_dia_json = orden_list if orden_list else None
        else:
            instance.orden_dia_json = None
        
        # Procesar otros campos JSON de manera similar
        resoluciones_texto = self.cleaned_data.get('resoluciones_texto', '').strip()
        if resoluciones_texto:
            resoluciones_list = []
            for linea in resoluciones_texto.split('\n'):
                if linea.strip():
                    partes = [p.strip() for p in linea.split(' - ')]
                    if len(partes) >= 3:
                        resolucion = {
                            'punto': partes[0].replace('Punto ', ''),
                            'clave': partes[1],
                            'texto': partes[2],
                            'tipo': partes[3] if len(partes) > 3 else 'general'
                        }
                        resoluciones_list.append(resolucion)
            instance.resoluciones_json = resoluciones_list if resoluciones_list else None
        else:
            instance.resoluciones_json = None
        
        if commit:
            instance.save()
        return instance


class ActaSesionConsejoForm(forms.ModelForm):
    # Campos JSON como campos de texto para facilitar el llenado
    
    invitados_texto = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        label='Invitados',
        help_text='Lista de invitados (uno por línea)'
    )
    
    orden_dia_texto = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label='Orden del Día y Resoluciones (JSON)'
    )
    
    resoluciones_texto = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 8, 'class': 'form-control'}),
        label='Resoluciones',
        help_text='Resoluciones adoptadas (una por párrafo)'
    )
    
    delegados_texto = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        label='Delegados',
        help_text='Delegados designados'
    )
    
    anexos_texto = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        label='Anexos',
        help_text='Descripción de anexos incluidos'
    )
    
    class Meta:
        model = ActaSesionConsejo
        fields = [
            'razon_social', 'fecha', 'hora_inicio', 'hora_cierre', 'lugar', 'ciudad',
            'convocatoria_realizada', 'presidente', 'secretario', 'estado'
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_cierre': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'lugar': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad de México'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'presidente': forms.TextInput(attrs={'class': 'form-control'}),
            'secretario': forms.TextInput(attrs={'class': 'form-control'}),
            'convocatoria_realizada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si estamos editando, poblar los campos de texto desde los JSON
        if self.instance and self.instance.pk:
            if self.instance.invitados_json:
                invitados_lines = []
                for invitado in self.instance.invitados_json:
                    if isinstance(invitado, dict):
                        line = f"{invitado.get('nombre', '')} - {invitado.get('cargo', '')}"
                        invitados_lines.append(line.strip(' - '))
                    else:
                        invitados_lines.append(str(invitado))
                self.fields['invitados_texto'].initial = '\n'.join(invitados_lines)
            
            if self.instance.orden_dia_json:
                import json
                self.fields['orden_dia_texto'].initial = json.dumps(
                    self.instance.orden_dia_json, ensure_ascii=False
                )
        
        # Aplicar clases CSS a todos los campos
        for field_name, field in self.fields.items():
            if field_name not in ['convocatoria_realizada']:
                if 'class' not in field.widget.attrs:
                    field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})
    
    def clean_orden_dia_texto(self):
        import json
        data = self.cleaned_data['orden_dia_texto']
        if not data or not data.strip():
            return None
        try:
            return json.loads(data)
        except Exception as e:
            raise forms.ValidationError(f"JSON inválido: {e}")
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Convertir campos de texto a JSON
        # Convertir invitados_texto a JSON
        invitados_texto = self.cleaned_data.get('invitados_texto', '')
        if invitados_texto:
            invitados_list = []
            for linea in invitados_texto.split('\n'):
                if linea.strip():
                    partes = [p.strip() for p in linea.split(' - ')]
                    if len(partes) >= 2:
                        invitado = {
                            'nombre': partes[0],
                            'cargo': partes[1]
                        }
                        invitados_list.append(invitado)
                    else:
                        invitado = {'nombre': linea.strip(), 'cargo': 'Invitado'}
                        invitados_list.append(invitado)
            instance.invitados_json = invitados_list if invitados_list else None
        else:
            instance.invitados_json = None
        
        # Convertir orden_dia_texto a JSON (ya validado en clean_orden_dia_texto)
        instance.orden_dia_json = self.cleaned_data.get('orden_dia_texto')
        
        resoluciones_texto = self.cleaned_data.get('resoluciones_texto', '')
        if resoluciones_texto:
            instance.resoluciones_json = [para.strip() for para in resoluciones_texto.split('\n\n') if para.strip()]
        else:
            instance.resoluciones_json = None
        
        delegados_texto = self.cleaned_data.get('delegados_texto', '')
        if delegados_texto:
            instance.delegados_json = [line.strip() for line in delegados_texto.split('\n') if line.strip()]
        else:
            instance.delegados_json = None
        
        anexos_texto = self.cleaned_data.get('anexos_texto', '')
        if anexos_texto:
            instance.anexos_json = [line.strip() for line in anexos_texto.split('\n') if line.strip()]
        else:
            instance.anexos_json = None
        
        if commit:
            instance.save()
        return instance


class EstatutosSociedadForm(forms.ModelForm):
    class Meta:
        model = EstatutosSociedad
        fields = [
            'denominacion', 'forma_legal', 'domicilio', 'nacionalidad',
            'objeto_social', 'duracion_indefinida', 'convenio_admision_extranjeros',
            'capital_fijo_monto', 'capital_fijo_texto', 'acciones_serie_a', 'capital_variable_ilimitado',
            'clase_acciones', 'libro_registro_acciones', 'derecho_preferencia',
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
            'objeto_social': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'clase_acciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
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
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})
        
        # Poblar campos de texto con datos JSON existentes si los hay
        if self.instance and self.instance.pk:
            if self.instance.asistentes_json:
                asistentes_lines = []
                for asistente in self.instance.asistentes_json:
                    if isinstance(asistente, dict):
                        line = f"{asistente.get('nombre', '')} - {asistente.get('rol', '')}"
                        asistentes_lines.append(line.strip(' - '))
                    else:
                        asistentes_lines.append(str(asistente))
                self.fields['asistentes_texto'].initial = '\n'.join(asistentes_lines)

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Procesar asistentes
        asistentes_texto = self.cleaned_data.get('asistentes_texto', '').strip()
        if asistentes_texto:
            asistentes_list = []
            for linea in asistentes_texto.split('\n'):
                if linea.strip():
                    partes = [p.strip() for p in linea.split(' - ')]
                    if len(partes) >= 2:
                        asistente = {
                            'nombre': partes[0],
                            'rol': partes[1],
                            'presente': True,
                            'remoto': False
                        }
                        asistentes_list.append(asistente)
                    else:
                        asistente = {'nombre': linea.strip(), 'rol': 'Consejero', 'presente': True, 'remoto': False}
                        asistentes_list.append(asistente)
            instance.asistentes_json = asistentes_list if asistentes_list else None
        else:
            instance.asistentes_json = None
        
        # Procesar orden del día
        orden_dia_texto = self.cleaned_data.get('orden_dia_texto', '').strip()
        if orden_dia_texto:
            orden_list = []
            for i, linea in enumerate(orden_dia_texto.split('\n'), 1):
                if linea.strip():
                    if '. ' in linea:
                        numero_parte, resto = linea.split('. ', 1)
                        try:
                            numero = int(numero_parte)
                        except ValueError:
                            numero = i
                            resto = linea
                    else:
                        numero = i
                        resto = linea
                    
                    if ' - ' in resto:
                        titulo, descripcion = resto.split(' - ', 1)
                    else:
                        titulo = resto
                        descripcion = ''
                    
                    punto = {
                        'numero': numero,
                        'titulo': titulo.strip(),
                        'descripcion': descripcion.strip()
                    }
                    orden_list.append(punto)
            instance.orden_dia_json = orden_list if orden_list else None
        else:
            instance.orden_dia_json = None
        
        if commit:
            instance.save()
        return instance


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
            'eventos_incumplimiento': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'clausula_aceleracion': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'anexos': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'condicion_prepago': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'tipo_pago': forms.Select(attrs={'class': 'form-select'}),
            'periodicidad': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'prepago_permitido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tiene_garantia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set all fields with null=True, blank=True as not required
        optional_fields_defaults = {
            'acreedor_rfc': '',
            'deudor_rfc': '',
            'deudor_representante': '',
            'monto_numeric': None,
            'monto_literal': '',
            'moneda': 'Pesos Mexicanos',
            'concepto': '',
            'tipo_pago': 'unico',
            'num_pagos': None,
            'periodicidad': None,
            'lugar_pago': '',
            'forma_pago': '',
            'tasa_interes_ordinario': None,
            'base_intereses': 360,
            'tasa_interes_moratorio': None,
            'gastos_admon': 0,
            'impuestos': '',
            'dias_aviso_prepago': None,
            'condicion_prepago': '',
            'descripcion_garantia': '',
            'aval_nombre': '',
            'aval_domicilio': '',
            'eventos_incumplimiento': '',
            'clausula_aceleracion': '',
            'jurisdiccion': 'Ciudad de México',
            'ley_aplicable': 'Leyes de los Estados Unidos Mexicanos',
            'num_paginas': 1,
            'anexos': ''
        }
        
        for field_name, default_value in optional_fields_defaults.items():
            if field_name in self.fields:
                self.fields[field_name].required = False
        
        for field_name, field in self.fields.items():
            if field_name not in ['prepago_permitido', 'tiene_garantia']:
                if 'class' not in field.widget.attrs:
                    field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})


class EstatutosSociedadForm(forms.ModelForm):
    class Meta:
        model = EstatutosSociedad
        fields = [
            'denominacion', 'forma_legal', 'domicilio', 'nacionalidad',
            'objeto_social', 'duracion_indefinida', 'convenio_admision_extranjeros',
            'capital_fijo_monto', 'capital_fijo_texto', 'acciones_serie_a', 'capital_variable_ilimitado',
            'clase_acciones', 'libro_registro_acciones', 'derecho_preferencia',
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
            'objeto_social': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'clase_acciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
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
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})


class ContratoCreditoForm(forms.ModelForm):
    class Meta:
        model = ContratoCredito
        fields = [
            # Datos Generales
            'fecha_contrato', 'lugar_contrato',
            # Acreditante
            'acreditante_razon_social', 'acreditante_forma_legal', 'acreditante_representante',
            'acreditante_deed_constitucion_numero', 'acreditante_deed_constitucion_fecha', 'acreditante_notario_constitucion',
            'acreditante_registro_constitucion_folio', 'acreditante_deed_prom_inv_numero', 'acreditante_deed_prom_inv_fecha',
            'acreditante_notario_prom_inv', 'acreditante_registro_prom_inv_folio', 'acreditante_deed_poder_numero',
            'acreditante_deed_poder_fecha', 'acreditante_notario_poder',
            # Acreditado
            'acreditado_razon_social_original', 'acreditado_deed_constitucion_original_numero',
            'acreditado_deed_constitucion_original_fecha', 'acreditado_notario_constitucion_original',
            'acreditado_registro_constitucion_original_folio', 'acreditado_deed_denominacion_cambio_numero',
            'acreditado_deed_denominacion_cambio_fecha', 'acreditado_notario_denominacion_cambio',
            'acreditado_registro_denominacion_cambio_folio', 'acreditado_deed_poder_numero',
            'acreditado_deed_poder_fecha', 'acreditado_notario_poder', 'acreditado_resoluciones_unani_fecha',
            # Términos del Crédito
            'monto_credito', 'monto_credito_texto', 'numero_disposiciones',
            'disposicion1_fecha', 'disposicion1_importe', 'disposicion2_fecha', 'disposicion2_importe',
            'disposicion3_fecha', 'disposicion3_importe', 'plazo_credito_fecha_vencimiento',
            'pagos_intereses_fecha1', 'pagos_intereses_fecha2', 'pagos_intereses_fecha3', 'pago_principal_fecha',
            'tasa_interes_ordinaria', 'tasa_interes_moratoria',
            # Información Bancaria
            'banco_cuenta_numero', 'banco_nombre', 'banco_titular', 'banco_clabe',
            # Domicilios
            'domicilio_acreditante', 'domicilio_acreditado',
            # Jurisdicción
            'jurisdiccion', 'ley_aplicable',
            # Aval
            'aval_nombre', 'aval_domicilio',
            # Estado
            'estado'
        ]
        widgets = {
            # Campos de fecha
            'fecha_contrato': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'acreditante_deed_constitucion_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'acreditante_deed_prom_inv_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'acreditante_deed_poder_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'acreditado_deed_constitucion_original_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'acreditado_deed_denominacion_cambio_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'acreditado_deed_poder_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'acreditado_resoluciones_unani_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'disposicion1_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'disposicion2_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'disposicion3_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'plazo_credito_fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pagos_intereses_fecha1': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pagos_intereses_fecha2': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pagos_intereses_fecha3': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pago_principal_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # Campos numéricos
            'monto_credito': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'disposicion1_importe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'disposicion2_importe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'disposicion3_importe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasa_interes_ordinaria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasa_interes_moratoria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'numero_disposiciones': forms.NumberInput(attrs={'class': 'form-control'}),
            # Campos de texto largo
            'domicilio_acreditante': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'domicilio_acreditado': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'aval_domicilio': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            # Campos de selección
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            # Datos Generales
            'fecha_contrato': 'Fecha del Contrato',
            'lugar_contrato': 'Lugar del Contrato',
            # Acreditante
            'acreditante_razon_social': 'Razón Social del Acreditante',
            'acreditante_forma_legal': 'Forma Legal del Acreditante',
            'acreditante_representante': 'Representante del Acreditante',
            'acreditante_deed_constitucion_numero': 'Número de Escritura de Constitución',
            'acreditante_deed_constitucion_fecha': 'Fecha de Escritura de Constitución',
            'acreditante_notario_constitucion': 'Notario de Constitución',
            'acreditante_registro_constitucion_folio': 'Folio de Registro de Constitución',
            'acreditante_deed_prom_inv_numero': 'Número de Escritura S.A.P.I.',
            'acreditante_deed_prom_inv_fecha': 'Fecha de Escritura S.A.P.I.',
            'acreditante_notario_prom_inv': 'Notario S.A.P.I.',
            'acreditante_registro_prom_inv_folio': 'Folio de Registro S.A.P.I.',
            'acreditante_deed_poder_numero': 'Número de Escritura de Poder',
            'acreditante_deed_poder_fecha': 'Fecha de Escritura de Poder',
            'acreditante_notario_poder': 'Notario del Poder',
            # Acreditado
            'acreditado_razon_social_original': 'Razón Social del Acreditado',
            'acreditado_deed_constitucion_original_numero': 'Número de Escritura de Constitución Original',
            'acreditado_deed_constitucion_original_fecha': 'Fecha de Escritura de Constitución Original',
            'acreditado_notario_constitucion_original': 'Notario de Constitución Original',
            'acreditado_registro_constitucion_original_folio': 'Folio de Registro de Constitución Original',
            'acreditado_deed_denominacion_cambio_numero': 'Número de Escritura de Cambio de Denominación',
            'acreditado_deed_denominacion_cambio_fecha': 'Fecha de Escritura de Cambio de Denominación',
            'acreditado_notario_denominacion_cambio': 'Notario de Cambio de Denominación',
            'acreditado_registro_denominacion_cambio_folio': 'Folio de Registro de Cambio de Denominación',
            'acreditado_deed_poder_numero': 'Número de Escritura de Poder del Acreditado',
            'acreditado_deed_poder_fecha': 'Fecha de Escritura de Poder del Acreditado',
            'acreditado_notario_poder': 'Notario del Poder del Acreditado',
            'acreditado_resoluciones_unani_fecha': 'Fecha de Resoluciones Unánimes del Consejo',
            # Términos del Crédito
            'monto_credito': 'Monto del Crédito',
            'monto_credito_texto': 'Monto del Crédito (en texto)',
            'numero_disposiciones': 'Número de Disposiciones',
            'plazo_credito_fecha_vencimiento': 'Fecha de Vencimiento',
            'tasa_interes_ordinaria': 'Tasa de Interés Ordinaria (%)',
            'tasa_interes_moratoria': 'Tasa de Interés Moratoria (%)',
            # Información Bancaria
            'banco_cuenta_numero': 'Número de Cuenta',
            'banco_nombre': 'Nombre del Banco',
            'banco_titular': 'Titular de la Cuenta',
            'banco_clabe': 'CLABE Interbancaria',
            # Domicilios
            'domicilio_acreditante': 'Domicilio del Acreditante',
            'domicilio_acreditado': 'Domicilio del Acreditado',
            # Jurisdicción
            'jurisdiccion': 'Jurisdicción',
            'ley_aplicable': 'Ley Aplicable',
            # Aval
            'aval_nombre': 'Nombre del Aval',
            'aval_domicilio': 'Domicilio del Aval',
            # Estado
            'estado': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})


class EstatutosSociedadForm(forms.ModelForm):
    class Meta:
        model = EstatutosSociedad
        fields = [
            'denominacion', 'forma_legal', 'domicilio', 'nacionalidad',
            'objeto_social', 'duracion_indefinida', 'convenio_admision_extranjeros',
            'capital_fijo_monto', 'capital_fijo_texto', 'acciones_serie_a', 'capital_variable_ilimitado',
            'clase_acciones', 'libro_registro_acciones', 'derecho_preferencia',
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
            'objeto_social': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'clase_acciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
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
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})


class ContratoPrendaAccionesForm(forms.ModelForm):
    class Meta:
        model = ContratoPrendaAcciones
        fields = [
            # Campos visibles en el formulario
            'fecha_contrato', 'lugar_contrato', 'numero_fideicomiso', 'fecha_fideicomiso',
            'fecha_aprobacion_proyecto', 'descripcion_proyecto', 'deudor_nombre',
            'deudor_representante', 'acciones_pledged_cantidad', 'acciones_pledged_texto',
            'acreedor_nombre', 'delegado_fiduciario', 'fideicomitente_nombre',
            'fideicomitente_representante', 'domicilio_deudor', 'domicilio_acreedor',
            'domicilio_fideicomitente', 'estado',
            # Campos obligatorios ocultos (escrituras notariales)
            'deudor_constitucion_escritura_num', 'deudor_constitucion_fecha', 'deudor_constitucion_notario',
            'deudor_constitucion_registro', 'deudor_adopcion_sapi_escritura_num', 'deudor_adopcion_sapi_fecha',
            'deudor_adopcion_sapi_notario', 'deudor_adopcion_sapi_registro',
            'acreedor_constitucion_escritura_num', 'acreedor_constitucion_fecha', 'acreedor_constitucion_notario',
            'acreedor_constitucion_registro', 'delegado_fiduciario_escritura_num', 'delegado_fiduciario_fecha',
            'delegado_fiduciario_notario', 'delegado_fiduciario_registro',
            'fideicomitente_constitucion_escritura_num', 'fideicomitente_constitucion_fecha',
            'fideicomitente_constitucion_notario', 'fideicomitente_constitucion_registro',
            'fideicomitente_rep_escritura_num', 'fideicomitente_rep_fecha',
            'fideicomitente_rep_notario', 'fideicomitente_rep_registro'
        ]
        widgets = {
            # Widgets para campos visibles
            'fecha_contrato': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fideicomiso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_aprobacion_proyecto': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'acciones_pledged_cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion_proyecto': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'domicilio_deudor': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'domicilio_acreedor': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'domicilio_fideicomitente': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            # Widgets ocultos para campos obligatorios
            'deudor_constitucion_escritura_num': forms.HiddenInput(),
            'deudor_constitucion_fecha': forms.HiddenInput(),
            'deudor_constitucion_notario': forms.HiddenInput(),
            'deudor_constitucion_registro': forms.HiddenInput(),
            'deudor_adopcion_sapi_escritura_num': forms.HiddenInput(),
            'deudor_adopcion_sapi_fecha': forms.HiddenInput(),
            'deudor_adopcion_sapi_notario': forms.HiddenInput(),
            'deudor_adopcion_sapi_registro': forms.HiddenInput(),
            'acreedor_constitucion_escritura_num': forms.HiddenInput(),
            'acreedor_constitucion_fecha': forms.HiddenInput(),
            'acreedor_constitucion_notario': forms.HiddenInput(),
            'acreedor_constitucion_registro': forms.HiddenInput(),
            'delegado_fiduciario_escritura_num': forms.HiddenInput(),
            'delegado_fiduciario_fecha': forms.HiddenInput(),
            'delegado_fiduciario_notario': forms.HiddenInput(),
            'delegado_fiduciario_registro': forms.HiddenInput(),
            'fideicomitente_constitucion_escritura_num': forms.HiddenInput(),
            'fideicomitente_constitucion_fecha': forms.HiddenInput(),
            'fideicomitente_constitucion_notario': forms.HiddenInput(),
            'fideicomitente_constitucion_registro': forms.HiddenInput(),
            'fideicomitente_rep_escritura_num': forms.HiddenInput(),
            'fideicomitente_rep_fecha': forms.HiddenInput(),
            'fideicomitente_rep_notario': forms.HiddenInput(),
            'fideicomitente_rep_registro': forms.HiddenInput(),
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


class EstatutosSociedadForm(forms.ModelForm):
    class Meta:
        model = EstatutosSociedad
        fields = [
            'denominacion', 'forma_legal', 'domicilio', 'nacionalidad',
            'objeto_social', 'duracion_indefinida', 'convenio_admision_extranjeros',
            'capital_fijo_monto', 'capital_fijo_texto', 'acciones_serie_a', 'capital_variable_ilimitado',
            'clase_acciones', 'libro_registro_acciones', 'derecho_preferencia',
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
            'objeto_social': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'clase_acciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
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
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})


class ConvenioModificatorioForm(forms.ModelForm):
    class Meta:
        model = ConvenioModificatorio
        fields = [
            'fecha_convenio', 'lugar_convenio', 'inversionista_razon_social',
            'inversionista_representante', 'inversionista_constitucion_escritura', 'inversionista_constitucion_fecha',
            'inversionista_notario_constitucion', 'inversionista_registro_constitucion', 'inversionista_poder_escritura',
            'inversionista_poder_fecha', 'inversionista_poder_notario', 'contrato_original_fecha', 'estudiante_nombre',
            'estudiante_estado_civil', 'estudiante_nacionalidad', 'estudiante_ocupacion',
            'estudiante_rfc', 'estudiante_curp', 'adeudo_principal_anterior',
            'adeudo_principal_anterior_texto', 'credito_original', 'luis_nombre', 'luis_rfc', 'luis_curp',
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
            'inversionista_constitucion_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'inversionista_poder_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'contrato_original_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pagare_ii_fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dispo_periodo_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dispo_periodo_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'adeudo_principal_anterior': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'credito_original': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
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
            'inversionista_constitucion_escritura': 'Escritura de Constitución',
            'inversionista_constitucion_fecha': 'Fecha de Constitución',
            'inversionista_notario_constitucion': 'Notario de Constitución',
            'inversionista_registro_constitucion': 'Registro de Constitución',
            'inversionista_poder_escritura': 'Escritura de Poder',
            'inversionista_poder_fecha': 'Fecha de Poder',
            'inversionista_poder_notario': 'Notario del Poder',
            'contrato_original_fecha': 'Fecha del Contrato Original',
            'estudiante_nombre': 'Nombre del Estudiante',
            'estudiante_estado_civil': 'Estado Civil',
            'estudiante_nacionalidad': 'Nacionalidad',
            'estudiante_ocupacion': 'Ocupación',
            'estudiante_rfc': 'RFC del Estudiante',
            'estudiante_curp': 'CURP del Estudiante',
            'adeudo_principal_anterior': 'Adeudo Principal Anterior',
            'adeudo_principal_anterior_texto': 'Adeudo Anterior (en texto)',
            'credito_original': 'Crédito Original',
            'luis_nombre': 'Nombre de Obligado 1',
            'luis_rfc': 'RFC de Obligado 1',
            'luis_curp': 'CURP de Obligado 1',
            'lizette_nombre': 'Nombre de Obligado 2',
            'lizette_rfc': 'RFC de Obligado 2',
            'lizette_curp': 'CURP de Obligado 2',
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


class EstatutosSociedadForm(forms.ModelForm):
    class Meta:
        model = EstatutosSociedad
        fields = [
            'denominacion', 'forma_legal', 'domicilio', 'nacionalidad',
            'objeto_social', 'duracion_indefinida', 'convenio_admision_extranjeros',
            'capital_fijo_monto', 'capital_fijo_texto', 'acciones_serie_a', 'capital_variable_ilimitado',
            'clase_acciones', 'libro_registro_acciones', 'derecho_preferencia',
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
            'objeto_social': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'clase_acciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
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
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})




class EstatutosSociedadForm(forms.ModelForm):
    class Meta:
        model = EstatutosSociedad
        fields = [
            'denominacion', 'forma_legal', 'domicilio', 'nacionalidad',
            'objeto_social', 'duracion_indefinida', 'convenio_admision_extranjeros',
            'capital_fijo_monto', 'capital_fijo_texto', 'acciones_serie_a', 'capital_variable_ilimitado',
            'clase_acciones', 'libro_registro_acciones', 'derecho_preferencia',
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
            'objeto_social': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'clase_acciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
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
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})
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


class EstatutosSociedadForm(forms.ModelForm):
    class Meta:
        model = EstatutosSociedad
        fields = [
            'denominacion', 'forma_legal', 'domicilio', 'nacionalidad',
            'objeto_social', 'duracion_indefinida', 'convenio_admision_extranjeros',
            'capital_fijo_monto', 'capital_fijo_texto', 'acciones_serie_a', 'capital_variable_ilimitado',
            'clase_acciones', 'libro_registro_acciones', 'derecho_preferencia',
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
            'objeto_social': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'clase_acciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
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
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            field.widget.attrs.update({'id': f'id_{field_name}'})
