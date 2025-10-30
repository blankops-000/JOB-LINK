import { useState } from 'react';
import { useAuth } from '../hooks/useAuthHook';
import { User, Mail, MapPin, Calendar, Star, CreditCard, Edit3, Camera, Heart } from 'lucide-react';
import Button from '../components/Button';
import LocationPicker from '../components/LocationPicker';

export default function ClientProfile() {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    phone: '+254 700 123 456',
    location: 'Nairobi, Kenya',
    preferences: {
      notifications: true,
      smsUpdates: false,
      emailPromotions: true
    }
  });

  const favoriteServices = [
    { name: 'House Cleaning', icon: '🧹', lastBooked: '2024-12-15' },
    { name: 'Plumbing', icon: '🔧', lastBooked: '2024-11-20' },
    { name: 'Gardening', icon: '🌱', lastBooked: '2024-10-05' }
  ];

  const recentBookings = [
    { id: 1, service: 'Kitchen Repair', provider: 'John Mwangi', date: '2024-12-20', status: 'completed', rating: 5 },
    { id: 2, service: 'House Cleaning', provider: 'Mary Njeri', date: '2024-12-18', status: 'completed', rating: 4 },
    { id: 3, service: 'Garden Maintenance', provider: 'Peter Kamau', date: '2024-12-15', status: 'upcoming', rating: null }
  ];

  const handleSave = () => {
    setIsEditing(false);
    // Save logic here
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="flex flex-col md:flex-row items-center gap-8">
            <div className="relative">
              <div className="w-32 h-32 bg-white rounded-full flex items-center justify-center text-gray-400 text-4xl shadow-lg">
                <User size={48} />
              </div>
              <button className="absolute bottom-2 right-2 bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-full shadow-lg transition-colors">
                <Camera size={16} />
              </button>
            </div>
            
            <div className="text-center md:text-left flex-1">
              <h1 className="text-4xl font-bold mb-2">{user?.name || 'Client Name'}</h1>
              <p className="text-blue-100 text-lg mb-4">JobLink Customer since 2024</p>
              <div className="flex flex-wrap gap-4 justify-center md:justify-start">
                <div className="flex items-center gap-2">
                  <Mail size={16} />
                  <span>{user?.email}</span>
                </div>
                <div className="flex items-center gap-2">
                  <MapPin size={16} />
                  <span>{formData.location}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Star size={16} fill="currentColor" />
                  <span>4.8 Average Rating Given</span>
                </div>
              </div>
            </div>
            
            <Button 
              onClick={() => setIsEditing(!isEditing)}
              className="bg-white text-blue-600 hover:bg-gray-100"
            >
              <Edit3 size={16} className="mr-2" />
              {isEditing ? 'Cancel' : 'Edit Profile'}
            </Button>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Personal Information */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Personal Information</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
                  {isEditing ? (
                    <input
                      type="text"
                      value={formData.name}
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  ) : (
                    <p className="text-gray-900 bg-gray-50 px-4 py-3 rounded-lg">{formData.name}</p>
                  )}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                  {isEditing ? (
                    <input
                      type="email"
                      value={formData.email}
                      onChange={(e) => setFormData({...formData, email: e.target.value})}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  ) : (
                    <p className="text-gray-900 bg-gray-50 px-4 py-3 rounded-lg">{formData.email}</p>
                  )}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Phone Number</label>
                  {isEditing ? (
                    <input
                      type="tel"
                      value={formData.phone}
                      onChange={(e) => setFormData({...formData, phone: e.target.value})}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  ) : (
                    <p className="text-gray-900 bg-gray-50 px-4 py-3 rounded-lg">{formData.phone}</p>
                  )}
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
                  {isEditing ? (
                    <LocationPicker 
                      onLocationSelect={(location) => setFormData({...formData, location})}
                      currentLocation={formData.location}
                    />
                  ) : (
                    <p className="text-gray-900 bg-gray-50 px-4 py-3 rounded-lg">{formData.location}</p>
                  )}
                </div>
              </div>
              
              {isEditing && (
                <div className="mt-6 flex gap-4">
                  <Button onClick={handleSave}>Save Changes</Button>
                  <Button variant="secondary" onClick={() => setIsEditing(false)}>Cancel</Button>
                </div>
              )}
            </div>

            {/* Preferences */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Notification Preferences</h2>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium text-gray-900">Email Notifications</h3>
                    <p className="text-sm text-gray-600">Receive booking confirmations and updates</p>
                  </div>
                  <input
                    type="checkbox"
                    checked={formData.preferences.notifications}
                    onChange={(e) => setFormData({
                      ...formData, 
                      preferences: {...formData.preferences, notifications: e.target.checked}
                    })}
                    className="w-4 h-4 text-blue-600"
                  />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium text-gray-900">SMS Updates</h3>
                    <p className="text-sm text-gray-600">Get text messages for urgent updates</p>
                  </div>
                  <input
                    type="checkbox"
                    checked={formData.preferences.smsUpdates}
                    onChange={(e) => setFormData({
                      ...formData, 
                      preferences: {...formData.preferences, smsUpdates: e.target.checked}
                    })}
                    className="w-4 h-4 text-blue-600"
                  />
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-medium text-gray-900">Promotional Emails</h3>
                    <p className="text-sm text-gray-600">Receive offers and service recommendations</p>
                  </div>
                  <input
                    type="checkbox"
                    checked={formData.preferences.emailPromotions}
                    onChange={(e) => setFormData({
                      ...formData, 
                      preferences: {...formData.preferences, emailPromotions: e.target.checked}
                    })}
                    className="w-4 h-4 text-blue-600"
                  />
                </div>
              </div>
            </div>

            {/* Recent Bookings */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Bookings</h2>
              <div className="space-y-4">
                {recentBookings.map((booking) => (
                  <div key={booking.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold text-gray-900">{booking.service}</h3>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        booking.status === 'completed' ? 'bg-green-100 text-green-800' :
                        booking.status === 'upcoming' ? 'bg-blue-100 text-blue-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {booking.status}
                      </span>
                    </div>
                    <p className="text-gray-600 mb-2">Provider: {booking.provider}</p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center text-sm text-gray-500">
                        <Calendar size={14} className="mr-1" />
                        {booking.date}
                      </div>
                      {booking.rating && (
                        <div className="flex items-center">
                          <Star size={14} className="text-yellow-400 mr-1" fill="currentColor" />
                          <span className="text-sm text-gray-600">{booking.rating}/5</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Account Stats */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Account Summary</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Total Bookings</span>
                  <span className="font-bold text-gray-900">12</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Total Spent</span>
                  <span className="font-bold text-gray-900">KSh 25,500</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Member Since</span>
                  <span className="font-bold text-gray-900">Jan 2024</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Favorite Service</span>
                  <span className="font-bold text-gray-900">Cleaning</span>
                </div>
              </div>
            </div>

            {/* Favorite Services */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">
                <Heart size={20} className="inline mr-2 text-red-500" />
                Favorite Services
              </h3>
              <div className="space-y-3">
                {favoriteServices.map((service, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center">
                      <span className="text-2xl mr-3">{service.icon}</span>
                      <div>
                        <p className="font-medium text-gray-900">{service.name}</p>
                        <p className="text-xs text-gray-500">Last: {service.lastBooked}</p>
                      </div>
                    </div>
                    <Button size="sm">Book Again</Button>
                  </div>
                ))}
              </div>
            </div>

            {/* Payment Methods */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">
                <CreditCard size={20} className="inline mr-2" />
                Payment Methods
              </h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-green-600 rounded flex items-center justify-center mr-3">
                      <span className="text-white text-xs font-bold">M</span>
                    </div>
                    <div>
                      <p className="font-medium">M-Pesa</p>
                      <p className="text-xs text-gray-500">+254 700 ***456</p>
                    </div>
                  </div>
                  <span className="text-xs text-green-600 font-medium">Primary</span>
                </div>
                <Button variant="secondary" className="w-full">
                  Add Payment Method
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}