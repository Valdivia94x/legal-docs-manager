from django.urls import path
from . import views

app_name = 'documentos'

urlpatterns = [
    # Actas de Asamblea
    path('', views.ActaListView.as_view(), name='lista'),
    path('crear/', views.ActaCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.ActaDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.ActaUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.ActaDeleteView.as_view(), name='eliminar'),
    path('<int:pk>/pdf/', views.descargar_pdf_asamblea, name='descargar_pdf_asamblea'),
    path('<int:pk>/docx/', views.descargar_docx_acta_asamblea, name='descargar_docx_asamblea'),
    path('vista-previa/', views.vista_previa_ajax, name='vista_previa'),
    
    # Actas de Sesión de Consejo
    path('consejo/', views.ConsejoListView.as_view(), name='lista_consejo'),
    path('consejo/crear/', views.ConsejoCreateView.as_view(), name='crear_consejo'),
    path('consejo/<int:pk>/', views.ConsejoDetailView.as_view(), name='detalle_consejo'),
    path('consejo/<int:pk>/editar/', views.ConsejoUpdateView.as_view(), name='editar_consejo'),
    path('consejo/<int:pk>/eliminar/', views.ConsejoDeleteView.as_view(), name='eliminar_consejo'),
    path('consejo/<int:pk>/pdf/', views.descargar_pdf_consejo, name='descargar_pdf_consejo'),
    path('consejo/<int:pk>/docx/', views.descargar_docx_consejo, name='descargar_docx_consejo'),
    path('consejo/vista-previa/', views.vista_previa_consejo_ajax, name='vista_previa_consejo'),
    
    # Convertidor DOCX
    path('docx-converter/', views.docx_converter, name='docx_converter'),
    
    # Pagaré URLs
    path('pagares/', views.PagareListView.as_view(), name='lista_pagare'),
    path('pagares/crear/', views.PagareCreateView.as_view(), name='crear_pagare'),
    path('pagares/<int:pk>/', views.PagareDetailView.as_view(), name='detalle_pagare'),
    path('pagares/<int:pk>/editar/', views.PagareUpdateView.as_view(), name='editar_pagare'),
    path('pagares/<int:pk>/eliminar/', views.PagareDeleteView.as_view(), name='eliminar_pagare'),
    path('pagares/<int:pk>/pdf/', views.descargar_pdf_pagare, name='descargar_pdf_pagare'),
    path('pagares/<int:pk>/docx/', views.descargar_docx_pagare, name='descargar_docx_pagare'),
    
    # Contrato de Crédito URLs
    path('contratos-credito/', views.ContratoCreditoListView.as_view(), name='lista_contrato_credito'),
    path('contratos-credito/crear/', views.ContratoCreditoCreateView.as_view(), name='crear_contrato_credito'),
    path('contratos-credito/<int:pk>/', views.ContratoCreditoDetailView.as_view(), name='detalle_contrato_credito'),
    path('contratos-credito/<int:pk>/editar/', views.ContratoCreditoUpdateView.as_view(), name='editar_contrato_credito'),
    path('contratos-credito/<int:pk>/eliminar/', views.ContratoCreditoDeleteView.as_view(), name='eliminar_contrato_credito'),
    path('contratos-credito/<int:pk>/docx/', views.descargar_docx_contrato_credito, name='descargar_docx_contrato_credito'),
    
    # Contrato de Prenda de Acciones URLs
    path('contratos-prenda/', views.ContratoPrendaAccionesListView.as_view(), name='lista_contrato_prenda'),
    path('contratos-prenda/crear/', views.ContratoPrendaAccionesCreateView.as_view(), name='crear_contrato_prenda'),
    path('contratos-prenda/<int:pk>/', views.ContratoPrendaAccionesDetailView.as_view(), name='detalle_contrato_prenda'),
    path('contratos-prenda/<int:pk>/editar/', views.ContratoPrendaAccionesUpdateView.as_view(), name='editar_contrato_prenda'),
    path('contratos-prenda/<int:pk>/eliminar/', views.ContratoPrendaAccionesDeleteView.as_view(), name='eliminar_contrato_prenda'),
    path('contratos-prenda/<int:pk>/docx/', views.descargar_docx_prenda, name='descargar_docx_prenda'),
    
    # Convenio Modificatorio URLs
    path('convenios-modificatorios/', views.ConvenioModificatorioListView.as_view(), name='lista_convenio_modificatorio'),
    path('convenios-modificatorios/crear/', views.ConvenioModificatorioCreateView.as_view(), name='crear_convenio_modificatorio'),
    path('convenios-modificatorios/<int:pk>/', views.ConvenioModificatorioDetailView.as_view(), name='detalle_convenio_modificatorio'),
    path('convenios-modificatorios/<int:pk>/editar/', views.ConvenioModificatorioUpdateView.as_view(), name='editar_convenio_modificatorio'),
    path('convenios-modificatorios/<int:pk>/eliminar/', views.ConvenioModificatorioDeleteView.as_view(), name='eliminar_convenio_modificatorio'),
    path('convenios-modificatorios/<int:pk>/docx/', views.descargar_docx_convenio_modificatorio, name='descargar_docx_convenio_modificatorio'),
    
    # Pagarés URLs
    path('pagares/', views.PagareListView.as_view(), name='lista_pagares'),
    path('pagares/crear/', views.PagareCreateView.as_view(), name='crear_pagare'),
    path('pagares/<int:pk>/', views.PagareDetailView.as_view(), name='detalle_pagare'),
    path('pagares/<int:pk>/editar/', views.PagareUpdateView.as_view(), name='editar_pagare'),
    path('pagares/<int:pk>/eliminar/', views.PagareDeleteView.as_view(), name='eliminar_pagare'),
    
    # Estatutos Sociales URLs
    path('estatutos-sociales/', views.EstatutosSociedadListView.as_view(), name='lista_estatutos_sociedad'),
    path('estatutos-sociales/crear/', views.EstatutosSociedadCreateView.as_view(), name='crear_estatutos_sociedad'),
    path('estatutos-sociales/<int:pk>/', views.EstatutosSociedadDetailView.as_view(), name='detalle_estatutos_sociedad'),
    path('estatutos-sociales/<int:pk>/editar/', views.EstatutosSociedadUpdateView.as_view(), name='editar_estatutos_sociedad'),
    path('estatutos-sociales/<int:pk>/eliminar/', views.EstatutosSociedadDeleteView.as_view(), name='eliminar_estatutos_sociedad'),
    path('estatutos-sociales/<int:pk>/docx/', views.descargar_docx_estatutos_sociedad, name='descargar_docx_estatutos_sociedad'),
]
