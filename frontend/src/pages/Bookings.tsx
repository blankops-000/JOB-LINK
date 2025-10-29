import { useState, useEffect } from 'react';
import api from '../services/authService';
import Button from '../components/Button';

interface Booking {
  id: string;
  provider_name: string;
  service_date: string;
  duration_hours: number;
  total_amount: number;
  status: string;
  created_at: string;
}

export default function Bookings() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBookings = async () => {
      try {
        const response = await api.get('/bookings');
        setBookings(response.data);
      } catch (error) {
        console.error('Failed to fetch bookings:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchBookings();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'confirmed': return 'bg-green-100 text-green-800';
      case 'completed': return 'bg-blue-100 text-blue-800';
      case 'cancelled': return 'bg-red-100 text-red-800';
      default: return 'bg-yellow-100 text-yellow-800';
    }
  };

  if (loading) return <div className="flex justify-center items-center h-64">Loading bookings...</div>;

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">My Bookings</h1>
      
      {bookings.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 mb-4">No bookings found.</p>
          <Button onClick={() => window.location.href = '/providers'}>
            Find Services
          </Button>
        </div>
      ) : (
        <div className="space-y-6">
          {bookings.map((booking) => (
            <div key={booking.id} className="bg-white rounded-lg shadow-md p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900">{booking.provider_name}</h3>
                  <p className="text-gray-600">
                    {new Date(booking.service_date).toLocaleDateString()} at{' '}
                    {new Date(booking.service_date).toLocaleTimeString()}
                  </p>
                  <p className="text-gray-600">{booking.duration_hours} hour(s)</p>
                </div>
                <div className="text-right">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(booking.status)}`}>
                    {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                  </span>
                  <p className="text-xl font-bold text-gray-900 mt-2">${booking.total_amount}</p>
                </div>
              </div>
              
              <div className="flex justify-between items-center text-sm text-gray-500">
                <span>Booked on {new Date(booking.created_at).toLocaleDateString()}</span>
                {booking.status === 'confirmed' && (
                  <Button size="sm" variant="secondary">
                    Contact Provider
                  </Button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}