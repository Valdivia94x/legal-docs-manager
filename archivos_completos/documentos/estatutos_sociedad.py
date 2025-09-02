from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class EstatutosSociedad(models.Model):
    # — Datos de Identificación —
    denominacion = models.CharField(
        max_length=200,
        help_text="Nombre completo de la sociedad (sin la abreviatura)",
    )
    forma_legal = models.CharField(
        max_length=100,
        help_text="Forma legal o abreviatura (p.ej. S.A.P.I. de C.V.), valor dinámico",
    )

    # — Domicilio y Nacionalidad —
    domicilio = models.CharField(
        max_length=200,
        help_text="Domicilio social registrado",
    )
    nacionalidad = models.CharField(
        max_length=100,
        default="mexicana",
        help_text="Nacionalidad de la sociedad",
    )

    # — Objeto Social —
    objeto_social = models.JSONField(
        help_text="Lista de cláusulas del objeto social",
    )

    # — Duración —
    duracion_indefinida = models.BooleanField(
        default=True,
        help_text="Si la sociedad tiene duración indefinida",
    )

    # — Cláusula de inversores extranjeros —
    convenio_admision_extranjeros = models.BooleanField(
        default=True,
        help_text="Si los accionistas adoptan el convenio de admisión de extranjeros",
    )

    # — Capital Social —
    capital_fijo_monto = models.DecimalField(
        max_digits=16,
        decimal_places=2,
        help_text="Monto del capital fijo en M.N.",
    )
    capital_fijo_texto = models.CharField(
        max_length=200,
        help_text="Monto del capital fijo en texto",
    )
    acciones_serie_a = models.BigIntegerField(
        help_text="Número de acciones de la Serie A (capital fijo)",
    )
    capital_variable_ilimitado = models.BooleanField(
        default=True,
        help_text="True si la parte variable del capital es ilimitada",
    )

    # — Clases de Acciones —
    clase_acciones = models.JSONField(
        help_text="Definición de series de acciones: claves 'A','B','P' con sus derechos y limitaciones",
    )

    # — Libros y Registros —
    libro_registro_acciones = models.CharField(
        max_length=200,
        default="Libro de Registro de Acciones",
        help_text="Nombre del libro de registro de acciones",
    )

    # — Aumentos y Disminuciones de Capital —
    derecho_preferencia = models.BooleanField(
        default=True,
        help_text="Si los accionistas tienen derecho de preferencia en aumentos de capital",
    )

    # — Transmisión de Acciones —
    procedimiento_transmision = models.TextField(
        help_text="Descripción del procedimiento de transmisión de acciones",
    )

    # — Asambleas de Accionistas —
    periodicidad_asamblea = models.CharField(
        max_length=100,
        default="Anual",
        help_text="Frecuencia de las Asambleas Ordinarias",
    )
    quorum_ordinaria = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=50.00,
        help_text="Porcentaje de quórum para Asamblea Ordinaria (%)",
    )
    quorum_extraordinaria = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=75.00,
        help_text="Porcentaje de quórum para Asamblea Extraordinaria (%)",
    )

    # — Administración y Consejo de Administración —
    num_consejeros = models.PositiveIntegerField(
        help_text="Número de consejeros propietarios",
    )
    suplentes_permitidos = models.BooleanField(
        default=True,
        help_text="Si hay consejeros suplentes",
    )

    # — Comisarios —
    num_comisarios = models.PositiveIntegerField(
        help_text="Número de comisarios titulares",
    )
    comisarios_suplentes = models.BooleanField(
        default=True,
        help_text="Si hay comisarios suplentes",
    )

    # — Ejercicio Social —
    ejercicio_inicio = models.CharField(
        max_length=20,
        default="01/01",
        help_text="Fecha de inicio del ejercicio social",
    )
    ejercicio_fin = models.CharField(
        max_length=20,
        default="31/12",
        help_text="Fecha de fin del ejercicio social",
    )

    # — Utilidades y Dividendos —
    reserva_legal_pct = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5.00,
        help_text="Porcentaje mínimo para el Fondo de Reserva Legal (%)",
    )
    
    # --- Campos de control ---
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estatutos_sociedad')
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('emitido', 'Emitido'),
        ('firmado', 'Firmado'),
        ('vigente', 'Vigente'),
        ('modificado', 'Modificado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    html_cache = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Estatutos Sociales"
        verbose_name_plural = "Estatutos Sociales"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.denominacion} {self.forma_legal}"
    
    def get_absolute_url(self):
        return reverse('documentos:detalle_estatutos_sociedad', kwargs={'pk': self.pk})
    
    def get_estado_badge_class(self):
        """Retorna la clase CSS para el badge del estado"""
        classes = {
            'borrador': 'bg-secondary',
            'emitido': 'bg-info',
            'firmado': 'bg-primary',
            'vigente': 'bg-success',
            'modificado': 'bg-warning',
        }
        return classes.get(self.estado, 'bg-secondary')
