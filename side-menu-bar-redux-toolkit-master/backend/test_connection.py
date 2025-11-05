"""
Script de prueba para verificar la conexión a la base de datos
"""
import os
import sys

# Añadir el directorio backend al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.config.database import db
from app.setting import settings

def test_connection():
    """Probar la conexión a la base de datos"""
    print("=== Configuración de la base de datos ===")
    print(f"ORACLE_USER: {settings.ORACLE_USER}")
    print(f"ORACLE_HOST: {settings.ORACLE_HOST}")
    print(f"ORACLE_PORT: {settings.ORACLE_PORT}")
    print(f"ORACLE_SERVICE_NAME: {settings.ORACLE_SERVICE_NAME}")
    print(f"DB_USER: {settings.DB_USER}")
    print(f"DB_TNS_NAME: {settings.DB_TNS_NAME}")
    
    print("\n=== Intentando conectar a la base de datos ===")
    try:
        conn = db.get_connection()
        print("✓ Conexión exitosa")
        
        # Probar una consulta simple
        try:
            result = db.execute_query("SELECT 1 as test FROM DUAL")
            print("✓ Consulta de prueba exitosa")
            print(f"  Resultado: {result}")
        except Exception as e:
            print(f"✗ Error en consulta de prueba: {e}")
            
    except Exception as e:
        print(f"✗ Error de conexión: {e}")
        print("\n=== Activando modo mock para pruebas ===")
        db.use_mock_mode(True)
        try:
            result = db.execute_query("SELECT * FROM USER_SYSTEM")
            print("✓ Modo mock activado correctamente")
            print(f"  Datos de ejemplo: {result}")
        except Exception as mock_error:
            print(f"✗ Error en modo mock: {mock_error}")

def test_user_operations():
    """Probar operaciones de usuario"""
    print("\n=== Probando operaciones de usuario ===")
    try:
        # Activar modo mock si no hay conexión real
        db.use_mock_mode(True)
        
        # Probar obtener todos los usuarios
        users = db.execute_query("SELECT * FROM USER_SYSTEM")
        print(f"✓ Usuarios obtenidos: {len(users)}")
        
        # Probar crear un usuario
        result = db.execute_dml("INSERT INTO USER_SYSTEM (ID, USERNAME, PASSWORD, ROLE, STATUS) VALUES (4, 'testuser', 'password', 'user', 'active')")
        print(f"✓ Usuario creado: {result} filas afectadas")
        
        # Probar actualizar un usuario
        result = db.execute_dml("UPDATE USER_SYSTEM SET STATUS = 'deleted' WHERE ID = 1")
        print(f"✓ Usuario actualizado: {result} filas afectadas")
        
        print("✓ Todas las operaciones de prueba completadas exitosamente")
        
    except Exception as e:
        print(f"✗ Error en operaciones de usuario: {e}")

if __name__ == "__main__":
    test_connection()
    test_user_operations()