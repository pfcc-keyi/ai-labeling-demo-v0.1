import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Types
export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  account_id: string;
}

export interface LabelRequest {
  text: string;
  model_name: 'gpt-4' | 'gpt-3.5-turbo';
}

export interface LabelResponse {
  id: number;
  input_text: string;
  model_name: string;
  predicted_label: string | null;
  processing_time: number;
  error_message?: string;
}

export interface FeedbackRequest {
  request_id: number;
  is_supported: boolean;
  corrected_label?: string;
}

export interface StatusResponse {
  is_busy: boolean;
  current_user: string | null;
  processing_time: number;
}

// API functions
export const login = async (data: LoginRequest): Promise<LoginResponse> => {
  const response = await api.post('/login', data);
  return response.data;
};

export const labelText = async (data: LabelRequest): Promise<LabelResponse> => {
  const response = await api.post('/label', data);
  return response.data;
};

export const submitFeedback = async (data: FeedbackRequest): Promise<{ status: string; message: string }> => {
  const response = await api.post('/feedback', data);
  return response.data;
};

export const getStatus = async (): Promise<StatusResponse> => {
  const response = await api.get('/status');
  return response.data;
};

export const getLabels = async (): Promise<{ labels: string[] }> => {
  const response = await api.get('/labels');
  return response.data;
};

export default api; 