"""
Rutas de usuarios - USER_SYSTEM (conectado a Oracle Database)
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from app.services.user_service import UserService

router = APIRouter()

# Modelos Pydantic para validación
class UserCreate(BaseModel):
    """Modelo para crear usuario"""
    username: str
    password: str
    role: str = "user"
    status: str = "A"  # Cambiar de "active" a "A" para que coincida con la base de datos

class UserUpdate(BaseModel):
    """Modelo para actualizar usuario"""
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None

class UserResponse(BaseModel):
    """Modelo de respuesta de usuario"""
    id: int
    username: str
    password: str
    role: str
    status: str

class DeleteResponse(BaseModel):
    """Modelo de respuesta para eliminación"""
    message: str
    id: int

class RestoreResponse(BaseModel):
    """Modelo de respuesta para restauración"""
    message: str
    user: UserResponse

@router.get("", response_model=List[UserResponse])
async def get_users():
    """Obtener todos los usuarios de USER_SYSTEM desde Oracle"""
    try:
        users = UserService.get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {str(e)}")

@router.get("/deleted", response_model=List[UserResponse])
async def get_deleted_users():
    """Obtener todos los usuarios eliminados lógicamente"""
    try:
        users = UserService.get_deleted_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios eliminados: {str(e)}")

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Obtener un usuario por ID desde Oracle"""
    try:
        user = UserService.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {str(e)}")

@router.post("", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Crear un nuevo usuario en USER_SYSTEM en Oracle"""
    try:
        new_user = UserService.create_user({
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "status": user.status
        })
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {str(e)}")

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate):
    """Actualizar un usuario en Oracle"""
    try:
        update_data = {}
        if user.username is not None:
            update_data["username"] = user.username
        if user.password is not None:
            update_data["password"] = user.password
        if user.role is not None:
            update_data["role"] = user.role
        if user.status is not None:
            update_data["status"] = user.status
        
        updated_user = UserService.update_user(user_id, update_data)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {str(e)}")

@router.delete("/{user_id}", response_model=DeleteResponse)
async def delete_user(user_id: int):
    """Eliminar un usuario de Oracle (eliminación lógica)"""
    try:
        success = UserService.delete_user(user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully", "id": user_id}
    except HTTPException:
        raise
    except ValueError as e:
        # Error de validación (foreign keys, dependencias)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        error_msg = str(e)
        # Si es un error de foreign key, dar mensaje más claro
        if "ORA-01407" in error_msg or "cannot update" in error_msg.lower():
            raise HTTPException(
                status_code=400, 
                detail="No se puede eliminar el usuario porque tiene registros relacionados en otras tablas. "
                       "Elimine primero los registros relacionados (por ejemplo, en la tabla SALE)."
            )
        raise HTTPException(status_code=500, detail=f"Error al eliminar usuario: {error_msg}")

@router.post("/{user_id}/restore", response_model=RestoreResponse)
async def restore_user(user_id: int):
    """Restaurar un usuario eliminado lógicamente"""
    try:
        restored_user = UserService.restore_user(user_id)
        if not restored_user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User restored successfully", "user": restored_user}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al restaurar usuario: {str(e)}")