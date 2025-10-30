import { User } from './user.types';

export interface Service {
  id: string;
  name: string;
  description: string;
  price: number;
  duration: number; // in minutes
  category_id: string;
  provider_id: string;
  created_at: string;
  updated_at: string;
}

export interface Booking {
  id: string;
  user_id: string;
  provider_id: string;
  service_id: string;
  date: string;
  start_time: string;
  end_time: string;
  status: 'pending' | 'confirmed' | 'completed' | 'cancelled';
  notes?: string;
  created_at: string;
  updated_at: string;
  user?: User;
  provider?: User;
  service?: Service;
}

export interface CreateBookingData {
  provider_id: string;
  service_id: string;
  date: string;
  start_time: string;
  notes?: string;
}

export interface UpdateBookingData {
  status?: 'confirmed' | 'completed' | 'cancelled';
  notes?: string;
}
