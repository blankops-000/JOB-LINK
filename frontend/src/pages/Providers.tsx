import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/authService';
import ProviderCard from '../components/ProviderCard';
import BookingModal from '../components/BookingModal';
import Input from '../components/Input';

interface Provider {
  id: string;
  name: string;
  service_category: string;
  rating: number;
  image_url?: string;
  location: string;
  hourly_rate: number;
  description: string;
}

export default function Providers() {
  const [providers, setProviders] = useState<Provider[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedProvider, setSelectedProvider] = useState<Provider | null>(null);
  const [showBookingModal, setShowBookingModal] = useState(false);
  const navigate = useNavigate();

  const categories = ['Cleaning', 'Plumbing', 'Electrical', 'Gardening', 'Handyman', 'Beauty', 'Tutoring', 'IT Support'];

  useEffect(() => {
    const fetchProviders = async () => {
      try {
        const params = new URLSearchParams();
        if (selectedCategory) params.append('category', selectedCategory);
        if (searchTerm) params.append('location', searchTerm);
        
        const response = await api.get(`/providers?${params}`);
        setProviders(response.data);
      } catch (error) {
        console.error('Failed to fetch providers:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProviders();
  }, [searchTerm, selectedCategory]);

  const handleBook = (providerId: string) => {
    const provider = providers.find(p => p.id === providerId);
    if (provider) {
      setSelectedProvider(provider);
      setShowBookingModal(true);
    }
  };

  const handleBookingSubmit = async (bookingData: any) => {
    try {
      await api.post('/bookings', bookingData);
      setShowBookingModal(false);
      navigate('/bookings');
    } catch (error) {
      console.error('Booking failed:', error);
      alert('Booking failed. Please try again.');
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading providers...</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Service Providers</h1>
      
      {/* Filters */}
      <div className="mb-8 grid grid-cols-1 md:grid-cols-2 gap-4">
        <Input
          label="Search by location"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Enter city or area..."
        />
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Service Category
          </label>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="">All Categories</option>
            {categories.map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {providers.map((provider) => (
          <ProviderCard
            key={provider.id}
            provider={provider}
            onBook={handleBook}
          />
        ))}
      </div>
      
      {providers.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">No providers found matching your criteria.</p>
        </div>
      )}

      <BookingModal
        isOpen={showBookingModal}
        onClose={() => setShowBookingModal(false)}
        provider={selectedProvider}
        onSubmit={handleBookingSubmit}
      />
    </div>
  );
}