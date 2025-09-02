from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Importamos el modelo EstatutosSociedad
from .estatutos_sociedad import EstatutosSociedad

class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documentos'

class ActaAsamblea(models.Model):
    TIPO_ASAMBLEA = [
        ('ordinaria', 'Ordinaria'),
        ('extraordinaria', 'Extraordinaria'),
        ('mixta', 'Mixta'),
    ]
    METODO_VOTACION = [
        ('economica', 'Económica'),
        ('nominal', 'Nominal'),
        ('por_accion', 'Por Acción'),
    ]
    ESTADO = [
        ('borrador', 'Borrador'),
        ('aprobada', 'Aprobada'),
        ('firmada', 'Firmada'),
    ]

    # Relación con usuario (mantenemos compatibilidad)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Core
    razon_social = models.CharField(max_length=255)
    tipo_asamblea = models.CharField(max_length=20, choices=TIPO_ASAMBLEA)
    caracter = models.CharField(max_length=100, blank=True)  # "General de Accionistas", etc.
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_cierre = models.TimeField(null=True, blank=True)
    lugar = models.TextField()

    porcentaje_capital_presente = models.DecimalField(
        max_digits=6, decimal_places=3,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    convocatoria_omitida = models.BooleanField(default=False)
    fundamento_convocatoria = models.TextField(blank=True)

    presidente = models.CharField(max_length=255)
    secretario = models.CharField(max_length=255)
    escrutador = models.CharField(max_length=255, blank=True)
    comisario = models.CharField(max_length=255, blank=True)

    metodo_votacion_general = models.CharField(max_length=20, choices=METODO_VOTACION, default='economica')

    # JSON blocks (usar JSONField nativo en Django 3.1+)
    asistentes_json = models.JSONField(null=True, blank=True)
    orden_dia_json = models.JSONField(null=True, blank=True)
    resoluciones_json = models.JSONField(null=True, blank=True)
    nombramientos_json = models.JSONField(null=True, blank=True)
    dividendos_json = models.JSONField(null=True, blank=True)
    delegados_json = models.JSONField(null=True, blank=True)
    anexos_json = models.JSONField(null=True, blank=True)

    estado = models.CharField(max_length=20, choices=ESTADO, default='borrador')

    acta_html_cache = models.TextField(blank=True)  # Versión congelada al firmar

    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Acta de Asamblea"
        verbose_name_plural = "Actas de Asambleas"
        ordering = ['-fecha', '-creada_en']

    def __str__(self):
        return f"{self.get_tipo_asamblea_display()} {self.razon_social} {self.fecha}"
    
    def get_absolute_url(self):
        return reverse('documentos:detalle', kwargs={'pk': self.pk})
    
    def get_estado_badge_class(self):
        """Retorna la clase CSS para el badge del estado"""
        classes = {
            'borrador': 'bg-secondary',
            'aprobada': 'bg-success',
            'firmada': 'bg-primary',
        }
        return classes.get(self.estado, 'bg-secondary')

    # Helpers opcionales
    def duracion_minutos(self):
        if self.hora_inicio and self.hora_cierre:
            from datetime import datetime
            dt_i = datetime.combine(self.fecha, self.hora_inicio)
            dt_f = datetime.combine(self.fecha, self.hora_cierre)
            return int((dt_f - dt_i).total_seconds() / 60)
        return None


class ActaSesionConsejo(models.Model):
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('aprobada', 'Aprobada'),
        ('firmada', 'Firmada'),
    ]
    METODO_INSTALACION = [
        ('mayoria', 'Mayoría'),
        ('unanimidad', 'Unanimidad'),
    ]

    # Relación con usuario (mantenemos compatibilidad)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # --- Datos básicos ---
    razon_social       = models.CharField(max_length=255, help_text="Nombre completo de la sociedad")
    organo             = models.CharField(max_length=50, default='Consejo de Administración', editable=False)
    fecha              = models.DateField()
    hora_inicio        = models.TimeField()
    hora_cierre        = models.TimeField(null=True, blank=True)
    lugar              = models.TextField(help_text="Dirección física o link de Zoom")
    ciudad             = models.CharField(max_length=100, default='México')
    plataforma_remota  = models.CharField(max_length=100, default='Zoom')
    abreviatura_sociedad = models.CharField(max_length=100, default='CAS')
    convocatoria_realizada = models.BooleanField(
        default=True,
        #help_text="Indica si hubo convocatoria formal (si es False, espera anexo_convocatoria)"
    )
    anexo_convocatoria = models.JSONField(
        null=True, blank=True,
        help_text="[{ 'tipo':'Convocatoria','archivo':'URL o referencia interna' }]"
    )

    # --- Quórum / Constitución ---
    porcentaje_miembros_presentes = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Porcentaje de consejeros presentes",
        null=True, blank=True, default=100.00
    )
    metodo_instalacion = models.CharField(
        max_length=20, choices=METODO_INSTALACION,
        default='mayoria',
        help_text="Cómo se declaró instalada la sesión",
        null=True, blank=True
    )

    # --- Mesa directiva ---
    presidente = models.CharField(max_length=255)
    secretario = models.CharField(max_length=255)

    # --- JSONFields para secciones dinámicas ---
    asistentes_json   = models.JSONField(
        null=True, blank=True,
        help_text="""
        [
          { "nombre":"Daniel Martínez", "rol":"Consejero", "presente":true, "remoto":false },
          { "nombre":"Luis Hernández",  "rol":"Consejero", "presente":true, "remoto":true }
        ]
        """
    )
    invitados_json    = models.JSONField(
        null=True, blank=True,
        help_text="""
        [
          { "nombre":"Ángel Nieblas", "cargo":"Contador Público" },
          { "nombre":"Ramona Sánchez", "cargo":"Invitada" }
        ]
        """
    )
    orden_dia_json    = models.JSONField(
        null=True, blank=True,
        help_text="""
        [
          { "numero":1, "titulo":"Perspectivas políticas y económicas",    "descripcion":"" },
          { "numero":2, "titulo":"Informe Director General y estados fin.", "descripcion":"" }
        ]
        """
    )
    resoluciones_json = models.JSONField(
        null=True, blank=True,
        help_text="""
        [
          { "punto":1, "clave":"Única",  "texto":"Se toma nota…",         "tipo":"toma_nota" },
          { "punto":2, "clave":"II.1",   "texto":"Se aprueba el informe…","tipo":"aprobacion_informe" }
        ]
        """
    )
    delegados_json     = models.JSONField(
        null=True, blank=True,
        help_text="""
        [
          { "nombre":"Alfonso Arellano", "facultades":"Protocolizar el acta" },
          { "nombre":"Ramona Sánchez",   "facultades":"Cumplir resoluciones" }
        ]
        """
    )
    anexos_json       = models.JSONField(
        null=True, blank=True,
        help_text="""
        [
          { "numero":1, "titulo":"Lista de asistencia" },
          { "numero":2, "titulo":"Convocatoria" },
          { "numero":3, "titulo":"Presentación Director General" },
          { "numero":4, "titulo":"CIM Expansión Sol I" }
        ]
        """
    )

    # --- Control de estado & caching ---
    estado       = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    html_cache   = models.TextField(blank=True, help_text="HTML congelado al firmar/aprobar")

    creada_en    = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Acta de Sesión de Consejo"
        verbose_name_plural = "Actas de Sesiones de Consejo"
        ordering = ['-fecha', '-creada_en']

    def __str__(self):
        return f"Sesión {self.fecha} — {self.razon_social}"

    def get_absolute_url(self):
        return reverse('documentos:detalle_consejo', kwargs={'pk': self.pk})
    
    def get_estado_badge_class(self):
        """Retorna la clase CSS para el badge del estado"""
        classes = {
            'borrador': 'bg-secondary',
            'aprobada': 'bg-success',
            'firmada': 'bg-primary',
        }
        return classes.get(self.estado, 'bg-secondary')

    def duracion_minutos(self):
        """Calcula minutos de sesión si existe hora_cierre."""
        if self.hora_inicio and self.hora_cierre:
            from datetime import datetime
            inicio = datetime.combine(self.fecha, self.hora_inicio)
            cierre = datetime.combine(self.fecha, self.hora_cierre)
            return int((cierre - inicio).total_seconds() / 60)
        return None


class Pagare(models.Model):
    # 1. Encabezado
    lugar_emision = models.CharField("Lugar de emisión", max_length=200)
    fecha_emision = models.DateField("Fecha de emisión")

    # 2. Acreedor
    acreedor_nombre = models.CharField("Nombre o razón social del Acreedor", max_length=200)
    acreedor_domicilio = models.TextField("Domicilio del Acreedor")
    acreedor_rfc = models.CharField("RFC del Acreedor", max_length=13, blank=True)

    # 3. Deudor
    deudor_nombre = models.CharField("Nombre completo del Deudor", max_length=200)
    deudor_domicilio = models.TextField("Domicilio del Deudor")
    deudor_rfc = models.CharField("RFC del Deudor", max_length=13, blank=True)
    deudor_representante = models.CharField("Representante legal", max_length=200, blank=True)

    # 4. Monto y objeto
    monto_numeric = models.DecimalField("Monto principal", max_digits=12, decimal_places=2, null=True, blank=True)
    monto_literal = models.CharField("Monto en letras", max_length=300, null=True, blank=True)
    moneda = models.CharField("Moneda", max_length=50, default="Pesos Mexicanos", null=True, blank=True)
    concepto = models.CharField("Concepto del pagaré", max_length=200, help_text="Ej. Préstamo personal, colegiaturas, etc.", null=True, blank=True)

    # 5. Condiciones de pago
    TIPO_PAGO_CHOICES = [
        ('unico', 'Un solo pago'),
        ('parcialidades', 'Parcialidades'),
    ]
    tipo_pago = models.CharField("Tipo de pago", max_length=20, choices=TIPO_PAGO_CHOICES, null=True, blank=True)
    num_pagos = models.PositiveIntegerField("Número de pagos", null=True, blank=True)
    PERIODICIDAD_CHOICES = [
        ('mensual', 'Mensual'),
        ('quincenal', 'Quincenal'),
        ('semanal', 'Semanal'),
        ('diario', 'Diario'),
    ]
    periodicidad = models.CharField("Periodicidad", max_length=20, choices=PERIODICIDAD_CHOICES, null=True, blank=True)
    lugar_pago = models.CharField("Lugar de pago", max_length=200, null=True, blank=True)
    forma_pago = models.CharField("Forma de pago", max_length=100, help_text="Ej. transferencia, efectivo, cheque", null=True, blank=True)

    # 6. Intereses y cargos
    tasa_interes_ordinario = models.DecimalField("Tasa de interés ordinario (%)", max_digits=5, decimal_places=2, null=True, blank=True)
    base_intereses = models.PositiveIntegerField("Base de cálculo de intereses (días)", default=360, null=True, blank=True)
    tasa_interes_moratorio = models.DecimalField("Tasa de interés moratorio (%)", max_digits=5, decimal_places=2, null=True, blank=True)
    gastos_admon = models.DecimalField("Gastos de administración", max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    impuestos = models.CharField("Impuestos aplicables", max_length=200, blank=True)

    # 7. Prepago
    prepago_permitido = models.BooleanField("Permitir prepago", default=False)
    dias_aviso_prepago = models.PositiveIntegerField("Días de aviso para prepago", null=True, blank=True)
    condicion_prepago = models.CharField("Condición de prepago", max_length=200, blank=True)

    # 8. Garantías y avales
    tiene_garantia = models.BooleanField("Tiene garantía o aval", default=False)
    descripcion_garantia = models.TextField("Descripción de la garantía", blank=True)
    aval_nombre = models.CharField("Nombre del Aval", max_length=200, blank=True)
    aval_domicilio = models.TextField("Domicilio del Aval", blank=True)

    # 9. Jurídico
    eventos_incumplimiento = models.TextField("Eventos de incumplimiento", default="", blank=True)
    clausula_aceleracion = models.TextField("Cláusula de aceleración", default="", blank=True)
    jurisdiccion = models.CharField("Jurisdicción", max_length=200, default="Ciudad de México", blank=True)
    ley_aplicable = models.CharField("Ley aplicable", max_length=200, default="Leyes de los Estados Unidos Mexicanos", blank=True)

    # 10. Anexos
    num_paginas = models.PositiveIntegerField("Número total de páginas", default=1, null=True, blank=True)
    anexos = models.TextField("Anexos", blank=True)

    # 11. Tabla de amortización (datos integrados)
    tabla_amortizacion = models.JSONField("Tabla de amortización", null=True, blank=True, 
                                        help_text="Formato: [{\"numero\": 1, \"fecha\": \"2025-08-01\", \"capital\": 1000.00, \"saldo\": 9000.00, \"costo_admon\": 50.00, \"iva_costo_admon\": 8.00, \"interes\": 100.00, \"iva_interes\": 16.00, \"total\": 1174.00, \"estado\": \"pendiente\", \"fecha_pago_real\": null}]")

    # Campos de control
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pagares')
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('emitido', 'Emitido'),
        ('firmado', 'Firmado'),
        ('pagado', 'Pagado'),
        ('vencido', 'Vencido'),
    ]
    estado = models.CharField("Estado", max_length=20, choices=ESTADO_CHOICES, default='borrador')
    html_cache = models.TextField("HTML generado", blank=True)
    fecha_creacion = models.DateTimeField("Fecha de creación", auto_now_add=True)
    fecha_actualizacion = models.DateTimeField("Fecha de actualización", auto_now=True)

    class Meta:
        verbose_name = "Pagaré"
        verbose_name_plural = "Pagarés"
        ordering = ['-fecha_emision', '-fecha_creacion']

    def __str__(self):
        return f"Pagaré #{self.id} - {self.deudor_nombre}"
    
    def get_absolute_url(self):
        return reverse('documentos:detalle_pagare', kwargs={'pk': self.pk})
    
    def get_estado_badge_class(self):
        """Retorna la clase CSS para el badge del estado"""
        classes = {
            'borrador': 'bg-secondary',
            'emitido': 'bg-info',
            'firmado': 'bg-primary',
            'pagado': 'bg-success',
            'vencido': 'bg-danger',
        }
        return classes.get(self.estado, 'bg-secondary')
    
    def agregar_cuota(self, numero, fecha, capital, saldo, costo_admon=0, iva_costo_admon=0, 
                     interes=0, iva_interes=0, estado='pendiente', fecha_pago_real=None):
        """Agrega una cuota a la tabla de amortización"""
        if self.tabla_amortizacion is None:
            self.tabla_amortizacion = []
            
        total = capital + costo_admon + iva_costo_admon + interes + iva_interes
        
        nueva_cuota = {
            "numero": numero,
            "fecha": fecha.isoformat() if isinstance(fecha, date) else fecha,
            "capital": float(capital),
            "saldo": float(saldo),
            "costo_admon": float(costo_admon),
            "iva_costo_admon": float(iva_costo_admon),
            "interes": float(interes),
            "iva_interes": float(iva_interes),
            "total": float(total),
            "estado": estado,
            "fecha_pago_real": fecha_pago_real.isoformat() if fecha_pago_real and isinstance(fecha_pago_real, date) else fecha_pago_real
        }
        
        self.tabla_amortizacion.append(nueva_cuota)
        self.save()
        
    def actualizar_estado_cuota(self, numero_cuota, nuevo_estado, fecha_pago_real=None):
        """Actualiza el estado de una cuota específica"""
        if not self.tabla_amortizacion:
            return False
            
        for i, cuota in enumerate(self.tabla_amortizacion):
            if cuota["numero"] == numero_cuota:
                self.tabla_amortizacion[i]["estado"] = nuevo_estado
                if fecha_pago_real:
                    self.tabla_amortizacion[i]["fecha_pago_real"] = fecha_pago_real.isoformat() if isinstance(fecha_pago_real, date) else fecha_pago_real
                self.save()
                return True
                
        return False
        
    def obtener_cuotas(self):
        """Retorna la tabla de amortización ordenada por número de cuota"""
        if not self.tabla_amortizacion:
            return []
            
        return sorted(self.tabla_amortizacion, key=lambda x: x["numero"])
        
    def calcular_total_pagado(self):
        """Calcula el total pagado hasta el momento"""
        if not self.tabla_amortizacion:
            return 0
            
        return sum(cuota["total"] for cuota in self.tabla_amortizacion if cuota["estado"] == "pagado")
        
    def calcular_saldo_pendiente(self):
        """Calcula el saldo pendiente de pago"""
        if not self.tabla_amortizacion:
            return self.monto_numeric
            
        cuotas_pagadas = [c for c in self.tabla_amortizacion if c["estado"] == "pagado"]
        if not cuotas_pagadas:
            return self.monto_numeric
            
        ultima_cuota_pagada = max(cuotas_pagadas, key=lambda x: x["numero"])
        return ultima_cuota_pagada["saldo"]
    
    def generar_tabla_amortizacion_automatica(self):
        """Tabla de amortización (Sistema Francés) con PAGO TOTAL CONSTANTE
        incluyendo IVA del interés.
        - La cuota fija 'cuota_base_eff' se calcula con una tasa efectiva i*(1+IVA).
        - En cada periodo: capital = cuota_base_eff - (interés + IVA_interés).
        - El Pago Total = cuota_base_eff + gastos + IVA_gastos (constante).
        - En la última cuota se ajusta capital por redondeos para cerrar saldo=0.00.
        """
        from datetime import timedelta
        from dateutil.relativedelta import relativedelta

        # Requisitos mínimos
        if not all([self.monto_numeric, self.num_pagos, self.tasa_interes_ordinario, self.fecha_emision]):
            return []

        # Parámetros base
        P = float(self.monto_numeric)
        n = int(self.num_pagos)
        tasa_anual = float(self.tasa_interes_ordinario) / 100.0
        fecha_inicio = self.fecha_emision

        # Periodicidad -> tasa por periodo y delta de fecha
        per = (self.periodicidad or "mensual").lower()
        if per == "quincenal":
            i = tasa_anual / 24.0
            delta = timedelta(days=15)
        elif per == "semanal":
            i = tasa_anual / 52.0
            delta = timedelta(weeks=1)
        else:  # mensual (default)
            i = tasa_anual / 12.0
            delta = relativedelta(months=1)

        # IVA
        IVA = 0.16

        # Gastos por periodo (si guardas TOTAL del crédito, cambia a / n)
        costo_admon = float(self.gastos_admon) if getattr(self, "gastos_admon", None) else 350.00
        # Si self.gastos_admon fuera TOTAL del crédito:
        # costo_admon = (float(self.gastos_admon) / n) if getattr(self, "gastos_admon", None) else 350.00
        iva_costo_admon = round(costo_admon * IVA, 2)

        # --- CUOTA que incluye IVA del interés ---
        # Usamos tasa efectiva por periodo: i_eff = i * (1 + IVA)
        i_eff = i * (1.0 + IVA)

        if i_eff > 0:
            cuota_base_eff = P * (i_eff * (1 + i_eff) ** n) / ((1 + i_eff) ** n - 1)
        else:
            cuota_base_eff = P / n

        # Pago total fijo (incluye gastos + IVA gastos)
        pago_total_const = round(cuota_base_eff + costo_admon + iva_costo_admon, 2)

        tabla = []
        saldo = P
        residuo_cap = 0.0  # acumula centavos por redondeo

        for k in range(1, n + 1):
            # Fecha de pago
            if per == "quincenal":
                fecha_pago = fecha_inicio + timedelta(days=15 * k)
            elif per == "semanal":
                fecha_pago = fecha_inicio + timedelta(weeks=k)
            else:
                fecha_pago = fecha_inicio + relativedelta(months=k)

            # Interés del periodo (sin IVA)
            interes = saldo * i
            iva_interes = interes * IVA

            # Capital como residuo de la CUOTA EFECTIVA (que ya considera IVA del interés)
            capital_teorico = cuota_base_eff - (interes + iva_interes)
            capital = round(capital_teorico, 2)
            residuo_cap += (capital_teorico - capital)

            # En la última cuota: ajustar capital para cerrar saldo = 0.00 (sin tocar el pago total)
            if k == n:
                ajuste = saldo - capital
                capital = round(capital + ajuste + residuo_cap, 2)

            # Redondeos para la fila
            interes = round(interes, 2)
            iva_interes = round(iva_interes, 2)

            # Pago total (constante por diseño)
            total = pago_total_const

            # Nuevo saldo
            nuevo_saldo = round(max(0.0, saldo - capital), 2)

            tabla.append({
                "numero": k,
                "fecha": fecha_pago.strftime("%d/%m/%Y"),
                "capital": capital,
                "saldo": nuevo_saldo,
                "costo_admon": round(costo_admon, 2),
                "iva_costo_admon": round(iva_costo_admon, 2),
                "interes": interes,
                "iva_interes": iva_interes,
                "total": total,  # constante e incluye IVA del interés
                "estado": "pendiente",
                "fecha_pago_real": None,
                "etapa": "Etapa de Estudios" if k <= n * 0.8 else "Etapa de Egreso",
            })

            saldo = nuevo_saldo

        return tabla

        """Genera automáticamente la tabla de amortización basada en los datos del pagaré"""
        # from datetime import datetime, timedelta
        # from dateutil.relativedelta import relativedelta
        # import math
        
        # if not all([self.monto_numeric, self.num_pagos, self.tasa_interes_ordinario, self.fecha_emision]):
        #     return []
        
        # # Parámetros base
        # monto_principal = float(self.monto_numeric)
        # num_pagos = self.num_pagos
        # tasa_anual = float(self.tasa_interes_ordinario) / 100
        # fecha_inicio = self.fecha_emision
        
        # # Calcular periodicidad
        # if self.periodicidad == 'mensual':
        #     tasa_periodo = tasa_anual / 12
        #     delta_periodo = relativedelta(months=1)
        # elif self.periodicidad == 'quincenal':
        #     tasa_periodo = tasa_anual / 24
        #     delta_periodo = timedelta(days=15)
        # elif self.periodicidad == 'semanal':
        #     tasa_periodo = tasa_anual / 52
        #     delta_periodo = timedelta(weeks=1)
        # else:  # mensual por defecto
        #     tasa_periodo = tasa_anual / 12
        #     delta_periodo = relativedelta(months=1)
        
        # # Calcular pago fijo (sistema francés)
        # if tasa_periodo > 0:
        #     pago_fijo = monto_principal * (tasa_periodo * (1 + tasa_periodo)**num_pagos) / ((1 + tasa_periodo)**num_pagos - 1)
        # else:
        #     pago_fijo = monto_principal / num_pagos
        
        # # Generar tabla
        # tabla = []
        # saldo_insoluto = monto_principal
        # fecha_actual = fecha_inicio
        
        # # Gastos fijos por pago
        # costo_admon = float(self.gastos_admon or 0) / num_pagos if self.gastos_admon else 350.00
        # iva_costo_admon = costo_admon * 0.16  # 16% IVA
        
        # for i in range(1, num_pagos + 1):
        #     # Calcular fecha de pago
        #     if self.periodicidad == 'mensual':
        #         fecha_pago = fecha_inicio + relativedelta(months=i)
        #     elif self.periodicidad == 'quincenal':
        #         fecha_pago = fecha_inicio + timedelta(days=15 * i)
        #     elif self.periodicidad == 'semanal':
        #         fecha_pago = fecha_inicio + timedelta(weeks=i)
        #     else:
        #         fecha_pago = fecha_inicio + relativedelta(months=i)
            
        #     # Calcular intereses sobre saldo insoluto
        #     interes_ordinario = saldo_insoluto * tasa_periodo
        #     iva_interes = interes_ordinario * 0.16  # 16% IVA
            
        #     # Calcular capital (último pago ajusta el saldo restante)
        #     if i == num_pagos:
        #         capital = saldo_insoluto
        #     else:
        #         capital = pago_fijo - interes_ordinario
        #         if capital < 0:
        #             capital = 0
            
        #     # Calcular total del pago
        #     pago_total = capital + costo_admon + iva_costo_admon + interes_ordinario + iva_interes
            
        #     # Actualizar saldo
        #     nuevo_saldo = max(0, saldo_insoluto - capital)
            
        #     # Agregar cuota a la tabla
        #     cuota = {
        #         "numero": i,
        #         "fecha": fecha_pago.strftime("%d/%m/%Y"),
        #         "capital": round(capital, 2),
        #         "saldo": round(nuevo_saldo, 2),
        #         "costo_admon": round(costo_admon, 2),
        #         "iva_costo_admon": round(iva_costo_admon, 2),
        #         "interes": round(interes_ordinario, 2),
        #         "iva_interes": round(iva_interes, 2),
        #         "total": round(pago_total, 2),
        #         "estado": "pendiente",
        #         "fecha_pago_real": None,
        #         "etapa": "Etapa de Estudios" if i <= num_pagos * 0.8 else "Etapa de Egreso"
        #     }
            
        #     tabla.append(cuota)
        #     saldo_insoluto = nuevo_saldo
        
        # return tabla


class ContratoCredito(models.Model):
    # --- Datos Generales del Contrato ---
    fecha_contrato = models.DateField(help_text="Fecha en que se firma el contrato")
    lugar_contrato = models.CharField(max_length=100, default="Ciudad de México")
    
    # --- Parte Acreditante ---
    acreditante_razon_social = models.CharField(max_length=200)
    acreditante_forma_legal = models.CharField(max_length=100, default="S.A.P.I. de C.V.")
    acreditante_representante = models.CharField(max_length=200)
    # Constitución original
    acreditante_deed_constitucion_numero = models.CharField(max_length=50)
    acreditante_deed_constitucion_fecha = models.DateField()
    acreditante_notario_constitucion = models.CharField(max_length=150)
    acreditante_registro_constitucion_folio = models.CharField(max_length=50)
    # Cambio a S.A.P.I.
    acreditante_deed_prom_inv_numero = models.CharField(max_length=50)
    acreditante_deed_prom_inv_fecha = models.DateField()
    acreditante_notario_prom_inv = models.CharField(max_length=150)
    acreditante_registro_prom_inv_folio = models.CharField(max_length=50)
    # Poder del representante
    acreditante_deed_poder_numero = models.CharField(max_length=50)
    acreditante_deed_poder_fecha = models.DateField()
    acreditante_notario_poder = models.CharField(max_length=150)
    
    # --- Parte Acreditado ---
    acreditado_razon_social_original = models.CharField(max_length=200)
    acreditado_deed_constitucion_original_numero = models.CharField(max_length=50)
    acreditado_deed_constitucion_original_fecha = models.DateField()
    acreditado_notario_constitucion_original = models.CharField(max_length=150)
    acreditado_registro_constitucion_original_folio = models.CharField(max_length=50)
    # Cambio de denominación social
    acreditado_deed_denominacion_cambio_numero = models.CharField(max_length=50)
    acreditado_deed_denominacion_cambio_fecha = models.DateField()
    acreditado_notario_denominacion_cambio = models.CharField(max_length=150)
    acreditado_registro_denominacion_cambio_folio = models.CharField(max_length=50)
    # Poder del representante
    acreditado_deed_poder_numero = models.CharField(max_length=50)
    acreditado_deed_poder_fecha = models.DateField()
    acreditado_notario_poder = models.CharField(max_length=150)
    # Resoluciones del consejo
    acreditado_resoluciones_unani_fecha = models.DateField(help_text="Fecha de las resoluciones unánimes del consejo")
    
    # --- Términos del Crédito ---
    monto_credito = models.DecimalField(max_digits=14, decimal_places=2, help_text="Monto total del crédito en MXN")  # SEGUNDA.- Objeto
    monto_credito_texto = models.CharField(max_length=200, help_text="Monto en texto (p.ej. \"Nueve millones de pesos 00/100 Moneda Nacional\")")
    numero_disposiciones = models.IntegerField(default=3)
    disposicion1_fecha = models.DateField()
    disposicion1_importe = models.DecimalField(max_digits=14, decimal_places=2)
    disposicion2_fecha = models.DateField()
    disposicion2_importe = models.DecimalField(max_digits=14, decimal_places=2)
    disposicion3_fecha = models.DateField()
    disposicion3_importe = models.DecimalField(max_digits=14, decimal_places=2)
    
    plazo_credito_fecha_vencimiento = models.DateField(help_text="Fecha de vencimiento del crédito")  # Cláusula Cuarta
    # Fechas de pago de intereses
    pagos_intereses_fecha1 = models.DateField()
    pagos_intereses_fecha2 = models.DateField()
    pagos_intereses_fecha3 = models.DateField()
    # Pago de principal
    pago_principal_fecha = models.DateField(help_text="Fecha de pago de principal")  # Cláusula Quinta & Sexta
    
    # Tasas de interés
    tasa_interes_ordinaria = models.DecimalField(max_digits=5, decimal_places=2, help_text="Tasa anual (%) de interés ordinario")  # 25%
    tasa_interes_moratoria = models.DecimalField(max_digits=5, decimal_places=2, help_text="Tasa anual (%) de interés moratorio")  # 36%
    
    # Cuenta para pagos
    banco_cuenta_numero = models.CharField(max_length=30)
    banco_nombre = models.CharField(max_length=150)
    banco_titular = models.CharField(max_length=200)
    banco_clabe = models.CharField(max_length=18)
    
    # Domicilios para notificaciones
    domicilio_acreditante = models.TextField()
    domicilio_acreditado = models.TextField()
    
    # Derecho aplicable y jurisdicción
    jurisdiccion = models.CharField(max_length=200, default="Tribunales de la Ciudad de México")
    ley_aplicable = models.CharField(max_length=200, default="Leyes de los Estados Unidos Mexicanos")
    
    # --- Datos del Aval (Anexo 1: Pagaré) ---
    aval_nombre = models.CharField(max_length=200)
    aval_domicilio = models.TextField()
    
    # --- Campos de control ---
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contratos_credito')
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('emitido', 'Emitido'),
        ('firmado', 'Firmado'),
        ('vigente', 'Vigente'),
        ('vencido', 'Vencido'),
        ('pagado', 'Pagado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    html_cache = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Contrato de Crédito"
        verbose_name_plural = "Contratos de Crédito"
        ordering = ['-fecha_contrato', '-fecha_creacion']
    
    def __str__(self):
        return f"Contrato {self.id} - {self.acreditado_razon_social_original} / {self.acreditante_razon_social}"
    
    def get_absolute_url(self):
        return reverse('documentos:detalle_contrato_credito', kwargs={'pk': self.pk})
    
    def get_estado_badge_class(self):
        """Retorna la clase CSS para el badge del estado"""
        classes = {
            'borrador': 'bg-secondary',
            'emitido': 'bg-info',
            'firmado': 'bg-primary',
            'vigente': 'bg-success',
            'vencido': 'bg-danger',
            'pagado': 'bg-success',
        }
        return classes.get(self.estado, 'bg-secondary')


class ContratoPrendaAcciones(models.Model):
    # — Datos Generales del Contrato —
    fecha_contrato = models.DateField(help_text="Fecha de firma del contrato")  # Ej. 2025-06-01
    lugar_contrato = models.CharField(max_length=200, help_text="Lugar de firma del contrato")

    # — Fideicomiso —
    numero_fideicomiso = models.CharField(max_length=20, help_text="Número del fideicomiso")  # Ej. "1051"
    fecha_fideicomiso = models.DateField(help_text="Fecha de constitución del fideicomiso")  # Ej. 2022-05-12

    # — Proyecto aprobado por Comité Técnico —
    fecha_aprobacion_proyecto = models.DateField(help_text="Fecha de aprobación del proyecto")  # Ej. 2022-05-31
    descripcion_proyecto = models.TextField(help_text="Descripción del proyecto aprobado")

    # — Deudor Prendario —
    deudor_nombre = models.CharField(max_length=200, default="Finanzas, S.A.P.I. de C.V.")
    deudor_constitucion_escritura_num = models.CharField(max_length=50, help_text="Número de escritura de constitución")
    deudor_constitucion_fecha = models.DateField(help_text="Fecha de escritura de constitución")
    deudor_constitucion_notario = models.CharField(max_length=200, help_text="Notario y número")
    deudor_constitucion_registro = models.CharField(max_length=100, help_text="Folio en Registro Público")

    deudor_adopcion_sapi_escritura_num = models.CharField(max_length=50, help_text="Escritura de adopción S.A.P.I.")
    deudor_adopcion_sapi_fecha = models.DateField(help_text="Fecha de escritura de adopción S.A.P.I.")
    deudor_adopcion_sapi_notario = models.CharField(max_length=200)
    deudor_adopcion_sapi_registro = models.CharField(max_length=100)

    deudor_representante = models.CharField(max_length=200, help_text="Nombre del apoderado legal")  # Ej. Raúl García

    acciones_pledged_cantidad = models.BigIntegerField(help_text="Cantidad de acciones pignoradas")  # Ej. 5853796
    acciones_pledged_texto = models.CharField(max_length=200, help_text="Texto de las acciones (en palabras)")

    # — Acreedor Prendario (Fiduciario) —
    acreedor_nombre = models.CharField(max_length=200, default="Casa de Bolsa, S.A. de C.V.")
    acreedor_constitucion_escritura_num = models.CharField(max_length=50)
    acreedor_constitucion_fecha = models.DateField()
    acreedor_constitucion_notario = models.CharField(max_length=200)
    acreedor_constitucion_registro = models.CharField(max_length=100)

    # Cambios de denominación social (hasta 3)
    acreedor_denominacion1_escritura_num = models.CharField(max_length=50, blank=True)
    acreedor_denominacion1_fecha = models.DateField(null=True, blank=True)
    acreedor_denominacion1_notario = models.CharField(max_length=200, blank=True)
    acreedor_denominacion1_registro = models.CharField(max_length=100, blank=True)

    acreedor_denominacion2_escritura_num = models.CharField(max_length=50, blank=True)
    acreedor_denominacion2_fecha = models.DateField(null=True, blank=True)
    acreedor_denominacion2_notario = models.CharField(max_length=200, blank=True)
    acreedor_denominacion2_registro = models.CharField(max_length=100, blank=True)

    acreedor_denominacion3_escritura_num = models.CharField(max_length=50, blank=True)
    acreedor_denominacion3_fecha = models.DateField(null=True, blank=True)
    acreedor_denominacion3_notario = models.CharField(max_length=200, blank=True)
    acreedor_denominacion3_registro = models.CharField(max_length=100, blank=True)

    delegado_fiduciario = models.CharField(max_length=200, help_text="Nombre del delegado fiduciario")  # Ej. Manuel Arturo Mollevi Palacios
    delegado_fiduciario_escritura_num = models.CharField(max_length=50)
    delegado_fiduciario_fecha = models.DateField()
    delegado_fiduciario_notario = models.CharField(max_length=200)
    delegado_fiduciario_registro = models.CharField(max_length=100)

    # — Fideicomitente —
    fideicomitente_nombre = models.CharField(max_length=200, default="Hotelería, S.A. de C.V.")
    fideicomitente_constitucion_escritura_num = models.CharField(max_length=50)
    fideicomitente_constitucion_fecha = models.DateField()
    fideicomitente_constitucion_notario = models.CharField(max_length=200)
    fideicomitente_constitucion_registro = models.CharField(max_length=100)

    fideicomitente_representante = models.CharField(max_length=200, help_text="Nombre del apoderado legal")  # Ej. Mauricio Martín del Campo Barrón
    fideicomitente_rep_escritura_num = models.CharField(max_length=50)
    fideicomitente_rep_fecha = models.DateField()
    fideicomitente_rep_notario = models.CharField(max_length=200)
    fideicomitente_rep_registro = models.CharField(max_length=100)

    # — Domicilios para notificaciones —
    domicilio_deudor = models.TextField()
    domicilio_acreedor = models.TextField()
    domicilio_fideicomitente = models.TextField()

    # — Anexos —
    anexo_contrato_promesa = models.FileField(upload_to="anexos/", blank=True, null=True)
    anexo_poder_irrevocable = models.FileField(upload_to="anexos/", blank=True, null=True)
    
    # --- Campos de control ---
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contratos_prenda_acciones')
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('emitido', 'Emitido'),
        ('firmado', 'Firmado'),
        ('vigente', 'Vigente'),
        ('cancelado', 'Cancelado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    html_cache = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Contrato de Prenda sobre Acciones"
        verbose_name_plural = "Contratos de Prenda sobre Acciones"
        ordering = ['-fecha_contrato', '-fecha_creacion']
    
    def __str__(self):
        return f"PrendaAcciones {self.id} – {self.deudor_nombre} / {self.acreedor_nombre}"
    
    def get_absolute_url(self):
        return reverse('documentos:detalle_contrato_prenda_acciones', kwargs={'pk': self.pk})
    
    def get_estado_badge_class(self):
        """Retorna la clase CSS para el badge del estado"""
        classes = {
            'borrador': 'bg-secondary',
            'emitido': 'bg-info',
            'firmado': 'bg-primary',
            'vigente': 'bg-success',
            'cancelado': 'bg-danger',
        }
        return classes.get(self.estado, 'bg-secondary')


class ConvenioModificatorio(models.Model):
    # — Datos Generales —
    fecha_convenio = models.DateField(help_text="Fecha de firma del convenio")
    lugar_convenio = models.CharField(max_length=200, help_text="Lugar de firma del convenio")

    # — Inversionista (F101) —
    inversionista_razon_social = models.CharField(max_length=200, default="Fomento Mexicano de Posgrados 101, S.A.P.I. de C.V.")
    inversionista_representante = models.CharField(max_length=200, help_text="Nombre del apoderado de F101")
    inversionista_constitucion_escritura = models.CharField(max_length=50, help_text="Número de escritura de constitución")
    inversionista_constitucion_fecha = models.DateField(help_text="Fecha de escritura de constitución")
    inversionista_notario_constitucion = models.CharField(max_length=200, help_text="Notario de constitución")
    inversionista_registro_constitucion = models.CharField(max_length=100, help_text="Folio en Registro Público")
    inversionista_poder_escritura = models.CharField(max_length=50, help_text="Número de escritura de poder")
    inversionista_poder_fecha = models.DateField(help_text="Fecha de escritura de poder")
    inversionista_poder_notario = models.CharField(max_length=200, help_text="Notario del poder")

    # — Antecedente: Contrato de Inversión Original —
    contrato_original_fecha = models.DateField(help_text="Fecha del Contrato de Inversión original")
    contrato_original_anexo = models.FileField(upload_to="anexos/", blank=True, null=True, help_text="Copia simple (Anexo 1)")

    # — Estudiante —
    estudiante_nombre = models.CharField(max_length=200, help_text="Nombre completo del estudiante")
    estudiante_estado_civil = models.CharField(max_length=50, help_text="Estado civil")
    estudiante_nacionalidad = models.CharField(max_length=50, help_text="Nacionalidad")
    estudiante_ocupacion = models.CharField(max_length=100, help_text="Ocupación")
    estudiante_rfc = models.CharField(max_length=13, help_text="Clave del RFC")
    estudiante_curp = models.CharField(max_length=18, help_text="Clave Única de Registro de Población")
    adeudo_principal_anterior = models.DecimalField(max_digits=14, decimal_places=2, help_text="Adeudo anterior (sin intereses)")
    adeudo_principal_anterior_texto = models.CharField(max_length=200, help_text="Monto anterior en texto")
    credito_original = models.DecimalField(max_digits=14, decimal_places=2, help_text="Monto del crédito original", null=True, blank=True)

    # — Obligados Solidarios —
    luis_nombre = models.CharField(max_length=200, help_text="Nombre de Luis Alejandro Cuevas Padilla")
    luis_estado_civil = models.CharField(max_length=50, blank=True)
    luis_ocupacion = models.CharField(max_length=100, blank=True)
    luis_rfc = models.CharField(max_length=13, help_text="RFC de Luis")
    luis_curp = models.CharField(max_length=18, help_text="CURP de Luis")

    lizette_nombre = models.CharField(max_length=200, help_text="Nombre de Lizette Guadalupe López Ortega")
    lizette_estado_civil = models.CharField(max_length=50, blank=True)
    lizette_ocupacion = models.CharField(max_length=100, blank=True)
    lizette_rfc = models.CharField(max_length=13, blank=True)
    lizette_curp = models.CharField(max_length=18, blank=True)

    # — Aumento de la Inversión (Inversión II) —
    aumento_monto = models.DecimalField(max_digits=14, decimal_places=2, help_text="Monto adicional acordado")
    aumento_monto_texto = models.CharField(max_length=200, help_text="Monto adicional en texto")

    # — Reconocimiento y Pagaré II —
    inversion_total = models.DecimalField(max_digits=14, decimal_places=2, help_text="Inversión total (principal + aumento)")
    inversion_total_texto = models.CharField(max_length=200, help_text="Inversión total en texto")
    adeudo_actualizado = models.DecimalField(max_digits=14, decimal_places=2, help_text="Adeudo total actualizado")
    pagare_ii_fecha = models.DateField(help_text="Fecha de emisión del Pagaré II")
    pagare_i_devuelto = models.BooleanField(help_text="¿Se devolvió el Pagaré I cancelado?", default=True)

    # — Periodo de Disposición —
    dispo_periodo_inicio = models.DateField(help_text="Inicio del Periodo de Disposición")
    dispo_periodo_fin = models.DateField(help_text="Fin del Periodo de Disposición")

    # — Términos Financieros —
    cat_anual = models.DecimalField(max_digits=5, decimal_places=2, help_text="Costo Anual Total (%)")
    tasa_interes_mensual = models.DecimalField(max_digits=5, decimal_places=2, help_text="Tasa de interés mensual (%)")
    tasa_moratoria_mensual = models.DecimalField(max_digits=5, decimal_places=2, help_text="Tasa de interés moratorio mensual (%)")
    
    # — Pagos en Etapa de Estudios —
    pagos_estudios_num1 = models.IntegerField(help_text="Número de pagos fijos 1")
    pagos_estudios_imp1 = models.DecimalField(max_digits=14, decimal_places=2, help_text="Importe de pagos fijos 1")
    pagos_estudios_num2 = models.IntegerField(help_text="Número de pagos fijos 2")
    pagos_estudios_imp2 = models.DecimalField(max_digits=14, decimal_places=2, help_text="Importe de pagos fijos 2")
    
    # — Pagos en Etapa de Egreso —
    pagos_egreso_num = models.IntegerField(help_text="Número de pagos en etapa de egreso")
    pagos_egreso_imp = models.DecimalField(max_digits=14, decimal_places=2, help_text="Monto fijo de cada pago en egreso")
    pago_egreso_ultimo = models.DecimalField(max_digits=14, decimal_places=2, help_text="Monto del último pago")

    # — Cuenta para pagos —
    cuenta_numero = models.CharField(max_length=30, help_text="Número de cuenta bancaria")
    cuenta_banco = models.CharField(max_length=100, help_text="Nombre del banco")
    cuenta_titular = models.CharField(max_length=200, help_text="Titular de la cuenta")
    cuenta_clabe = models.CharField(max_length=18, help_text="CLABE interbancaria")

    # — Documentos a entregar (Cláusula Novena) —
    entrego_acta_nacimiento = models.BooleanField(default=False)
    entrego_identificacion_oficial = models.BooleanField(default=False)
    entrego_reporte_buro = models.BooleanField(default=False)
    entrego_rfc = models.BooleanField(default=False)
    entrego_curp = models.BooleanField(default=False)
    entrego_comprobante_domicilio = models.BooleanField(default=False)
    entrego_comprobante_ingresos = models.BooleanField(default=False)

    # — Beneficio por Cursos de Capacitación —
    cursos_requeridos = models.IntegerField(help_text="Número de cursos requeridos")
    beneficio_descripcion = models.TextField(help_text="Descripción del posible beneficio")

    # — Confidencialidad —
    confidencialidad_years = models.IntegerField(help_text="Años de vigencia de la obligación de confidencialidad")
    
    # --- Campos de control ---
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='convenios_modificatorios')
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('emitido', 'Emitido'),
        ('firmado', 'Firmado'),
        ('vigente', 'Vigente'),
        ('cancelado', 'Cancelado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    html_cache = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Convenio Modificatorio"
        verbose_name_plural = "Convenios Modificatorios"
        ordering = ['-fecha_convenio', '-fecha_creacion']
    
    def __str__(self):
        return f"Convenio {self.id} – {self.estudiante_nombre} / {self.inversionista_razon_social}"
    
    def get_absolute_url(self):
        return reverse('documentos:detalle_convenio_modificatorio', kwargs={'pk': self.pk})
    
    def get_estado_badge_class(self):
        """Retorna la clase CSS para el badge del estado"""
        classes = {
            'borrador': 'bg-secondary',
            'emitido': 'bg-info',
            'firmado': 'bg-primary',
            'vigente': 'bg-success',
            'cancelado': 'bg-danger',
        }
        return classes.get(self.estado, 'bg-secondary')
