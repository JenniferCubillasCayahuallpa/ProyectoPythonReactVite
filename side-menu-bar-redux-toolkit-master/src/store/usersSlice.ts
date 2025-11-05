import {
  PayloadAction,
  createAsyncThunk,
  createSlice,
} from "@reduxjs/toolkit";
import { API_ENDPOINTS, apiClient } from "../config/api";

export interface User {
  id: number;
  username: string;
  password: string;
  role: string;
  status: string;
}

interface UserCreate {
  username: string;
  password: string;
  role?: string;
  status?: string;
}

interface UserUpdate {
  username?: string;
  password?: string;
  role?: string;
  status?: string;
}

interface UsersState {
  users: User[];
  loading: boolean;
  error?: string;
}

// Función auxiliar para manejar errores de red
const handleApiError = (error: any): string => {
  if (error.status === 500) {
    return "Error del servidor. Verifique que el backend esté corriendo.";
  } else if (error.status === 404) {
    return "Recurso no encontrado.";
  } else if (error.message) {
    return error.message;
  } else {
    return "Error de conexión. Verifique su conexión a internet y que el servidor esté disponible.";
  }
};

export const fetchUsers = createAsyncThunk("users/fetchAll", async (_, { rejectWithValue }) => {
  try {
    return await apiClient.get<User[]>(API_ENDPOINTS.USERS.BASE);
  } catch (error: any) {
    return rejectWithValue(handleApiError(error));
  }
});

export const fetchUser = createAsyncThunk(
  "users/fetchOne",
  async (id: number, { rejectWithValue }) => {
    try {
      return await apiClient.get<User>(API_ENDPOINTS.USERS.BY_ID(id));
    } catch (error: any) {
      return rejectWithValue(handleApiError(error));
    }
  }
);

export const createUser = createAsyncThunk(
  "users/create",
  async (data: UserCreate, { rejectWithValue }) => {
    try {
      return await apiClient.post<User>(API_ENDPOINTS.USERS.BASE, data);
    } catch (error: any) {
      return rejectWithValue(handleApiError(error));
    }
  }
);

export const updateUser = createAsyncThunk(
  "users/update",
  async ({ id, data }: { id: number; data: UserUpdate }, { rejectWithValue }) => {
    try {
      return await apiClient.put<User>(API_ENDPOINTS.USERS.BY_ID(id), data);
    } catch (error: any) {
      return rejectWithValue(handleApiError(error));
    }
  }
);

export const deleteUser = createAsyncThunk(
  "users/delete",
  async (id: number, { rejectWithValue }) => {
    try {
      // The backend returns {message: string, id: number}, but we only need the id
      const response = await apiClient.delete<{message: string, id: number}>(API_ENDPOINTS.USERS.BY_ID(id));
      return response.id;
    } catch (error: any) {
      return rejectWithValue(handleApiError(error));
    }
  }
);

// Nuevas acciones para restaurar usuarios
export const restoreUser = createAsyncThunk(
  "users/restore",
  async (id: number, { rejectWithValue }) => {
    try {
      // The backend returns {message: string, user: User}, but we only need the user
      const response = await apiClient.post<{message: string, user: User}>(`${API_ENDPOINTS.USERS.BY_ID(id)}/restore`, {});
      return response.user;
    } catch (error: any) {
      return rejectWithValue(handleApiError(error));
    }
  }
);

// Acción para obtener usuarios eliminados
export const fetchDeletedUsers = createAsyncThunk(
  "users/fetchDeleted",
  async (_, { rejectWithValue }) => {
    try {
      return await apiClient.get<User[]>(`${API_ENDPOINTS.USERS.BASE}/deleted`);
    } catch (error: any) {
      return rejectWithValue(handleApiError(error));
    }
  }
);

const initialState: UsersState = {
  users: [],
  loading: false,
};

export const usersSlice = createSlice({
  name: "users",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchUsers.pending, (state) => {
        state.loading = true;
        state.error = undefined;
      })
      .addCase(fetchUsers.fulfilled, (state, action: PayloadAction<User[]>) => {
        state.loading = false;
        state.users = action.payload;
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(createUser.pending, (state) => {
        state.loading = true;
        state.error = undefined;
      })
      .addCase(createUser.fulfilled, (state, action: PayloadAction<User>) => {
        state.loading = false;
        state.users.push(action.payload);
      })
      .addCase(createUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(updateUser.pending, (state) => {
        state.loading = true;
        state.error = undefined;
      })
      .addCase(updateUser.fulfilled, (state, action: PayloadAction<User>) => {
        state.loading = false;
        const index = state.users.findIndex(u => u.id === action.payload.id);
        if (index !== -1) {
          state.users[index] = action.payload;
        }
      })
      .addCase(updateUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(deleteUser.pending, (state) => {
        state.loading = true;
        state.error = undefined;
      })
      .addCase(deleteUser.fulfilled, (state, action: PayloadAction<number>) => {
        state.loading = false;
        // Eliminación lógica: cambiar el estado en lugar de eliminar
        const index = state.users.findIndex(u => u.id === action.payload);
        if (index !== -1) {
          state.users[index].status = 'deleted';
        }
      })
      .addCase(deleteUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(restoreUser.pending, (state) => {
        state.loading = true;
        state.error = undefined;
      })
      .addCase(restoreUser.fulfilled, (state, action: PayloadAction<User>) => {
        state.loading = false;
        // Restaurar usuario: actualizar en la lista o añadir si no existe
        const index = state.users.findIndex(u => u.id === action.payload.id);
        if (index !== -1) {
          state.users[index] = action.payload;
        } else {
          state.users.push(action.payload);
        }
      })
      .addCase(restoreUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      .addCase(fetchDeletedUsers.pending, (state) => {
        state.loading = true;
        state.error = undefined;
      })
      .addCase(fetchDeletedUsers.fulfilled, (state, action: PayloadAction<User[]>) => {
        state.loading = false;
        // Reemplazar la lista con usuarios eliminados
        state.users = action.payload;
      })
      .addCase(fetchDeletedUsers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export default usersSlice.reducer;