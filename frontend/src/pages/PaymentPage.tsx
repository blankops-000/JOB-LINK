import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { CreditCard, Shield, CheckCircle, Clock, ArrowLeft, Smartphone } from 'lucide-react';
import api from '../services/authService';
import Button from '../components/Button';

export default function PaymentPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const { booking } = location.state || {
    provider_name: 'John Kamau - Plumber',
    service_date: new Date().toISOString(),
    duration_hours: 2,
    total_amount: 3000
  };
  
  const [phoneNumber, setPhoneNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('mpesa');

  const handlePayment = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await api.post('/payments/initiate', {
        booking_id: booking.id,
        phone_number: phoneNumber,
        payment_method: paymentMethod
      });

      navigate('/payment-status', { 
        state: { 
          paymentId: response.data.payment_id,
          checkoutRequestId: response.data.checkout_request_id 
        } 
      });
    } catch (err: any) {
      setError(err.response?.data?.message || 'Payment initiation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <button 
            onClick={() => navigate(-1)}
            className="flex items-center text-blue-600 hover:text-blue-700 mb-4"
          >
            <ArrowLeft size={20} className="mr-2" />
            Back to Booking
          </button>
          <h1 className="text-3xl font-bold text-gray-900">Complete Your Payment</h1>
          <p className="text-gray-600 mt-2">Secure payment processing for your service booking</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Payment Form */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center mb-6">
                <CreditCard className="text-blue-600 mr-3" size={24} />
                <h2 className="text-xl font-bold text-gray-900">Payment Method</h2>
              </div>

              {/* Payment Method Selection */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div 
                  onClick={() => setPaymentMethod('mpesa')}
                  className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                    paymentMethod === 'mpesa' 
                      ? 'border-green-500 bg-green-50' 
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center">
                    <div className="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center mr-3">
                      <Smartphone className="text-white" size={20} />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">M-Pesa</h3>
                      <p className="text-sm text-gray-600">Pay with mobile money</p>
                    </div>
                  </div>
                </div>

                <div 
                  onClick={() => setPaymentMethod('card')}
                  className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                    paymentMethod === 'card' 
                      ? 'border-blue-500 bg-blue-50' 
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="flex items-center">
                    <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center mr-3">
                      <CreditCard className="text-white" size={20} />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900">Credit Card</h3>
                      <p className="text-sm text-gray-600">Visa, Mastercard</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Payment Form */}
              <form onSubmit={handlePayment} className="space-y-6">
                {error && (
                  <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
                    {error}
                  </div>
                )}

                {paymentMethod === 'mpesa' ? (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      M-Pesa Phone Number
                    </label>
                    <input
                      type="tel"
                      value={phoneNumber}
                      onChange={(e) => setPhoneNumber(e.target.value)}
                      placeholder="254700000000"
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      required
                    />
                    <div className="mt-3 p-4 bg-green-50 rounded-lg">
                      <h4 className="font-medium text-green-800 mb-2">How it works:</h4>
                      <ul className="text-sm text-green-700 space-y-1">
                        <li>• Enter your M-Pesa registered phone number</li>
                        <li>• You'll receive an STK push notification</li>
                        <li>• Enter your M-Pesa PIN to complete payment</li>
                        <li>• Payment confirmation will be sent via SMS</li>
                      </ul>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Card Number
                      </label>
                      <input
                        type="text"
                        placeholder="1234 5678 9012 3456"
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Expiry Date
                        </label>
                        <input
                          type="text"
                          placeholder="MM/YY"
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          CVV
                        </label>
                        <input
                          type="text"
                          placeholder="123"
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                      </div>
                    </div>
                  </div>
                )}

                <Button 
                  type="submit" 
                  disabled={loading}
                  className="w-full py-4 text-lg"
                >
                  {loading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Processing Payment...
                    </div>
                  ) : (
                    `Pay KES ${booking.total_amount?.toLocaleString() || '3,000'}`
                  )}
                </Button>
              </form>
            </div>

            {/* Security Info */}
            <div className="mt-6 bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center mb-4">
                <Shield className="text-green-600 mr-3" size={24} />
                <h3 className="text-lg font-bold text-gray-900">Secure Payment</h3>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div className="flex items-center">
                  <CheckCircle className="text-green-600 mr-2" size={16} />
                  <span className="text-gray-600">256-bit SSL encryption</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="text-green-600 mr-2" size={16} />
                  <span className="text-gray-600">PCI DSS compliant</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="text-green-600 mr-2" size={16} />
                  <span className="text-gray-600">Money-back guarantee</span>
                </div>
              </div>
            </div>
          </div>

          {/* Order Summary */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-6 sticky top-8">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Booking Summary</h3>
              
              <div className="space-y-4">
                <div className="flex items-start">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                    <Clock className="text-blue-600" size={20} />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-semibold text-gray-900">{booking.provider_name}</h4>
                    <p className="text-sm text-gray-600">
                      {new Date(booking.service_date).toLocaleDateString('en-US', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}
                    </p>
                    <p className="text-sm text-gray-600">{booking.duration_hours} hours</p>
                  </div>
                </div>
              </div>

              <div className="border-t pt-4 mt-6">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600">Service fee</span>
                  <span className="text-gray-900">KES {(booking.total_amount * 0.9)?.toLocaleString() || '2,700'}</span>
                </div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600">Platform fee</span>
                  <span className="text-gray-900">KES {(booking.total_amount * 0.1)?.toLocaleString() || '300'}</span>
                </div>
                <div className="border-t pt-2 mt-2">
                  <div className="flex justify-between items-center">
                    <span className="text-lg font-bold text-gray-900">Total</span>
                    <span className="text-lg font-bold text-blue-600">
                      KES {booking.total_amount?.toLocaleString() || '3,000'}
                    </span>
                  </div>
                </div>
              </div>

              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <p className="text-sm text-blue-800">
                  <strong>Cancellation Policy:</strong> Free cancellation up to 24 hours before the service date.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}