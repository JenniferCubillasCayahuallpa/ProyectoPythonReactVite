import { useEffect, useState } from "react";
import { useAppDispatch, useAppSelector } from "../store/store";
import { fetchUsers, deleteUser, createUser, updateUser, User, restoreUser, fetchDeletedUsers } from "../store/usersSlice";

export const UsersPage = () => {
  const dispatch = useAppDispatch();
  const { users, loading, error } = useAppSelector((state) => state.users);
  
  const [showModal, setShowModal] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    role: "user",
    status: "A"  // Cambiar a 'A' para activo
  });
  const [viewMode, setViewMode] = useState<"active" | "deleted">("active");

  useEffect(() => {
    if (viewMode === "active") {
      dispatch(fetchUsers());
    } else {
      dispatch(fetchDeletedUsers());
    }
  }, [dispatch, viewMode]);

  const handleDelete = async (id: number) => {
    if (window.confirm("¿Está seguro de eliminar este usuario?")) {
      try {
        const result = await dispatch(deleteUser(id));
        if (deleteUser.rejected.match(result)) {
          const errorMsg = result.payload as string || result.error?.message || "Error al eliminar usuario";
          alert(`Error: ${errorMsg}`);
          return;
        }
        // Refrescar lista solo si fue exitoso
        if (viewMode === "active") {
          dispatch(fetchUsers());
        } else {
          dispatch(fetchDeletedUsers());
        }
      } catch (err: any) {
        alert(`Error al eliminar: ${err?.message || "Error desconocido"}`);
      }
    }
  };

  const handleRestore = async (id: number) => {
    if (window.confirm("¿Está seguro de restaurar este usuario?")) {
      try {
        const result = await dispatch(restoreUser(id));
        if (restoreUser.rejected.match(result)) {
          const errorMsg = result.payload as string || result.error?.message || "Error al restaurar usuario";
          alert(`Error: ${errorMsg}`);
          return;
        }
        // Refrescar lista solo si fue exitoso
        if (viewMode === "active") {
          dispatch(fetchUsers());
        } else {
          dispatch(fetchDeletedUsers());
        }
      } catch (err: any) {
        alert(`Error al restaurar: ${err?.message || "Error desconocido"}`);
      }
    }
  };

  const handleEdit = (user: User) => {
    setEditingUser(user);
    setFormData({
      username: user.username,
      password: "",
      role: user.role,
      status: user.status
    });
    setShowModal(true);
  };

  const handleCreate = () => {
    setEditingUser(null);
    setFormData({
      username: "",
      password: "",
      role: "user",
      status: "A"  // Cambiar a 'A' para activo
    });
    setShowModal(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    
    try {
      if (editingUser) {
        // Actualizar usuario - solo enviar campos que tienen valor
        const updateData: any = {
          username: formData.username,
          role: formData.role,
          status: formData.status
        };
        // Solo incluir password si se proporcionó uno nuevo
        if (formData.password && formData.password.trim() !== "") {
          updateData.password = formData.password;
        }
        
        const result = await dispatch(updateUser({
          id: editingUser.id,
          data: updateData
        }));
        
        if (updateUser.rejected.match(result)) {
          const errorMsg = result.payload as string || result.error?.message || "Error al actualizar usuario";
          setFormError(errorMsg);
          return;
        }
      } else {
        // Crear usuario
        if (!formData.password || formData.password.trim() === "") {
          setFormError("La contraseña es requerida");
          return;
        }
        
        const result = await dispatch(createUser({
          username: formData.username,
          password: formData.password,
          role: formData.role,
          status: formData.status
        }));
        
        if (createUser.rejected.match(result)) {
          const errorMsg = result.payload as string || result.error?.message || "Error al crear usuario";
          setFormError(errorMsg);
          return;
        }
      }
      
      // Si todo salió bien, cerrar modal y refrescar
      setShowModal(false);
      setFormError(null);
      // Refrescar lista
      if (viewMode === "active") {
        dispatch(fetchUsers());
      } else {
        dispatch(fetchDeletedUsers());
      }
    } catch (err: any) {
      console.error("Error al guardar usuario:", err);
      setFormError(err?.message || "Error desconocido al guardar usuario");
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingUser(null);
    setFormError(null);
    setFormData({
      username: "",
      password: "",
      role: "user",
      status: "A"  // Cambiar a 'A' para activo
    });
  };

  if (loading) {
    return (
      <div className="p-4">
        <h1 className="text-2xl font-bold mb-4">Gestión de Usuarios - USER_SYSTEM</h1>
        <div className="text-center py-8">Cargando usuarios...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4">
        <h1 className="text-2xl font-bold mb-4">Gestión de Usuarios - USER_SYSTEM</h1>
        <div className="bg-red-100 text-red-700 p-4 rounded">
          Error: {error}
        </div>
      </div>
    );
  }

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Gestión de Usuarios - USER_SYSTEM</h1>
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode("active")}
            className={`px-4 py-2 rounded transition ${viewMode === "active" ? "bg-blue-600 text-white" : "bg-gray-200 hover:bg-gray-300"}`}
          >
            Activos
          </button>
          <button
            onClick={() => setViewMode("deleted")}
            className={`px-4 py-2 rounded transition ${viewMode === "deleted" ? "bg-red-600 text-white" : "bg-gray-200 hover:bg-gray-300"}`}
          >
            Eliminados
          </button>
          <button
            onClick={handleCreate}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
          >
            + Nuevo Usuario
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-100 text-red-700 p-4 rounded mb-4">
          Error: {error}
        </div>
      )}

      <div className="bg-white rounded border overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-100">
            <tr>
              <th className="text-left p-3 border-b">ID</th>
              <th className="text-left p-3 border-b">USERNAME</th>
              <th className="text-left p-3 border-b">PASSWORD</th>
              <th className="text-left p-3 border-b">ROLE</th>
              <th className="text-left p-3 border-b">STATUS</th>
              <th className="text-center p-3 border-b">Acciones</th>
            </tr>
          </thead>
          <tbody>
            {users.length === 0 ? (
              <tr>
                <td className="p-3 text-center text-gray-500" colSpan={6}>
                  No hay usuarios disponibles.
                </td>
              </tr>
            ) : (
              users.map((user) => (
                <tr key={user.id} className="border-b hover:bg-gray-50">
                  <td className="p-3">{user.id}</td>
                  <td className="p-3 font-medium">{user.username}</td>
                  <td className="p-3 text-gray-600">{user.password}</td>
                  <td className="p-3">
                    <span className={`px-2 py-1 rounded text-xs ${
                      user.role === "ADMIN" 
                        ? "bg-purple-100 text-purple-800" 
                        : "bg-blue-100 text-blue-800"
                    }`}>
                      {user.role}
                    </span>
                  </td>
                  <td className="p-3">
                    <span className={`px-2 py-1 rounded text-xs ${
                      user.status === "A" 
                        ? "bg-green-100 text-green-800" 
                        : "bg-red-100 text-red-800"
                    }`}>
                      {user.status === "A" ? "Activo" : "Eliminado"}
                    </span>
                  </td>
                  <td className="p-3">
                    <div className="flex gap-3 justify-center">
                      {viewMode === "active" ? (
                        <>
                          <button 
                            className="text-blue-600 hover:text-blue-800 underline text-sm"
                            onClick={() => handleEdit(user)}
                          >
                            Editar
                          </button>
                          <button 
                            className="text-red-600 hover:text-red-800 underline text-sm"
                            onClick={() => handleDelete(user.id)}
                          >
                            Eliminar
                          </button>
                        </>
                      ) : (
                        <button 
                          className="text-green-600 hover:text-green-800 underline text-sm"
                          onClick={() => handleRestore(user.id)}
                        >
                          Restaurar
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Modal de Crear/Editar Usuario */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">
              {editingUser ? "Editar Usuario" : "Nuevo Usuario"}
            </h2>
            
            {formError && (
              <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
                {formError}
              </div>
            )}
            
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1">Username</label>
                <input
                  type="text"
                  required
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  className="w-full border rounded px-3 py-2"
                  placeholder="Ingrese username"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium mb-1">
                  Password {editingUser && "(dejar vacío para no cambiar)"}
                </label>
                <input
                  type="password"
                  required={!editingUser}
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  className="w-full border rounded px-3 py-2"
                  placeholder="Ingrese password"
                />
              </div>

              <div className="mb-4">
                <label htmlFor="role-select" className="block text-sm font-medium mb-1">Role</label>
                <select
                  id="role-select"
                  value={formData.role}
                  onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                  className="w-full border rounded px-3 py-2"
                  aria-label="Seleccionar rol del usuario"
                >
                  <option value="user">User</option>
                  <option value="EMPLEADO">Empleado</option>
                  <option value="ADMIN">Admin</option>
                </select>
              </div>

              <div className="mb-4">
                <label htmlFor="status-select" className="block text-sm font-medium mb-1">Status</label>
                <select
                  id="status-select"
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  className="w-full border rounded px-3 py-2"
                  aria-label="Seleccionar estado del usuario"
                >
                  <option value="A">Activo</option>
                  <option value="I">Inactivo</option>
                </select>
              </div>

              <div className="flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={handleCloseModal}
                  className="px-4 py-2 border rounded hover:bg-gray-100"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  {editingUser ? "Actualizar" : "Crear"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};