"""
Punto de entrada principal de la aplicación
"""
from dotenv import load_dotenv
import os

load_dotenv() 

from app import app
from app.config.database import db
import uvicorn
from app.setting import settings

if __name__ == "__main__":
    if settings.USE_MOCK_DATABASE:
        print("⚠️  Modo MOCK activado - usando datos de ejemplo")
        # No need to do anything else, the database will automatically use mock mode
    else:
        # Verificar conexión a Oracle al inicio
        try:
            conn = db.get_connection()
            print(f"✓ Conexión a Oracle verificada: {settings.ORACLE_USER}@{settings.ORACLE_HOST}:{settings.ORACLE_PORT}")
        except Exception as e:
            print(f"⚠️  No se pudo conectar a Oracle: {e}")
            print("ℹ️  La aplicación se ejecutará en modo limitado")
            print("ℹ️  Para usar datos reales, asegúrese de que Oracle esté corriendo")
            print("ℹ️  Para desarrollo, puede activar el modo mock añadiendo USE_MOCK_DATABASE=true a su .env")
    
    print(f"🚀 Iniciando servidor en http://{settings.HOST}:{settings.PORT}")
    
    # Ejecutar aplicación
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )