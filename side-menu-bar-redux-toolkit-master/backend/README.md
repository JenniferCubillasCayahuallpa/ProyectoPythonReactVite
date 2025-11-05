# Backend API - Side Menu Bar

Backend desarrollado con **FastAPI** y **Python** para la aplicación Side Menu Bar.

## 🚀 Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **Python 3.11+** - Lenguaje de programación
- **SQLAlchemy** - ORM para base de datos
- **Oracle Database** - Base de datos
- **Docker** - Contenedorización
- **Uvicorn** - Servidor ASGI

## 📋 Requisitos Previos

- Python 3.11 o superior
- Docker (opcional, para Oracle)
- pip

## 🛠️ Instalación

### 1. Crear Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate

# Activar entorno virtual (Windows)
venv\Scripts\activate
```

### 2. Instalar Dependencias

```bash
# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
# Especialmente importante: configurar credenciales de Oracle
```

## 🐳 Docker

### Iniciar Oracle con Docker

```bash
# Revisar contenedores activos
docker ps

# Revisar todos los contenedores (activos e inactivos)
docker ps -a

# Iniciar contenedor de Oracle
docker start oracle-docker
```

### Ejecutar con Docker Compose

```bash
# Construir y ejecutar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

## 🚀 Ejecutar la Aplicación

### Desarrollo

```bash
# Ejecutar servidor de desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# O usando Python directamente
python -m app.main
```

### Producción

```bash
# Ejecutar con uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📡 Endpoints

Una vez ejecutando, la API estará disponible en:

- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Endpoints Disponibles

- `/api/auth/login` - Login de usuario
- `/api/auth/me` - Información del usuario actual
- `/api/users/` - CRUD de usuarios
- `/api/items/` - CRUD de items
- `/api/orders/` - CRUD de órdenes

## 📁 Estructura del Proyecto

```
backend/
├── app/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── database.py      # Configuración de base de datos
│   │   └── settings.py      # Configuración general
│   ├── models/              # Modelos de base de datos
│   ├── routes/              # Rutas/Endpoints
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── items.py
│   │   └── orders.py
│   ├── schemas/             # Schemas Pydantic
│   ├── services/            # Lógica de negocio
│   ├── __init__.py
│   └── main.py              # Aplicación principal
├── tests/                   # Tests
├── .env.example             # Ejemplo de variables de entorno
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 🔧 Configuración

### Variables de Entorno

Crear archivo `.env` basado en `.env.example`:

```env
HOST=0.0.0.0
PORT=8000
DEBUG=True
ORACLE_USER=tu_usuario
ORACLE_PASSWORD=tu_contraseña
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=orcl
SECRET_KEY=tu-secret-key-segura
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## 🧪 Testing

```bash
# Ejecutar tests (cuando estén implementados)
pytest
```

## 📝 Notas

- El backend está configurado para conectarse a Oracle Database
- Asegúrate de tener Oracle corriendo antes de ejecutar la aplicación
- Los endpoints actualmente usan datos mock, se debe implementar la conexión real a la base de datos
- Para producción, cambiar `DEBUG=False` y usar una `SECRET_KEY` segura

## 🔗 Integración con Frontend

El backend está configurado para aceptar peticiones del frontend React en:
- http://localhost:5173 (Vite default)
- http://localhost:3000

Ajustar `CORS_ORIGINS` en `.env` si es necesario.

