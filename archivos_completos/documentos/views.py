from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
# Importación condicional de mammoth
try:
    import mammoth
    MAMMOTH_AVAILABLE = True
except ImportError:
    MAMMOTH_AVAILABLE = False
import os
import tempfile
import json
from io import BytesIO

# ReportLab imports
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from .models import ActaAsamblea, ActaSesionConsejo, Pagare, ContratoCredito, ContratoPrendaAcciones, ConvenioModificatorio
from .estatutos_sociedad import EstatutosSociedad
from .forms import ActaAsambleaForm, ActaSesionConsejoForm, RegistroForm, PagareForm, ContratoCreditoForm, ContratoPrendaAccionesForm, ConvenioModificatorioForm
from .forms_estatutos_fixed import EstatutosSociedadForm
from .pdf_generator import descargar_pdf_consejo, descargar_pdf_asamblea, descargar_pdf_pagare, descargar_docx_consejo, descargar_docx_pagare, descargar_docx_acta_asamblea, descargar_docx_prenda
from .docx_estatutos_generator import descargar_docx_estatutos_sociedad
from .docx_convenio_generator import descargar_docx_convenio_modificatorio
from .docx_contrato_credito_generator import descargar_docx_contrato_credito

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Contadores específicos por tipo
        total_asambleas = ActaAsamblea.objects.filter(usuario=self.request.user).count()
        total_consejos = ActaSesionConsejo.objects.filter(usuario=self.request.user).count()
        total_contratos_credito = ContratoCredito.objects.filter(usuario=self.request.user).count()
        total_pagares = Pagare.objects.filter(usuario=self.request.user).count()
        total_contratos_prenda = ContratoPrendaAcciones.objects.filter(usuario=self.request.user).count()
        total_convenios_modificatorios = ConvenioModificatorio.objects.filter(usuario=self.request.user).count()
        total_estatutos_sociedad = EstatutosSociedad.objects.filter(usuario=self.request.user).count()
        
        context['total_documentos'] = (total_asambleas + total_consejos + total_contratos_credito + 
                                     total_pagares + total_contratos_prenda + total_convenios_modificatorios + total_estatutos_sociedad)
        context['total_actas_asamblea'] = total_asambleas
        context['total_actas_consejo'] = total_consejos
        context['total_contratos_credito'] = total_contratos_credito
        context['total_pagares'] = total_pagares
        context['total_contratos_prenda'] = total_contratos_prenda
        context['total_convenios_modificatorios'] = total_convenios_modificatorios
        context['total_estatutos_sociedad'] = total_estatutos_sociedad
        
        # Documentos recientes de ambos tipos
        asambleas_recientes = ActaAsamblea.objects.filter(
            usuario=self.request.user
        ).order_by('-actualizada_en')[:3]
        consejos_recientes = ActaSesionConsejo.objects.filter(
            usuario=self.request.user
        ).order_by('-actualizada_en')[:3]
        
        # Agregar tipo de documento a cada objeto
        for asamblea in asambleas_recientes:
            asamblea.tipo_documento = 'Acta de Asamblea'
            asamblea.tipo_documento_class = 'asamblea'
        
        for consejo in consejos_recientes:
            consejo.tipo_documento = 'Acta de Sesión de Consejo'
            consejo.tipo_documento_class = 'consejo'
        
        # Combinar y ordenar por fecha de actualización
        documentos_recientes = list(asambleas_recientes) + list(consejos_recientes)
        documentos_recientes.sort(key=lambda x: x.actualizada_en, reverse=True)
        context['documentos_recientes'] = documentos_recientes[:5]
        
        return context

class RegisterView(CreateView):
    form_class = RegistroForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuario creado exitosamente. Ahora puedes iniciar sesión.')
        return super().form_valid(form)

class ActaListView(LoginRequiredMixin, ListView):
    model = ActaAsamblea
    template_name = 'documentos/lista.html'
    context_object_name = 'documentos'
    paginate_by = 10
    
    def get_queryset(self):
        return ActaAsamblea.objects.filter(usuario=self.request.user).order_by('-actualizada_en')

class ActaCreateView(LoginRequiredMixin, CreateView):
    model = ActaAsamblea
    form_class = ActaAsambleaForm
    template_name = 'documentos/crear_acta_asamblea.html'
    success_url = reverse_lazy('documentos:lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_documento'] = 'Acta de Asamblea'
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Acta de Asamblea creada exitosamente.')
        return super().form_valid(form)

class ActaUpdateView(LoginRequiredMixin, UpdateView):
    model = ActaAsamblea
    form_class = ActaAsambleaForm
    template_name = 'documentos/editar_acta_asamblea.html'
    success_url = reverse_lazy('documentos:lista')
    
    def get_queryset(self):
        return ActaAsamblea.objects.filter(usuario=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_documento'] = 'Acta de Asamblea'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Acta de Asamblea actualizada exitosamente.')
        return super().form_valid(form)

class ActaDetailView(LoginRequiredMixin, DetailView):
    model = ActaAsamblea
    template_name = 'documentos/detalle.html'
    context_object_name = 'documento'
    
    def get_queryset(self):
        return ActaAsamblea.objects.filter(usuario=self.request.user)

class ActaDeleteView(LoginRequiredMixin, DeleteView):
    model = ActaAsamblea
    template_name = 'documentos/confirmar_eliminar.html'
    success_url = reverse_lazy('documentos:lista')
    
    def get_queryset(self):
        return ActaAsamblea.objects.filter(usuario=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Documento eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

@login_required
def vista_previa_ajax(request):
    """Vista para actualizar la vista previa en tiempo real"""
    if request.method == 'POST':
        form_data = request.POST
        context = {
            'form_data': form_data,
        }
        return render(request, 'documentos/vista_previa_acta_asamblea.html', context)
    return JsonResponse({'error': 'Método no permitido'})


# ===== VISTAS PARA ACTA DE SESIÓN DE CONSEJO =====

class ConsejoListView(LoginRequiredMixin, ListView):
    model = ActaSesionConsejo
    template_name = 'documentos/lista_consejo.html'
    context_object_name = 'documentos'
    paginate_by = 10
    
    def get_queryset(self):
        return ActaSesionConsejo.objects.filter(usuario=self.request.user).order_by('-actualizada_en')

class ConsejoCreateView(LoginRequiredMixin, CreateView):
    model = ActaSesionConsejo
    form_class = ActaSesionConsejoForm
    template_name = 'documentos/crear_acta_consejo.html'
    success_url = reverse_lazy('documentos:lista_consejo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_documento'] = 'Acta de Sesión de Consejo'
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Acta de Sesión de Consejo creada exitosamente.')
        return super().form_valid(form)

class ConsejoUpdateView(LoginRequiredMixin, UpdateView):
    model = ActaSesionConsejo
    form_class = ActaSesionConsejoForm
    template_name = 'documentos/editar_acta_consejo.html'
    success_url = reverse_lazy('documentos:lista_consejo')
    context_object_name = 'documento'  # Agregar nombre específico para el objeto
    
    def get_queryset(self):
        return ActaSesionConsejo.objects.filter(usuario=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_documento'] = 'Acta de Sesión de Consejo'
        # Asegurar que el objeto esté disponible tanto como 'object' como 'documento'
        context['documento'] = self.object
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Acta de Sesión de Consejo actualizada exitosamente.')
        return super().form_valid(form)

class ConsejoDetailView(LoginRequiredMixin, DetailView):
    model = ActaSesionConsejo
    template_name = 'documentos/detalle_consejo.html'
    context_object_name = 'documento'
    
    def get_queryset(self):
        return ActaSesionConsejo.objects.filter(usuario=self.request.user)

class ConsejoDeleteView(LoginRequiredMixin, DeleteView):
    model = ActaSesionConsejo
    template_name = 'documentos/confirmar_eliminar_consejo.html'
    success_url = reverse_lazy('documentos:lista_consejo')
    context_object_name = 'documento'  # Agregar nombre específico para el objeto
    
    def get_queryset(self):
        return ActaSesionConsejo.objects.filter(usuario=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Asegurar que el objeto esté disponible tanto como 'object' como 'documento'
        context['documento'] = self.object
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Acta de Sesión de Consejo eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)

@login_required
def vista_previa_consejo_ajax(request):
    """Vista para actualizar la vista previa en tiempo real del acta de consejo"""
    if request.method == 'POST':
        form_data = request.POST
        context = {
            'form_data': form_data,
        }
        return render(request, 'documentos/vista_previa_acta_consejo.html', context)
    return JsonResponse({'error': 'Método no permitido'})


# ===== CONVERTIDOR DOCX A HTML =====

@login_required
def docx_converter(request):
    """Vista para convertir archivos DOCX a HTML usando Mammoth"""
    context = {
        'html_result': None,
        'original_filename': None,
        'error_message': None,
        'conversion_messages': None
    }
    
    # Verificar si mammoth está disponible
    if not MAMMOTH_AVAILABLE:
        context['error_message'] = 'La biblioteca Mammoth no está instalada. Por favor, instálala con "pip install mammoth" para usar esta funcionalidad.'
        messages.error(request, 'La biblioteca Mammoth no está instalada. Esta funcionalidad no está disponible.')
        return render(request, 'documentos/docx_converter.html', context)
    
    if request.method == 'POST' and request.FILES.get('docx_file'):
        docx_file = request.FILES['docx_file']
        
        # Validar que sea un archivo DOCX
        if not docx_file.name.lower().endswith('.docx'):
            context['error_message'] = 'Por favor, selecciona un archivo .docx válido.'
            return render(request, 'documentos/docx_converter.html', context)
        
        try:
            # Crear un archivo temporal para procesar el DOCX
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as temp_file:
                # Escribir el contenido del archivo subido al archivo temporal
                for chunk in docx_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            
            # Convertir DOCX a HTML usando Mammoth
            with open(temp_file_path, 'rb') as docx_file_handle:
                result = mammoth.convert_to_html(docx_file_handle)
                
                context['html_result'] = result.value
                context['original_filename'] = docx_file.name
                
                # Capturar mensajes de conversión (advertencias, etc.)
                if result.messages:
                    context['conversion_messages'] = [str(msg) for msg in result.messages]
            
            # Limpiar el archivo temporal
            os.unlink(temp_file_path)
            
            messages.success(request, f'Archivo "{docx_file.name}" convertido exitosamente.')
            
        except Exception as e:
            context['error_message'] = f'Error al convertir el archivo: {str(e)}'
            messages.error(request, 'Error durante la conversión del archivo.')
            
            # Limpiar el archivo temporal en caso de error
            if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    return render(request, 'documentos/docx_converter.html', context)


# ============ PAGARE VIEWS ============
class PagareListView(LoginRequiredMixin, ListView):
    model = Pagare
    template_name = 'documentos/lista_pagare.html'
    context_object_name = 'pagares'
    ordering = ['-fecha_emision']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Pagarés'
        return context


class PagareCreateView(LoginRequiredMixin, CreateView):
    model = Pagare
    form_class = PagareForm
    template_name = 'documentos/crear_pagare.html'
    success_url = reverse_lazy('documentos:lista_pagares')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Pagaré creado exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Pagaré'
        return context


class PagareUpdateView(LoginRequiredMixin, UpdateView):
    model = Pagare
    form_class = PagareForm
    template_name = 'documentos/editar_pagare.html'
    success_url = reverse_lazy('documentos:lista_pagares')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Pagaré'
        return context


class PagareDetailView(LoginRequiredMixin, DetailView):
    model = Pagare
    template_name = 'documentos/detalle_pagare.html'
    context_object_name = 'pagare'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle del Pagaré'
        return context


class PagareDeleteView(LoginRequiredMixin, DeleteView):
    model = Pagare
    template_name = 'documentos/eliminar_pagare.html'
    success_url = reverse_lazy('documentos:lista_pagares')
    context_object_name = 'pagare'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Pagaré'
        return context


# ============ CONTRATO CREDITO VIEWS ============
class ContratoCreditoListView(LoginRequiredMixin, ListView):
    model = ContratoCredito
    template_name = 'documentos/lista_contrato_credito.html'
    context_object_name = 'contratos'
    ordering = ['-fecha_contrato']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Contratos de Crédito'
        return context


class ContratoCreditoListView(LoginRequiredMixin, ListView):
    model = ContratoCredito
    template_name = 'documentos/lista_contrato_credito.html'
    context_object_name = 'contratos'
    ordering = ['-fecha_contrato']
    paginate_by = 10

    def get_queryset(self):
        return ContratoCredito.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Contratos de Crédito'
        return context


class ContratoCreditoCreateView(LoginRequiredMixin, CreateView):
    model = ContratoCredito
    form_class = ContratoCreditoForm
    template_name = 'documentos/crear_contrato_credito.html'
    success_url = reverse_lazy('documentos:lista_contrato_credito')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Contrato de Crédito'
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Contrato de Crédito creado exitosamente.')
        return super().form_valid(form)


class ContratoCreditoUpdateView(LoginRequiredMixin, UpdateView):
    model = ContratoCredito
    form_class = ContratoCreditoForm
    template_name = 'documentos/editar_contrato_credito.html'
    success_url = reverse_lazy('documentos:lista_contrato_credito')
    context_object_name = 'contrato'

    def get_queryset(self):
        return ContratoCredito.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Contrato de Crédito'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Contrato de Crédito actualizado exitosamente.')
        return super().form_valid(form)


class ContratoCreditoDetailView(LoginRequiredMixin, DetailView):
    model = ContratoCredito
    template_name = 'documentos/detalle_contrato_credito.html'
    context_object_name = 'contrato'

    def get_queryset(self):
        return ContratoCredito.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle del Contrato de Crédito'
        return context


class ContratoCreditoDeleteView(LoginRequiredMixin, DeleteView):
    model = ContratoCredito
    template_name = 'documentos/eliminar_contrato_credito.html'
    success_url = reverse_lazy('documentos:lista_contrato_credito')
    context_object_name = 'contrato'

    def get_queryset(self):
        return ContratoCredito.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Contrato de Crédito'
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Contrato de Crédito eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============ CONTRATO PRENDA ACCIONES VIEWS ============
class ContratoPrendaAccionesListView(LoginRequiredMixin, ListView):
    model = ContratoPrendaAcciones
    template_name = 'documentos/lista_contrato_prenda.html'
    context_object_name = 'contratos'
    ordering = ['-fecha_contrato']
    paginate_by = 10

    def get_queryset(self):
        return ContratoPrendaAcciones.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Contratos de Prenda de Acciones'
        return context


class ContratoPrendaAccionesCreateView(LoginRequiredMixin, CreateView):
    model = ContratoPrendaAcciones
    form_class = ContratoPrendaAccionesForm
    template_name = 'documentos/crear_contrato_prenda.html'
    success_url = reverse_lazy('documentos:lista_contrato_prenda')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Contrato de Prenda de Acciones'
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Contrato de Prenda sobre Acciones creado exitosamente.')
        return super().form_valid(form)


class ContratoPrendaAccionesUpdateView(LoginRequiredMixin, UpdateView):
    model = ContratoPrendaAcciones
    form_class = ContratoPrendaAccionesForm
    template_name = 'documentos/editar_contrato_prenda.html'
    success_url = reverse_lazy('documentos:lista_contrato_prenda')

    def get_queryset(self):
        return ContratoPrendaAcciones.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Contrato de Prenda de Acciones'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Contrato de Prenda sobre Acciones actualizado exitosamente.')
        return super().form_valid(form)


class ContratoPrendaAccionesDetailView(LoginRequiredMixin, DetailView):
    model = ContratoPrendaAcciones
    template_name = 'documentos/detalle_contrato_prenda.html'
    context_object_name = 'contrato'

    def get_queryset(self):
        return ContratoPrendaAcciones.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle del Contrato de Prenda de Acciones'
        return context


class ContratoPrendaAccionesDeleteView(LoginRequiredMixin, DeleteView):
    model = ContratoPrendaAcciones
    template_name = 'documentos/eliminar_contrato_prenda.html'
    success_url = reverse_lazy('documentos:lista_contrato_prenda')
    context_object_name = 'contrato'

    def get_queryset(self):
        return ContratoPrendaAcciones.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Contrato de Prenda de Acciones'
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Contrato de Prenda sobre Acciones eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============ CONVENIO MODIFICATORIO VIEWS ============
class ConvenioModificatorioListView(LoginRequiredMixin, ListView):
    model = ConvenioModificatorio
    template_name = 'documentos/lista_convenio_modificatorio.html'
    context_object_name = 'convenios'
    ordering = ['-fecha_convenio']
    paginate_by = 10

    def get_queryset(self):
        return ConvenioModificatorio.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Convenios Modificatorios'
        return context


class ConvenioModificatorioCreateView(LoginRequiredMixin, CreateView):
    model = ConvenioModificatorio
    form_class = ConvenioModificatorioForm
    template_name = 'documentos/crear_convenio_modificatorio.html'
    success_url = reverse_lazy('documentos:lista_convenio_modificatorio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Convenio Modificatorio'
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Convenio Modificatorio creado exitosamente.')
        return super().form_valid(form)


class ConvenioModificatorioUpdateView(LoginRequiredMixin, UpdateView):
    model = ConvenioModificatorio
    form_class = ConvenioModificatorioForm
    template_name = 'documentos/editar_convenio_modificatorio.html'
    success_url = reverse_lazy('documentos:lista_convenio_modificatorio')

    def get_queryset(self):
        return ConvenioModificatorio.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Convenio Modificatorio'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Convenio Modificatorio actualizado exitosamente.')
        return super().form_valid(form)


class ConvenioModificatorioDetailView(LoginRequiredMixin, DetailView):
    model = ConvenioModificatorio
    template_name = 'documentos/detalle_convenio_modificatorio.html'
    context_object_name = 'convenio'

    def get_queryset(self):
        return ConvenioModificatorio.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle del Convenio Modificatorio'
        return context


class ConvenioModificatorioDeleteView(LoginRequiredMixin, DeleteView):
    model = ConvenioModificatorio
    template_name = 'documentos/eliminar_convenio_modificatorio.html'
    success_url = reverse_lazy('documentos:lista_convenio_modificatorio')
    context_object_name = 'convenio'

    def get_queryset(self):
        return ConvenioModificatorio.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Convenio Modificatorio'
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Convenio Modificatorio eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============ VISTAS CRUD PARA PAGARÉS ============

class PagareListView(LoginRequiredMixin, ListView):
    model = Pagare
    template_name = 'documentos/lista_pagares.html'
    context_object_name = 'pagares'
    paginate_by = 10

    def get_queryset(self):
        return Pagare.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Pagarés'
        return context


class PagareCreateView(LoginRequiredMixin, CreateView):
    model = Pagare
    form_class = PagareForm
    template_name = 'documentos/crear_pagare.html'
    success_url = reverse_lazy('documentos:lista_pagares')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Pagaré creado exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Pagaré'
        return context


class PagareUpdateView(LoginRequiredMixin, UpdateView):
    model = Pagare
    form_class = PagareForm
    template_name = 'documentos/editar_pagare.html'
    success_url = reverse_lazy('documentos:lista_pagares')

    def get_queryset(self):
        return Pagare.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        # Get the existing instance from database to preserve values not in the form
        existing_instance = self.get_object()
        
        # Fields that might not be in the edit form but should preserve their existing values
        fields_to_preserve = [
            'monto_numeric', 'monto_literal', 'moneda', 'concepto', 'tipo_pago',
            'tasa_interes_ordinario', 'base_intereses', 'tasa_interes_moratorio',
            'gastos_admon', 'num_paginas', 'dias_aviso_prepago', 'num_pagos',
            'periodicidad', 'forma_pago', 'impuestos', 'condicion_prepago',
            'descripcion_garantia', 'eventos_incumplimiento', 'jurisdiccion',
            'ley_aplicable', 'anexos', 'deudor_rfc', 'deudor_representante',
            'acreedor_rfc', 'prepago_permitido', 'tiene_garantia'
        ]
        
        # Before saving, preserve existing values for fields not present in the form
        for field_name in fields_to_preserve:
            if hasattr(form.instance, field_name) and hasattr(existing_instance, field_name):
                # If the field is not in the form data or is empty/None, preserve the existing value
                form_value = getattr(form.instance, field_name)
                existing_value = getattr(existing_instance, field_name)
                
                # Preserve existing value if form value is None or empty string (but not False for booleans)
                if form_value is None or (isinstance(form_value, str) and form_value == '' and existing_value):
                    setattr(form.instance, field_name, existing_value)
        
        messages.success(self.request, 'Pagaré actualizado exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Pagaré'
        return context


class PagareDetailView(LoginRequiredMixin, DetailView):
    model = Pagare
    template_name = 'documentos/detalle_pagare.html'
    context_object_name = 'pagare'

    def get_queryset(self):
        return Pagare.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle del Pagaré'
        return context


class PagareDeleteView(LoginRequiredMixin, DeleteView):
    model = Pagare
    template_name = 'documentos/eliminar_pagare.html'
    success_url = reverse_lazy('documentos:lista_pagares')
    context_object_name = 'pagare'

    def get_queryset(self):
        return Pagare.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Pagaré'
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Pagaré eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# ===== VISTAS CRUD PARA ESTATUTOS SOCIALES =====

class EstatutosSociedadListView(LoginRequiredMixin, ListView):
    model = EstatutosSociedad
    template_name = 'documentos/lista_estatutos_sociedad.html'
    context_object_name = 'estatutos_list'
    paginate_by = 10

    def get_queryset(self):
        return EstatutosSociedad.objects.filter(usuario=self.request.user).order_by('-fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Estatutos Sociales'
        return context


class EstatutosSociedadCreateView(LoginRequiredMixin, CreateView):
    model = EstatutosSociedad
    form_class = EstatutosSociedadForm
    template_name = 'documentos/crear_estatutos_sociedad.html'
    success_url = reverse_lazy('documentos:lista_estatutos_sociedad')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Estatutos Sociales creados exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Estatutos Sociales'
        return context


class EstatutosSociedadUpdateView(LoginRequiredMixin, UpdateView):
    model = EstatutosSociedad
    form_class = EstatutosSociedadForm
    template_name = 'documentos/editar_estatutos_sociedad.html'
    success_url = reverse_lazy('documentos:lista_estatutos_sociedad')

    def get_queryset(self):
        return EstatutosSociedad.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        # Debug: verificar si el formulario es realmente válido
        if not form.is_valid():
            messages.error(self.request, 'El formulario contiene errores de validación.')
            return self.form_invalid(form)
        
        try:
            form.instance.usuario = self.request.user
            messages.success(self.request, 'Estatutos Sociales actualizados exitosamente.')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Error al guardar: {str(e)}')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        # Debug: mostrar errores específicos del formulario
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(f"{field}: {error}")
        
        if error_messages:
            messages.error(self.request, f'Errores en el formulario: {"; ".join(error_messages)}')
        else:
            messages.error(self.request, 'Error desconocido en el formulario.')
        
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Estatutos Sociales'
        return context


class EstatutosSociedadDetailView(LoginRequiredMixin, DetailView):
    model = EstatutosSociedad
    template_name = 'documentos/detalle_estatutos_sociedad.html'
    context_object_name = 'estatutos'

    def get_queryset(self):
        return EstatutosSociedad.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle de Estatutos Sociales'
        return context


class EstatutosSociedadDeleteView(LoginRequiredMixin, DeleteView):
    model = EstatutosSociedad
    template_name = 'documentos/eliminar_estatutos_sociedad.html'
    success_url = reverse_lazy('documentos:lista_estatutos_sociedad')
    context_object_name = 'estatutos'

    def get_queryset(self):
        return EstatutosSociedad.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Estatutos Sociales'
        return context
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Estatutos Sociales eliminados exitosamente.')
        return super().delete(request, *args, **kwargs)
