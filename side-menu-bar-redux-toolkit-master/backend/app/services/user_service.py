"""
Servicio de usuarios - Lógica de negocio con Oracle Database
"""
from typing import List, Optional, Dict
from app.config.database import db
import hashlib

class UserService:
    """Servicio para manejar la lógica de negocio de usuarios de USER_SYSTEM"""
    
    @staticmethod
    def get_all_users() -> List[Dict]:
        """Obtener todos los usuarios de USER_SYSTEM"""
        try:
            query = """
                SELECT ID, USERNAME, PASSWORD, ROLE, STATUS 
                FROM USER_SYSTEM 
                ORDER BY ID
            """
            results = db.execute_query(query)
            
            # Formatear resultados
            users = []
            for row in results:
                users.append({
                    "id": row.get("id"),
                    "username": row.get("username"),
                    "password": "********",  # No mostrar password real
                    "role": row.get("role"),
                    "status": row.get("status")
                })
            return users
        except Exception as e:
            print(f"Error al obtener usuarios: {str(e)}")
            # Devolver lista vacía si hay error de conexión
            return []
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict]:
        """Obtener usuario por ID"""
        try:
            query = """
                SELECT ID, USERNAME, PASSWORD, ROLE, STATUS 
                FROM USER_SYSTEM 
                WHERE ID = :user_id
            """
            results = db.execute_query(query, {"user_id": user_id})
            
            if not results:
                return None
            
            row = results[0]
            return {
                "id": row.get("id"),
                "username": row.get("username"),
                "password": "********",  # No mostrar password real
                "role": row.get("role"),
                "status": row.get("status")
            }
        except Exception as e:
            print(f"Error al obtener usuario: {str(e)}")
            return None
    
    @staticmethod
    def create_user(user_data: Dict) -> Dict:
        """Crear un nuevo usuario en USER_SYSTEM"""
        try:
            # Verificar si el username ya existe
            check_query = """
                SELECT COUNT(*) as count 
                FROM USER_SYSTEM 
                WHERE UPPER(USERNAME) = UPPER(:username)
            """
            check_result = db.execute_query(check_query, {"username": user_data["username"]})
            if check_result and check_result[0].get("count", 0) > 0:
                raise ValueError(f"El usuario '{user_data['username']}' ya existe")
            
            # Hash de la contraseña (simple hash MD5 para este ejemplo)
            # En producción, usar bcrypt o similar
            password_hash = hashlib.md5(user_data["password"].encode()).hexdigest()
            
            # Insertar usuario (dejar que la base de datos genere el ID automáticamente)
            insert_query = """
                INSERT INTO USER_SYSTEM (USERNAME, PASSWORD, ROLE, STATUS)
                VALUES (:username, :password, :role, :status)
            """
            params = {
                "username": user_data["username"],
                "password": password_hash,
                "role": user_data.get("role", "user"),
                "status": user_data.get("status", "A")  # Usar 'A' para activo
            }
            
            db.execute_dml(insert_query, params)
            
            # Obtener el usuario recién creado
            get_user_query = """
                SELECT ID, USERNAME, PASSWORD, ROLE, STATUS 
                FROM USER_SYSTEM 
                WHERE USERNAME = :username AND PASSWORD = :password
                ORDER BY ID DESC FETCH FIRST 1 ROWS ONLY
            """
            user_result = db.execute_query(get_user_query, {
                "username": user_data["username"],
                "password": password_hash
            })
            
            if not user_result:
                raise Exception("No se pudo obtener el usuario recién creado")
            
            row = user_result[0]
            return {
                "id": row.get("id"),
                "username": row.get("username"),
                "password": "********",
                "role": row.get("role"),
                "status": row.get("status")
            }
        except Exception as e:
            print(f"Error al crear usuario: {str(e)}")
            raise
    
    @staticmethod
    def update_user(user_id: int, user_data: Dict) -> Optional[Dict]:
        """Actualizar usuario en USER_SYSTEM"""
        try:
            # Verificar que el usuario existe
            existing = UserService.get_user_by_id(user_id)
            if not existing:
                return None
            
            # Construir query de actualización dinámicamente
            update_fields = []
            params: Dict[str, object] = {"user_id": user_id}
            
            if "username" in user_data and user_data["username"]:
                # Verificar si el nuevo username ya existe (si es diferente)
                check_query = """
                    SELECT COUNT(*) as count 
                    FROM USER_SYSTEM 
                    WHERE UPPER(USERNAME) = UPPER(:username) AND ID != :user_id
                """
                check_result = db.execute_query(check_query, {
                    "username": user_data["username"],
                    "user_id": user_id
                })
                if check_result and check_result[0].get("count", 0) > 0:
                    raise ValueError(f"El usuario '{user_data['username']}' ya existe")
                
                update_fields.append("USERNAME = :username")
                params["username"] = user_data["username"]
            
            if "password" in user_data and user_data["password"]:
                password_hash = hashlib.md5(user_data["password"].encode()).hexdigest()
                update_fields.append("PASSWORD = :password")
                params["password"] = password_hash
            
            if "role" in user_data and user_data["role"]:
                update_fields.append("ROLE = :role")
                params["role"] = user_data["role"]
            
            if "status" in user_data and user_data["status"]:
                update_fields.append("STATUS = :status")
                params["status"] = user_data["status"]
            
            if not update_fields:
                return existing
            
            update_query = f"""
                UPDATE USER_SYSTEM 
                SET {', '.join(update_fields)}
                WHERE ID = :user_id
            """
            
            db.execute_dml(update_query, params)
            
            # Retornar usuario actualizado
            return UserService.get_user_by_id(user_id)
        except Exception as e:
            print(f"Error al actualizar usuario: {str(e)}")
            raise
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        """Eliminar usuario de USER_SYSTEM (eliminación lógica)"""
        try:
            # Verificar que el usuario existe
            existing = UserService.get_user_by_id(user_id)
            if not existing:
                return False
            
            # Eliminación lógica: cambiar el estado a 'I' (inactivo) en lugar de eliminar físicamente
            # Basado en el error ORA-02290, 'E' no es un valor válido, probablemente 'I' sí lo sea
            update_query = """
                UPDATE USER_SYSTEM 
                SET STATUS = 'I'
                WHERE ID = :user_id
            """
            params: Dict[str, object] = {"user_id": user_id}
            
            db.execute_dml(update_query, params)
            return True
        except Exception as e:
            print(f"Error al eliminar usuario: {str(e)}")
            raise
    
    @staticmethod
    def restore_user(user_id: int) -> Optional[Dict]:
        """Restaurar usuario eliminado lógicamente"""
        try:
            # Verificar que el usuario existe
            existing = UserService.get_user_by_id(user_id)
            if not existing:
                return None
            
            # Restaurar usuario: cambiar el estado a 'A' (activo)
            update_query = """
                UPDATE USER_SYSTEM 
                SET STATUS = 'A'
                WHERE ID = :user_id
            """
            params: Dict[str, object] = {"user_id": user_id}
            
            db.execute_dml(update_query, params)
            
            # Retornar usuario restaurado
            return UserService.get_user_by_id(user_id)
        except Exception as e:
            print(f"Error al restaurar usuario: {str(e)}")
            raise
    
    @staticmethod
    def get_deleted_users() -> List[Dict]:
        """Obtener todos los usuarios eliminados lógicamente"""
        try:
            query = """
                SELECT ID, USERNAME, PASSWORD, ROLE, STATUS 
                FROM USER_SYSTEM 
                WHERE STATUS = 'I'
                ORDER BY ID
            """
            results = db.execute_query(query)
            
            # Formatear resultados
            users = []
            for row in results:
                users.append({
                    "id": row.get("id"),
                    "username": row.get("username"),
                    "password": "********",  # No mostrar password real
                    "role": row.get("role"),
                    "status": row.get("status")
                })
            return users
        except Exception as e:
            print(f"Error al obtener usuarios eliminados: {str(e)}")
            return []