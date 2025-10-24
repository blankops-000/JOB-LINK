import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { User, Mail, Shield, Edit3, Camera, Star, MapPin, Phone } from 'lucide-react';
import Button from '../components/Button';

export default function Profile() {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    phone: '+254 700 123 456',
    location: 'Nairobi, Kenya',
    bio: 'Professional service provider with 5+ years of experience.'
  });

  const handleSave = () => {
    setIsEditing(false);
    // Add save logic here
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="flex flex-col md:flex-row items-center gap-8">
            {/* Profile Picture */}
            <div className="relative">
              <div className="w-32 h-32 bg-white rounded-full flex items-center justify-center text-gray-400 text-4xl shadow-lg">
                <User size={48} />
              </div>
              <button className="absolute bottom-2 right-2 bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-full shadow-lg transition-colors">
                <Camera size={16} />
              </button>
            </div>
            
            {/* User Info */}
            <div className="text-center md:text-left flex-1">
              <h1 className="text-4xl font-bold mb-2">{user?.name || 'John Doe'}</h1>
              <p className="text-blue-100 text-lg mb-4 capitalize">{user?.role || 'Customer'}</p>
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
                  <span>4.8 Rating</span>
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
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-900">Personal Information</h2>
                <Shield className="text-green-500" size={24} />
              </div>
              
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
                    <input
                      type="text"
                      value={formData.location}
                      onChange={(e) => setFormData({...formData, location: e.target.value})}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  ) : (
                    <p className="text-gray-900 bg-gray-50 px-4 py-3 rounded-lg">{formData.location}</p>
                  )}
                </div>
              </div>
              
              <div className="mt-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Bio</label>
                {isEditing ? (
                  <textarea
                    value={formData.bio}
                    onChange={(e) => setFormData({...formData, bio: e.target.value})}
                    rows={4}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                ) : (
                  <p className="text-gray-900 bg-gray-50 px-4 py-3 rounded-lg">{formData.bio}</p>
                )}
              </div>
              
              {isEditing && (
                <div className="mt-6 flex gap-4">
                  <Button onClick={handleSave}>Save Changes</Button>
                  <Button variant="secondary" onClick={() => setIsEditing(false)}>Cancel</Button>
                </div>
              )}
            </div>

            {/* Activity Stats */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Activity Overview</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-3xl font-bold text-blue-600">12</div>
                  <div className="text-sm text-gray-600">Bookings</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-3xl font-bold text-green-600">4.8</div>
                  <div className="text-sm text-gray-600">Rating</div>
                </div>
                <div className="text-center p-4 bg-yellow-50 rounded-lg">
                  <div className="text-3xl font-bold text-yellow-600">8</div>
                  <div className="text-sm text-gray-600">Reviews</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <div className="text-3xl font-bold text-purple-600">2</div>
                  <div className="text-sm text-gray-600">Years</div>
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <Button className="w-full justify-start">
                  <Phone size={16} className="mr-2" />
                  Update Contact
                </Button>
                <Button variant="secondary" className="w-full justify-start">
                  <Shield size={16} className="mr-2" />
                  Privacy Settings
                </Button>
                <Button variant="secondary" className="w-full justify-start">
                  <Star size={16} className="mr-2" />
                  View Reviews
                </Button>
              </div>
            </div>

            {/* Account Status */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Account Status</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Email Verified</span>
                  <span className="px-2 py-1 bg-green-100 text-green-600 text-xs rounded-full">✓ Verified</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Phone Verified</span>
                  <span className="px-2 py-1 bg-green-100 text-green-600 text-xs rounded-full">✓ Verified</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">ID Verified</span>
                  <span className="px-2 py-1 bg-yellow-100 text-yellow-600 text-xs rounded-full">Pending</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}