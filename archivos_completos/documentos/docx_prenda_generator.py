import os
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from docxtpl import DocxTemplate
from num2words import num2words
import tempfile


def formatear_fecha(fecha):
    """Convierte una fecha a formato español legible"""
    if not fecha:
        return ''
    
    meses = [
        '', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]
    
    return f"{fecha.day} de {meses[fecha.month]} de {fecha.year}"


def generar_docx_prenda(contrato):
    """
    Genera un documento DOCX para ContratoPrendaAcciones reemplazando placeholders
    """
    # Ruta de la plantilla
    template_path = os.path.join(
        os.path.dirname(settings.BASE_DIR), 
        'DOCUMENTOS OLEA ABOGADOS', 
        'Contratos de Prenda Sobre Acciones',
        'Contrato de Prenda PLACE.docx'
    )
    
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"No se encontró la plantilla en: {template_path}")
    
    # Cargar la plantilla con docxtpl
    doc = DocxTemplate(template_path)
    
    # Diccionario de contexto para docxtpl (sin llaves dobles)
    context = {
        # Datos Generales
        'fecha_contrato': formatear_fecha(contrato.fecha_contrato),
        'lugar_contrato': contrato.lugar_contrato or '',
        
        # Fideicomiso
        'numero_fideicomiso': contrato.numero_fideicomiso or '',
        'fecha_fideicomiso': formatear_fecha(contrato.fecha_fideicomiso),
        
        # Proyecto
        'fecha_aprobacion_proyecto': formatear_fecha(contrato.fecha_aprobacion_proyecto),
        'descripcion_proyecto': contrato.descripcion_proyecto or '',
        
        # Deudor Prendario
        'deudor_nombre': contrato.deudor_nombre or '',
        'DEUDOR_NOMBRE': contrato.deudor_nombre.upper() if contrato.deudor_nombre else '',
        'deudor_constitucion_escritura_num': contrato.deudor_constitucion_escritura_num or '',
        'deudor_constitucion_fecha': formatear_fecha(contrato.deudor_constitucion_fecha),
        'deudor_constitucion_notario': contrato.deudor_constitucion_notario or '',
        'deudor_constitucion_registro': contrato.deudor_constitucion_registro or '',
        
        'deudor_adopcion_sapi_escritura_num': contrato.deudor_adopcion_sapi_escritura_num or '',
        'deudor_adopcion_sapi_fecha': formatear_fecha(contrato.deudor_adopcion_sapi_fecha),
        'deudor_adopcion_sapi_notario': contrato.deudor_adopcion_sapi_notario or '',
        'deudor_adopcion_sapi_registro': contrato.deudor_adopcion_sapi_registro or '',
        
        'deudor_representante': contrato.deudor_representante or '',
        'DEUDOR_REPRESENTANTE': contrato.deudor_representante.upper() if contrato.deudor_representante else '',
        
        # Acciones
        'acciones_pledged_cantidad': f"{contrato.acciones_pledged_cantidad:,}" if contrato.acciones_pledged_cantidad else '',
        'acciones_pledged_texto': contrato.acciones_pledged_texto or '',
        'ACCIONES_PLEDGED_TEXTO': contrato.acciones_pledged_texto.upper() if contrato.acciones_pledged_texto else '',
        
        # Acreedor Prendario
        'acreedor_nombre': contrato.acreedor_nombre or '',
        'ACREEDOR_NOMBRE': contrato.acreedor_nombre.upper() if contrato.acreedor_nombre else '',
        'acreedor_constitucion_escritura_num': contrato.acreedor_constitucion_escritura_num or '',
        'acreedor_constitucion_fecha': formatear_fecha(contrato.acreedor_constitucion_fecha),
        'acreedor_constitucion_notario': contrato.acreedor_constitucion_notario or '',
        'acreedor_constitucion_registro': contrato.acreedor_constitucion_registro or '',
        
        # Cambios de denominación social del acreedor
        'acreedor_denominacion1_escritura_num': contrato.acreedor_denominacion1_escritura_num or '',
        'acreedor_denominacion1_fecha': formatear_fecha(contrato.acreedor_denominacion1_fecha),
        'acreedor_denominacion1_notario': contrato.acreedor_denominacion1_notario or '',
        'acreedor_denominacion1_registro': contrato.acreedor_denominacion1_registro or '',
        
        'acreedor_denominacion2_escritura_num': contrato.acreedor_denominacion2_escritura_num or '',
        'acreedor_denominacion2_fecha': formatear_fecha(contrato.acreedor_denominacion2_fecha),
        'acreedor_denominacion2_notario': contrato.acreedor_denominacion2_notario or '',
        'acreedor_denominacion2_registro': contrato.acreedor_denominacion2_registro or '',
        
        'acreedor_denominacion3_escritura_num': contrato.acreedor_denominacion3_escritura_num or '',
        'acreedor_denominacion3_fecha': formatear_fecha(contrato.acreedor_denominacion3_fecha),
        'acreedor_denominacion3_notario': contrato.acreedor_denominacion3_notario or '',
        'acreedor_denominacion3_registro': contrato.acreedor_denominacion3_registro or '',
        
        # Delegado Fiduciario
        'delegado_fiduciario': contrato.delegado_fiduciario or '',
        'DELEGADO_FIDUCIARIO': contrato.delegado_fiduciario.upper() if contrato.delegado_fiduciario else '',
        'delegado_fiduciario_escritura_num': contrato.delegado_fiduciario_escritura_num or '',
        'delegado_fiduciario_fecha': formatear_fecha(contrato.delegado_fiduciario_fecha),
        'delegado_fiduciario_notario': contrato.delegado_fiduciario_notario or '',
        'delegado_fiduciario_registro': contrato.delegado_fiduciario_registro or '',
        
        # Fideicomitente
        'fideicomitente_nombre': contrato.fideicomitente_nombre or '',
        'FIDEICOMITENTE_NOMBRE': contrato.fideicomitente_nombre.upper() if contrato.fideicomitente_nombre else '',
        'fideicomitente_constitucion_escritura_num': contrato.fideicomitente_constitucion_escritura_num or '',
        'fideicomitente_constitucion_fecha': formatear_fecha(contrato.fideicomitente_constitucion_fecha),
        'fideicomitente_constitucion_notario': contrato.fideicomitente_constitucion_notario or '',
        'fideicomitente_constitucion_registro': contrato.fideicomitente_constitucion_registro or '',
        
        'fideicomitente_representante': contrato.fideicomitente_representante or '',
        'FIDEICOMITENTE_REPRESENTANTE': contrato.fideicomitente_representante.upper() if contrato.fideicomitente_representante else '',
        'fideicomitente_rep_escritura_num': contrato.fideicomitente_rep_escritura_num or '',
        'fideicomitente_rep_fecha': formatear_fecha(contrato.fideicomitente_rep_fecha),
        'fideicomitente_rep_notario': contrato.fideicomitente_rep_notario or '',
        'fideicomitente_rep_registro': contrato.fideicomitente_rep_registro or '',
        
        # Domicilios
        'domicilio_deudor': contrato.domicilio_deudor or '',
        'domicilio_acreedor': contrato.domicilio_acreedor or '',
        'domicilio_fideicomitente': contrato.domicilio_fideicomitente or '',
        'estado_civil': "soltero",
    }
    
    # Renderizar la plantilla con el contexto
    doc.render(context)
    
    # Crear archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
        tmp_filename = tmp_file.name
    
    # Guardar el documento fuera del context manager
    doc.save(tmp_filename)
    
    try:
        # Leer el archivo y crear la respuesta HTTP
        with open(tmp_filename, 'rb') as f:
            response = HttpResponse(
                f.read(),
                content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )
    finally:
        # Eliminar archivo temporal
        try:
            os.unlink(tmp_filename)
        except OSError:
            pass  # Ignorar si no se puede eliminar
    
    # Configurar headers de descarga
    filename = f"Contrato_de_Prenda_generado_{contrato.id}.docx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response
