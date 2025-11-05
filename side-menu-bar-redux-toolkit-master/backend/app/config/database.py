"""
Configuración de conexión a Oracle Database con soporte para Wallet y TNS
"""
import oracledb
from app.setting import settings
from typing import Optional
import os

class MockDatabase:
    """Clase mock para simular la base de datos cuando Oracle no está disponible"""
    
    # Datos de ejemplo para pruebas
    mock_data = [
        {"id": 1, "username": "admin", "password": "********", "role": "admin", "status": "active"},
        {"id": 2, "username": "user1", "password": "********", "role": "user", "status": "active"},
        {"id": 3, "username": "user2", "password": "********", "role": "user", "status": "deleted"}
    ]
    
    @staticmethod
    def execute_query(query: str, params: Optional[dict] = None) -> list:
        """Simular consulta SELECT"""
        # Devolver datos de ejemplo para pruebas
        if "USER_SYSTEM" in query.upper():
            # Si la consulta busca usuarios eliminados, filtrar por status deleted
            if "deleted" in query.lower():
                return [user for user in MockDatabase.mock_data if user["status"] == "deleted"]
            # Si la consulta busca todos los usuarios, devolver todos
            elif "order by id" in query.lower():
                return MockDatabase.mock_data
            # Si la consulta busca por ID, filtrar por ID
            elif "where id" in query.lower() and params and "user_id" in params:
                return [user for user in MockDatabase.mock_data if user["id"] == params["user_id"]]
        return []
    
    @staticmethod
    def execute_dml(query: str, params: Optional[dict] = None) -> int:
        """Simular INSERT, UPDATE, DELETE"""
        # Simular que la operación fue exitosa
        return 1

class OracleDatabase:
    """Clase para manejar la conexión a Oracle Database con Wallet/TNS"""
    
    _connection: Optional[oracledb.Connection] = None
    
    @classmethod
    def get_connection(cls) -> oracledb.Connection:
        """Obtener conexión a la base de datos usando TNS con Wallet o DSN estándar"""
        if settings.USE_MOCK_DATABASE:
            raise Exception("Modo mock activado - no se requiere conexión real")
            
        if cls._connection is None:
            try:
                # Método 1: Usar DSN estándar (host/port/service) - método preferido para evitar problemas de wallet
                if settings.ORACLE_USER and settings.ORACLE_PASSWORD:
                    dsn = oracledb.makedsn(
                        host=settings.ORACLE_HOST,
                        port=settings.ORACLE_PORT,
                        service_name=settings.ORACLE_SERVICE_NAME
                    )
                    
                    cls._connection = oracledb.connect(
                        user=settings.ORACLE_USER,
                        password=settings.ORACLE_PASSWORD,
                        dsn=dsn
                    )
                    print(f"✓ Conexión a Oracle establecida: {settings.ORACLE_USER}@{settings.ORACLE_HOST}:{settings.ORACLE_PORT}/{settings.ORACLE_SERVICE_NAME}")
                
                # Método 2: Usar TNS con Wallet (fallback)
                elif settings.DB_USER and settings.DB_PASS and settings.DB_TNS_NAME:
                    # Configurar wallet si está disponible
                    wallet_path = None
                    if settings.DB_WALLET_DIR:
                        # Convertir ruta relativa a absoluta si es necesario
                        wallet_path = os.path.abspath(settings.DB_WALLET_DIR) if not os.path.isabs(settings.DB_WALLET_DIR) else settings.DB_WALLET_DIR
                    
                    if wallet_path and os.path.exists(wallet_path):
                        # Establecer variables de entorno para wallet
                        os.environ["TNS_ADMIN"] = wallet_path
                        
                        # Configurar wallet para la conexión con oracledb
                        connection_params = {
                            "user": settings.DB_USER,
                            "password": settings.DB_PASS,
                            "dsn": settings.DB_TNS_NAME,
                            "config_dir": wallet_path,
                            "wallet_location": wallet_path,
                            "wallet_password": settings.WALLET_PASSWORD
                        }
                        
                        cls._connection = oracledb.connect(**connection_params)
                        print(f"✓ Conexión a Oracle establecida con Wallet: {settings.DB_USER}@{settings.DB_TNS_NAME}")
                        print(f"  Wallet: {wallet_path}")
                    else:
                        # Conexión TNS sin wallet
                        cls._connection = oracledb.connect(
                            user=settings.DB_USER,
                            password=settings.DB_PASS,
                            dsn=settings.DB_TNS_NAME
                        )
                        print(f"✓ Conexión a Oracle establecida con TNS: {settings.DB_USER}@{settings.DB_TNS_NAME}")
                else:
                    raise ValueError("No se proporcionaron credenciales de base de datos. Configure ORACLE_USER/ORACLE_PASSWORD o DB_USER/DB_PASS/DB_TNS_NAME")
                    
            except Exception as e:
                print(f"✗ Error al conectar a Oracle: {str(e)}")
                raise
        return cls._connection
    
    @classmethod
    def close_connection(cls):
        """Cerrar conexión a la base de datos"""
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None
    
    @classmethod
    def execute_query(cls, query: str, params: Optional[dict] = None) -> list:
        """Ejecutar consulta SELECT"""
        if settings.USE_MOCK_DATABASE:
            return MockDatabase.execute_query(query, params)
            
        conn = cls.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Obtener nombres de columnas
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            
            # Obtener resultados
            rows = cursor.fetchall()
            
            # Convertir a lista de diccionarios
            result = []
            for row in rows:
                row_dict = {}
                for i, col in enumerate(columns):
                    row_dict[col.lower()] = row[i]
                result.append(row_dict)
            
            return result
        finally:
            cursor.close()
    
    @classmethod
    def execute_dml(cls, query: str, params: Optional[dict] = None) -> int:
        """Ejecutar INSERT, UPDATE, DELETE"""
        if settings.USE_MOCK_DATABASE:
            return MockDatabase.execute_dml(query, params)
            
        conn = cls.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise
        finally:
            cursor.close()

# Instancia global
db = OracleDatabase()