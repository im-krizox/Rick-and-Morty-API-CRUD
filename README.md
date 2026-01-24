# Rick and Morty API CRUD

Aplicación web desarrollada con Django que permite gestionar personajes del universo de Rick and Morty. El proyecto integra la [API pública de Rick and Morty](https://rickandmortyapi.com/) para poblar la base de datos inicial y proporciona una interfaz moderna para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre los personajes.

## Tabla de Contenidos

- [Rick and Morty API CRUD](#rick-and-morty-api-crud)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Descripción General](#descripción-general)
  - [Características](#características)
  - [Tecnologías Utilizadas](#tecnologías-utilizadas)
  - [Requisitos Previos](#requisitos-previos)
  - [Instalación](#instalación)
    - [1. Clonar el Repositorio](#1-clonar-el-repositorio)
    - [2. Crear Entorno Virtual](#2-crear-entorno-virtual)
    - [3. Instalar Dependencias](#3-instalar-dependencias)
  - [Configuración](#configuración)
    - [Variables de Entorno](#variables-de-entorno)
    - [Migraciones de Base de Datos](#migraciones-de-base-de-datos)
    - [Crear Superusuario (Opcional)](#crear-superusuario-opcional)
  - [Ejecución](#ejecución)
    - [Servidor de Desarrollo](#servidor-de-desarrollo)
    - [Acceso al Panel de Administración](#acceso-al-panel-de-administración)
    - [Desactivar entorno virtual](#desactivar-entorno-virtual)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Modelos de Datos](#modelos-de-datos)
    - [Character (Personaje)](#character-personaje)
    - [Location (Ubicación)](#location-ubicación)
    - [Episode (Episodio)](#episode-episodio)
  - [Funcionalidades](#funcionalidades)
    - [Página Principal](#página-principal)
    - [Inicialización de Base de Datos](#inicialización-de-base-de-datos)
    - [CRUD de Personajes](#crud-de-personajes)
  - [API de Rick and Morty](#api-de-rick-and-morty)
    - [Clases de Servicio](#clases-de-servicio)
    - [Ejemplo de Uso del Servicio](#ejemplo-de-uso-del-servicio)

## Descripción General

Este proyecto es una aplicación web que demuestra la integración de Django con una API externa. Permite a los usuarios explorar, crear, editar y eliminar personajes del multiverso de Rick and Morty. La aplicación descarga automáticamente los datos desde la API oficial, incluyendo imágenes de los personajes, ubicaciones y episodios asociados.

## Características

- **Integración con API Externa**: Conexión con la API pública de Rick and Morty para obtener datos actualizados de personajes.
- **Operaciones CRUD Completas**: Crear, visualizar, editar y eliminar personajes de la base de datos local.
- **Gestión de Imágenes**: Descarga y almacenamiento local de imágenes de personajes.
- **Relaciones de Datos**: Manejo de relaciones entre personajes, ubicaciones y episodios.
- **Interfaz Moderna**: Diseño responsive con temática inspirada en la serie.
- **Sistema de Mensajes**: Notificaciones visuales para acciones del usuario (éxito, error, advertencia).
- **Panel de Estadísticas**: Visualización del total de personajes, ubicaciones y episodios.
- **Paginación Automática**: Carga de datos con soporte para paginación de la API.

## Tecnologías Utilizadas

| Tecnología | Versión | Descripción |
|------------|---------|-------------|
| Python | 3.10+ | Lenguaje de programación |
| Django | 6.0.1+ | Framework web |
| SQLite | 3 | Base de datos por defecto |
| Pillow | 10.0.0+ | Procesamiento de imágenes |
| Requests | 2.31.0+ | Cliente HTTP para consumo de API |

## Requisitos Previos

Antes de comenzar, asegúrese de tener instalado:

- **Python 3.10 o superior**: [Descargar Python](https://www.python.org/downloads/)
- **pip**: Gestor de paquetes de Python (incluido con Python 3.4+)
- **Git** (opcional): Para clonar el repositorio

Para verificar las versiones instaladas:

```bash
python --version
pip --version
```

## Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/su-usuario/Rick-and-Morty-API-CRUD.git
cd Rick-and-Morty-API-CRUD
```

### 2. Crear Entorno Virtual

Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.

**En Linux/macOS:**

```bash
python3 -m venv env
. env/bin/activate
```

**En Windows:**

```bash
python -m venv env
env\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

## Configuración

### Variables de Entorno

El proyecto soporta las siguientes variables de entorno para configuración. Puede crear un archivo `.env` o configurarlas directamente en su sistema:

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `DJANGO_SECRET_KEY` | Clave secreta de Django (obligatorio en producción) | Clave de desarrollo |
| `DJANGO_DEBUG` | Modo de depuración | `True` |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos (separados por coma) | `[]` |

**Ejemplo de configuración para producción:**

```bash
export DJANGO_SECRET_KEY='su-clave-secreta-segura-aqui'
export DJANGO_DEBUG='False'
export DJANGO_ALLOWED_HOSTS='ejemplo.com,www.ejemplo.com'
```

### Migraciones de Base de Datos

Ejecute las migraciones para crear las tablas necesarias en la base de datos:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Crear Superusuario (Opcional)

Para acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

## Ejecución

### Servidor de Desarrollo

```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://127.0.0.1:8000/`

### Acceso al Panel de Administración

Si creó un superusuario, puede acceder al panel de administración en:

`http://127.0.0.1:8000/admin/`

### Desactivar entorno virtual

**En Linux/macOS:**

```bash
deactivate
```

**En Windows:**

```bash
deactivate
```

## Estructura del Proyecto

```
Rick-and-Morty-API-CRUD/
├── manage.py                    # Script de gestión de Django
├── requirements.txt             # Dependencias del proyecto
├── README.md                    # Documentación del proyecto
├── media/                       # Archivos multimedia subidos
│   └── characters/              # Imágenes de personajes
├── myAPIapp/                    # Aplicación principal
│   ├── __init__.py
│   ├── admin.py                 # Configuración del admin
│   ├── api_service.py           # Servicio de consumo de API
│   ├── apps.py                  # Configuración de la app
│   ├── models.py                # Modelos de datos
│   ├── urls.py                  # Rutas de la aplicación
│   ├── views.py                 # Vistas y lógica de negocio
│   ├── migrations/              # Migraciones de base de datos
│   └── templates/               # Plantillas HTML
│       └── rickmorty_app/
│           ├── base.html                    # Plantilla base
│           ├── index.html                   # Página principal
│           ├── character_detail.html        # Detalle de personaje
│           ├── character_form.html          # Formulario de personaje
│           └── character_confirm_delete.html # Confirmación de eliminación
└── rick_and_morty_api_crud/     # Configuración del proyecto
    ├── __init__.py
    ├── asgi.py                  # Configuración ASGI
    ├── settings.py              # Configuración de Django
    ├── urls.py                  # Rutas principales
    └── wsgi.py                  # Configuración WSGI
```

## Modelos de Datos

### Character (Personaje)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | CharField | Nombre del personaje |
| `image` | ImageField | Imagen del personaje |
| `location` | ForeignKey | Ubicación actual (relación con Location) |
| `episode` | ManyToManyField | Episodios en los que aparece |

### Location (Ubicación)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | CharField | Nombre de la ubicación |
| `dimension` | CharField | Dimensión (ej: Dimension C-137) |

### Episode (Episodio)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | CharField | Nombre del episodio |
| `air_date` | CharField | Fecha de emisión |

## Funcionalidades

### Página Principal

- Visualización de todos los personajes en formato de tarjetas.
- Panel de estadísticas con conteo de personajes, ubicaciones y episodios.
- Botón para inicializar la base de datos desde la API.
- Acciones rápidas: ver, editar y eliminar personajes.

### Inicialización de Base de Datos

Al presionar el botón "Inicializar Base de Datos", la aplicación:

1. Consume la API de Rick and Morty con paginación.
2. Descarga hasta 150 personajes por defecto.
3. Crea registros de ubicaciones y episodios relacionados.
4. Descarga y almacena las imágenes localmente.
5. Muestra estadísticas de la operación (creados, omitidos, errores).

### CRUD de Personajes

| Operación | Ruta | Descripción |
|-----------|------|-------------|
| Listar | `/` | Página principal con todos los personajes |
| Crear | `/character/create/` | Formulario para nuevo personaje |
| Ver | `/character/<id>/` | Detalle de un personaje |
| Editar | `/character/<id>/edit/` | Formulario de edición |
| Eliminar | `/character/<id>/delete/` | Confirmación y eliminación |

## API de Rick and Morty

La aplicación consume la [API pública de Rick and Morty](https://rickandmortyapi.com/), que proporciona:

- **Personajes**: Información completa de los personajes de la serie.
- **Ubicaciones**: Lugares del multiverso.
- **Episodios**: Lista de todos los episodios.

### Clases de Servicio

El archivo `api_service.py` contiene dos clases principales:

- **`RickAndMortyAPI`**: Métodos estáticos para consumir la API externa.
- **`DataLoader`**: Métodos para cargar datos de la API a la base de datos local.

### Ejemplo de Uso del Servicio

```python
from myAPIapp.api_service import RickAndMortyAPI, DataLoader

# Obtener un personaje específico
character = RickAndMortyAPI.get_character_by_id(1)

# Cargar personajes a la base de datos
stats = DataLoader.load_characters(limit=50)
```