# 🔗 Guía de Conexión Frontend - Backend

Esta guía explica cómo conectar y ejecutar el frontend y backend juntos.

## 📋 Prerrequisitos

1. **Backend**:
   - Python 3.11+
   - Entorno virtual activado
   - Dependencias instaladas

2. **Frontend**:
   - Node.js instalado
   - Dependencias instaladas (`npm install`)

## 🚀 Pasos para Conectar

### 1. Configurar Variables de Entorno

#### Backend (`backend/.env`):
```env
HOST=0.0.0.0
PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
# ... otras configuraciones
```

#### Frontend (`src/.env` o `.env` en la raíz):
```env
VITE_API_BASE_URL=http://localhost:8000
```

### 2. Iniciar el Backend

```bash
# En la carpeta backend
cd backend

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate

# Ejecutar servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en: **http://localhost:8000**

### 3. Iniciar el Frontend

```bash
# En la carpeta raíz del proyecto
npm run dev
```

El frontend estará disponible en: **http://localhost:5173**

## ✅ Verificar Conexión

1. **Backend funcionando**:
   - Abre: http://localhost:8000/docs
   - Deberías ver la documentación Swagger de FastAPI

2. **Frontend conectado**:
   - Abre: http://localhost:5173
   - Navega a la página de Items
   - Deberías ver los items cargados desde el backend

## 🔍 Endpoints Disponibles

### Items
- `GET /api/items` - Obtener todos los items
- `GET /api/items/{id}` - Obtener un item
- `POST /api/items` - Crear item
- `PUT /api/items/{id}` - Actualizar item
- `DELETE /api/items/{id}` - Eliminar item

### Usuarios
- `GET /api/users` - Obtener todos los usuarios
- `GET /api/users/{id}` - Obtener un usuario
- `POST /api/users` - Crear usuario

### Órdenes
- `GET /api/orders` - Obtener todas las órdenes
- `GET /api/orders/{id}` - Obtener una orden
- `POST /api/orders` - Crear orden

### Autenticación
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener usuario actual

## 🐛 Solución de Problemas

### Error: CORS
**Problema**: El frontend no puede hacer peticiones al backend.

**Solución**: 
- Verifica que `CORS_ORIGINS` en `backend/.env` incluya `http://localhost:5173`
- Reinicia el servidor backend

### Error: Connection refused
**Problema**: El frontend no puede conectarse al backend.

**Solución**:
- Verifica que el backend esté corriendo en el puerto 8000
- Verifica que `VITE_API_BASE_URL` esté configurado correctamente
- Verifica que no haya un firewall bloqueando la conexión

### Error: 404 Not Found
**Problema**: Los endpoints no se encuentran.

**Solución**:
- Verifica que las rutas en el backend usen el prefijo `/api/`
- Verifica que las URLs en el frontend usen `API_ENDPOINTS`

## 📝 Notas

- El backend usa datos mock por ahora. Para producción, conectar con Oracle Database.
- El frontend usa Redux Toolkit para manejar el estado y las peticiones API.
- Todas las peticiones pasan por el cliente API centralizado en `src/config/api.ts`.

## 🎯 Próximos Pasos

1. Implementar autenticación real con JWT
2. Conectar backend con Oracle Database
3. Agregar validación de formularios en el frontend
4. Implementar manejo de errores más robusto
5. Agregar tests

