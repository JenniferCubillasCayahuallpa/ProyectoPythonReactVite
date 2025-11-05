"""
Configuración de la aplicación
"""
import os
from dotenv import load_dotenv
import oracledb
from typing import List

load_dotenv()

class Config:
    # Base de datos Oracle y configuración de mi Wallet
    
    DB_USER = os.getenv("DB_USER", "DEVELOPER_02")
    DB_PASS = os.getenv("DB_PASS", "JenniferCubillas12345")
    DB_TNS_NAME = os.getenv("DB_TNS_NAME", "pruebavictoria_high")
    DB_WALLET_DIR = os.getenv("DB_WALLET_DIR") or os.path.join(os.path.dirname(os.path.dirname(__file__)), "Wallet_inversionesVictoria")
    WALLET_PASSWORD = os.getenv("DB_WALLET_PASSWORD", "Carlostomi12*")
    
    # Compatibilidad con configuración anterior (fallback)
    ORACLE_USER = os.getenv("ORACLE_USER")
    ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
    ORACLE_HOST = os.getenv("ORACLE_HOST", "localhost")
    ORACLE_PORT = int(os.getenv("ORACLE_PORT", "1521"))
    ORACLE_SERVICE_NAME = os.getenv("ORACLE_SERVICE_NAME", "orcl")
    
    # Modo mock para desarrollo
    USE_MOCK_DATABASE = os.getenv("USE_MOCK_DATABASE", "false").lower() == "true"
    
    # Servidor
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "5000"))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Seguridad
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
    
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "config_dir": DB_WALLET_DIR,
            "wallet_location": DB_WALLET_DIR,
            "wallet_password": WALLET_PASSWORD
        }
    }
    
    # URI estándar solo como placeholder
    SQLALCHEMY_DATABASE_URI = f"oracle+oracledb://{DB_USER}:{DB_PASS}@{DB_TNS_NAME}"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convierte CORS_ORIGINS string a lista"""
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

# Instancia global de configuración
settings = Config()