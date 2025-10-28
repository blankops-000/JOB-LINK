import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/authService';
import Rating from '../components/Rating';
import Button from '../components/Button';
import BookingModal from '../components/BookingModal';

interface Provider {
  id: string;
  name: string;
  service_category: string;
  location: string;
  hourly_rate: number;
  rating: number;
  image_url?: string;
  description: string;
  reviews: Array<{
    rating: number;
    comment: string;
    client_name: string;
    created_at: string;
  }>;
}

export default function ProviderProfile() {
  const { id } = useParams();
  const [provider, setProvider] = useState<Provider | null>(null);
  const [loading, setLoading] = useState(true);
  const [showBookingModal, setShowBookingModal] = useState(false);

  useEffect(() => {
    const fetchProvider = async () => {
      try {
        const response = await api.get(`/providers/${id}`);
        setProvider(response.data);
      } catch (error) {
        console.error('Failed to fetch provider:', error);
      } finally {
        setLoading(false);
      }
    };

    if (id) fetchProvider();
  }, [id]);

  const handleBooking = async (bookingData: any) => {
    try {
      await api.post('/bookings', bookingData);
      setShowBookingModal(false);
      alert('Booking created successfully!');
    } catch (error) {
      console.error('Booking failed:', error);
      alert('Booking failed. Please try again.');
    }
  };

  if (loading) return <div className="flex justify-center items-center h-64">Loading...</div>;
  if (!provider) return <div className="text-center py-12">Provider not found</div>;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        {provider.image_url && (
          <img 
            src={provider.image_url} 
            alt={provider.name}
            className="w-full h-64 object-cover"
          />
        )}
        
        <div className="p-8">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{provider.name}</h1>
              <p className="text-xl text-primary-600 font-medium mb-1">{provider.service_category}</p>
              <p className="text-gray-600">{provider.location}</p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold text-gray-900 mb-2">
                ${provider.hourly_rate}/hr
              </div>
              <Rating rating={provider.rating} size="lg" />
            </div>
          </div>

          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-4">About</h2>
            <p className="text-gray-700 leading-relaxed">{provider.description}</p>
          </div>

          <div className="mb-8">
            <Button onClick={() => setShowBookingModal(true)} size="lg">
              Book This Service
            </Button>
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-4">Reviews ({provider.reviews.length})</h2>
            <div className="space-y-4">
              {provider.reviews.map((review, index) => (
                <div key={index} className="border-b border-gray-200 pb-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium text-gray-900">{review.client_name}</span>
                    <Rating rating={review.rating} size="sm" />
                  </div>
                  <p className="text-gray-700">{review.comment}</p>
                  <p className="text-sm text-gray-500 mt-1">
                    {new Date(review.created_at).toLocaleDateString()}
                  </p>
                </div>
              ))}
              {provider.reviews.length === 0 && (
                <p className="text-gray-500">No reviews yet.</p>
              )}
            </div>
          </div>
        </div>
      </div>

      <BookingModal
        isOpen={showBookingModal}
        onClose={() => setShowBookingModal(false)}
        provider={provider}
        onSubmit={handleBooking}
      />
    </div>
  );
}