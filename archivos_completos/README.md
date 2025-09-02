# Asistente Legal - Aplicación Django

## Descripción
Aplicación web para la generación de documentos legales con vista previa en tiempo real. Especializada en Actas de Asambleas Generales con formato legal mexicano profesional.

## Características
- 🔐 Sistema de autenticación completo
- 📄 Generación de Actas de Asambleas
- ⚡ Vista previa en tiempo real
- 💾 Gestión CRUD completa
- 🏛️ Panel de administración Django
- 📱 Interfaz responsive

## Instalación

### Prerrequisitos
- Python 3.8+
- pip

### Pasos de instalación

1. **Clonar/Extraer el proyecto**
```bash
cd asistente_legal
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar la base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crear superusuario**
```bash
python manage.py createsuperuser
```

6. **Ejecutar el servidor**
```bash
python manage.py runserver
```

## Uso

### Acceso a la aplicación
- **Aplicación principal**: http://127.0.0.1:8005/
- **Panel de administración**: http://127.0.0.1:8005/admin/

### Funcionalidades principales
1. **Registro e inicio de sesión** de usuarios
2. **Dashboard** personalizado con estadísticas
3. **Crear documentos** con vista previa en tiempo real
4. **Editar y eliminar** documentos existentes
5. **Gestión de anexos** condicional

## Estructura del Proyecto

```
asistente_legal/
├── manage.py
├── requirements.txt
├── asistente_legal/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── documentos/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── urls.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── registration/
│   └── documentos/
├── static/
│   ├── css/
│   └── js/
└── media/
```

## Tecnologías Utilizadas
- **Backend**: Django 4.2+
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Base de datos**: SQLite (desarrollo)
- **Autenticación**: Django Auth

## Personalización

### Añadir nuevos tipos de documentos
1. Crear nuevo modelo en `documentos/models.py`
2. Crear formulario en `documentos/forms.py`
3. Añadir vistas en `documentos/views.py`
4. Crear templates correspondientes
5. Actualizar URLs

### Modificar plantillas de documentos
Editar los templates en `templates/documentos/` para cambiar el formato de salida.

## Seguridad
- Protección CSRF habilitada
- Autenticación requerida para todas las funciones
- Separación de datos por usuario
- Validación de formularios

## Soporte
Para soporte técnico o consultas, contactar al desarrollador del proyecto.

## Licencia
Proyecto desarrollado para uso interno/educativo.
