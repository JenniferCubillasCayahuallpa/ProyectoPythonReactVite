# Configuración de Oracle Database

## Credenciales Configuradas

El sistema está configurado para conectarse a Oracle Database con las siguientes credenciales:

- **Usuario**: `DEVELOPER_02`
- **Contraseña**: `JenniferCubillas12345`
- **Host**: `localhost` (por defecto)
- **Puerto**: `1521` (por defecto)
- **Service Name**: `orcl` (por defecto)

## Configuración del archivo .env

Crea un archivo `.env` en la carpeta `backend/` con el siguiente contenido:

```env
# Configuración del servidor
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Base de datos Oracle
ORACLE_USER=DEVELOPER_02
ORACLE_PASSWORD=JenniferCubillas12345
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=orcl

# Configuración de seguridad
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## Estructura de la Tabla USER_SYSTEM

La aplicación espera una tabla con la siguiente estructura:

```sql
CREATE TABLE USER_SYSTEM (
    ID NUMBER PRIMARY KEY,
    USERNAME VARCHAR2(100) NOT NULL UNIQUE,
    PASSWORD VARCHAR2(255) NOT NULL,
    ROLE VARCHAR2(50) NOT NULL,
    STATUS VARCHAR2(50) NOT NULL
);
```

## Ejecutar la Aplicación

1. Activar el entorno virtual:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. Instalar dependencias (si no están instaladas):
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar el servidor:
   ```bash
   python run.py
   ```

   O con uvicorn directamente:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

## Notas Importantes

- Asegúrate de que Oracle Database esté corriendo antes de iniciar la aplicación
- Las contraseñas se almacenan con hash MD5 (en producción, usar bcrypt)
- El sistema usa conexión singleton a la base de datos
- Los errores de conexión se mostrarán en la consola del servidor

