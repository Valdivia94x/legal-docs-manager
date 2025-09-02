from django.contrib import admin
from .models import ActaAsamblea, ActaSesionConsejo, TipoDocumento

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']

@admin.register(ActaAsamblea)
class ActaAsambleaAdmin(admin.ModelAdmin):
    list_display = [
        'razon_social', 'tipo_asamblea', 'fecha', 'presidente', 
        'secretario', 'estado', 'creada_en'
    ]
    list_filter = [
        'tipo_asamblea', 'estado', 'fecha', 'creada_en', 
        'convocatoria_omitida', 'metodo_votacion_general'
    ]
    search_fields = [
        'razon_social', 'presidente', 'secretario', 'escrutador', 
        'comisario', 'caracter'
    ]
    date_hierarchy = 'fecha'
    ordering = ['-fecha', '-creada_en']
    
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'usuario', 'razon_social', 'tipo_asamblea', 'caracter', 
                'fecha', 'hora_inicio', 'hora_cierre', 'lugar'
            )
        }),
        ('Participación y Convocatoria', {
            'fields': (
                'porcentaje_capital_presente', 'convocatoria_omitida', 
                'fundamento_convocatoria', 'metodo_votacion_general'
            )
        }),
        ('Participantes', {
            'fields': (
                'presidente', 'secretario', 'escrutador', 'comisario'
            )
        }),
        ('Datos Estructurados (JSON)', {
            'fields': (
                'asistentes_json', 'orden_dia_json', 'resoluciones_json',
                'nombramientos_json', 'dividendos_json', 'delegados_json',
                'anexos_json'
            ),
            'classes': ('collapse',),
            'description': 'Campos JSON para almacenar datos estructurados complejos'
        }),
        ('Estado y Cache', {
            'fields': (
                'estado', 'acta_html_cache'
            ),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['creada_en', 'actualizada_en']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.usuario = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)


@admin.register(ActaSesionConsejo)
class ActaSesionConsejoAdmin(admin.ModelAdmin):
    list_display = [
        'razon_social', 'fecha', 'presidente', 'secretario', 
        'porcentaje_miembros_presentes', 'estado', 'creada_en'
    ]
    list_filter = [
        'estado', 'fecha', 'creada_en', 'convocatoria_realizada', 
        'metodo_instalacion'
    ]
    search_fields = [
        'razon_social', 'presidente', 'secretario', 'lugar'
    ]
    date_hierarchy = 'fecha'
    ordering = ['-fecha', '-creada_en']
    
    fieldsets = (
        ('Información Básica', {
            'fields': (
                'usuario', 'razon_social', 'fecha', 'hora_inicio', 
                'hora_cierre', 'lugar'
            )
        }),
        ('Convocatoria y Quórum', {
            'fields': (
                'convocatoria_realizada', 'porcentaje_miembros_presentes', 
                'metodo_instalacion'
            )
        }),
        ('Mesa Directiva', {
            'fields': (
                'presidente', 'secretario'
            )
        }),
        ('Datos Estructurados (JSON)', {
            'fields': (
                'asistentes_json', 'invitados_json', 'orden_dia_json', 
                'resoluciones_json', 'delegados_json', 'anexos_json'
            ),
            'classes': ('collapse',),
            'description': 'Campos JSON para almacenar datos estructurados complejos'
        }),
        ('Estado y Cache', {
            'fields': (
                'estado', 'acta_html_cache'
            ),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['creada_en', 'actualizada_en']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.usuario = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)
