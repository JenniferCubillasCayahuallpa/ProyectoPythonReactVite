"""
Modelo de usuario para base de datos - USER_SYSTEM
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserSystem(Base):
    """Modelo de usuario en la base de datos - Tabla USER_SYSTEM"""
    __tablename__ = "USER_SYSTEM"
    
    ID = Column(Integer, primary_key=True, index=True)
    USERNAME = Column(String(100), unique=True, nullable=False, index=True)
    PASSWORD = Column(String(255), nullable=False)
    ROLE = Column(String(50), default="user", nullable=False)
    STATUS = Column(String(50), default="active", nullable=False)
    
    def to_dict(self):
        """Convertir modelo a diccionario"""
        return {
            "id": self.ID,
            "username": self.USERNAME,
            "password": self.PASSWORD,
            "role": self.ROLE,
            "status": self.STATUS
        }

# Alias para compatibilidad
User = UserSystem

