import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import api from '../services/authService';
import Input from '../components/Input';
import Button from '../components/Button';

export default function Payment() {
  const location = useLocation();
  const navigate = useNavigate();
  const { booking } = location.state || {};
  
  const [phoneNumber, setPhoneNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handlePayment = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await api.post('/payments/initiate', {
        booking_id: booking.id,
        phone_number: phoneNumber
      });

      // Redirect to payment status page
      navigate('/payment-status', { 
        state: { 
          paymentId: response.data.payment_id,
          checkoutRequestId: response.data.checkout_request_id 
        } 
      });
    } catch (err) {
      setError((err as Error & { response?: { data?: { message?: string } } }).response?.data?.message || 'Payment initiation failed');
    } finally {
      setLoading(false);
    }
  };

  if (!booking) {
    return (
      <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
        <p className="text-red-600">No booking information found.</p>
        <Button onClick={() => navigate('/bookings')}>
          Go to Bookings
        </Button>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Complete Payment</h2>
      
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-semibold mb-2">Booking Summary</h3>
        <p><strong>Service:</strong> {booking.provider_name}</p>
        <p><strong>Date:</strong> {new Date(booking.service_date).toLocaleDateString()}</p>
        <p><strong>Duration:</strong> {booking.duration_hours} hours</p>
        <p className="text-xl font-bold text-primary-600 mt-2">
          Total: ${booking.total_amount}
        </p>
      </div>

      <form onSubmit={handlePayment} className="space-y-4">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded">
            {error}
          </div>
        )}

        <Input
          label="M-Pesa Phone Number"
          type="tel"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          placeholder="254700000000"
          required
        />

        <div className="text-sm text-gray-600">
          <p>• Enter your M-Pesa registered phone number</p>
          <p>• You will receive an STK push notification</p>
          <p>• Enter your M-Pesa PIN to complete payment</p>
        </div>

        <div className="w-full">
          <Button type="submit" disabled={loading}>
            {loading ? 'Initiating Payment...' : 'Pay with M-Pesa'}
          </Button>
        </div>
      </form>
    </div>
  );
}