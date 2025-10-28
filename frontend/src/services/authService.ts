import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  async login(email: string, password: string) {
    const response = await api.post('/api/auth/login', { email, password });
    return response.data;
  },

  async getCurrentUser() {
    const response = await api.get('/api/auth/me');
    return response.data;
  },

  async register(userData: any) {
    const response = await api.post('/api/auth/register', userData);
    return response.data;
  }
};

export default api;