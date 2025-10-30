import { Service } from './booking.types';

export interface ProviderProfile {
  id: string;
  user_id: string;
  business_name: string;
  description: string;
  phone_number: string;
  address: string;
  city: string;
  state: string;
  country: string;
  postal_code: string;
  latitude: number;
  longitude: number;
  service_radius: number; // in kilometers
  is_verified: boolean;
  rating: number;
  review_count: number;
  created_at: string;
  updated_at: string;
  services?: Service[];
  user?: {
    id: string;
    first_name: string;
    last_name: string;
    email: string;
  };
}

export interface ProviderService extends Service {
  provider: {
    id: string;
    business_name: string;
    rating: number;
    review_count: number;
  };
}

export interface ProviderSearchParams {
  service_id?: string;
  category_id?: string;
  location?: string;
  radius?: number;
  min_rating?: number;
  sort_by?: 'rating' | 'distance' | 'price';
  sort_order?: 'asc' | 'desc';
  page?: number;
  limit?: number;
}
