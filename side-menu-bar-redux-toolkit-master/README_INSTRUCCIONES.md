# Instrucciones para usar la aplicación

## Modos de funcionamiento

La aplicación puede funcionar en dos modos:

### 1. Modo normal (con Oracle Database)
- Requiere Oracle Database corriendo en localhost:1521
- Usa credenciales reales para conectarse a la base de datos
- Para activar este modo, asegúrese de que `USE_MOCK_DATABASE=false` en el archivo `.env`

### 2. Modo mock (para desarrollo)
- No requiere Oracle Database
- Usa datos de ejemplo para simular la base de datos
- Para activar este modo, establezca `USE_MOCK_DATABASE=true` en el archivo `.env` o use el script `start_mock.bat`

## Iniciar la aplicación

### Backend
1. **Modo normal**:
   ```
   cd backend
   python run.py
   ```

2. **Modo mock**:
   ```
   cd backend
   start_mock.bat
   ```
   O manualmente:
   ```
   cd backend
   set USE_MOCK_DATABASE=true
   python run.py
   ```

### Frontend
```
pnpm install
pnpm dev
```

## Funcionalidades implementadas

1. **CRUD de usuarios**:
   - Crear nuevos usuarios
   - Leer lista de usuarios
   - Actualizar información de usuarios
   - Eliminar usuarios (eliminación lógica)

2. **Eliminación lógica**:
   - Los usuarios no se eliminan físicamente de la base de datos
   - Se marca su estado como "deleted"
   - Se pueden restaurar posteriormente

3. **Restauración de usuarios**:
   - Los usuarios eliminados pueden ser restaurados
   - Su estado se cambia de "deleted" a "active"

4. **Visualización de usuarios eliminados**:
   - Se puede ver la lista de usuarios eliminados

## Solución de problemas

### Error "DPY-4027: no configuration directory specified"
Este error ocurre cuando hay problemas con la configuración del Oracle Wallet. 
- Solución: Usar el modo mock o asegurarse de que Oracle esté correctamente configurado

### Error de conexión a Oracle
- Verifique que Oracle Database esté corriendo
- Verifique que los parámetros de conexión sean correctos
- Verifique que el firewall no bloquee el puerto 1521

### No tengo Oracle instalado
- Use el modo mock estableciendo `USE_MOCK_DATABASE=true` en el archivo `.env`
- O ejecute el backend con `start_mock.bat`