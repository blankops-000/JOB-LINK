import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Calendar, DollarSign, Star, Users, TrendingUp, Clock, MapPin, Phone } from 'lucide-react';
import { useAuth } from '../hooks/useAuthHook';
import Button from '../components/Button';

export default function ProviderDashboard() {
  const { user } = useAuth();
  const [bookings] = useState([
    {
      id: 1,
      client: 'Mary Wanjiku',
      service: 'Kitchen Repair',
      date: '2024-12-20',
      time: '10:00 AM',
      status: 'confirmed',
      amount: 2500,
      location: 'Nairobi',
      phone: '+254 700 123 456'
    },
    {
      id: 2,
      client: 'David Kiprotich',
      service: 'Bathroom Plumbing',
      date: '2024-12-22',
      time: '2:00 PM',
      status: 'pending',
      amount: 3500,
      location: 'Kiambu',
      phone: '+254 701 234 567'
    }
  ]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Provider Dashboard</h1>
              <p className="text-gray-600">Welcome back, {user?.name}! Manage your services and bookings</p>
            </div>
            <div className="flex space-x-3">
              <Link to="/profile">
                <Button variant="secondary">Update Profile</Button>
              </Link>
              <Button>Add Service</Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <Calendar className="text-blue-600" size={24} />
                  </div>
                  <div className="ml-4">
                    <p className="text-2xl font-bold text-gray-900">12</p>
                    <p className="text-sm text-gray-600">Total Bookings</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                    <DollarSign className="text-green-600" size={24} />
                  </div>
                  <div className="ml-4">
                    <p className="text-2xl font-bold text-gray-900">KSh 45,000</p>
                    <p className="text-sm text-gray-600">Total Earnings</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                    <Star className="text-yellow-600" size={24} />
                  </div>
                  <div className="ml-4">
                    <p className="text-2xl font-bold text-gray-900">4.8</p>
                    <p className="text-sm text-gray-600">Average Rating</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                    <Users className="text-purple-600" size={24} />
                  </div>
                  <div className="ml-4">
                    <p className="text-2xl font-bold text-gray-900">8</p>
                    <p className="text-sm text-gray-600">Happy Clients</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Bookings */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-900">Recent Bookings</h2>
                <Link to="/bookings" className="text-blue-600 hover:text-blue-700 font-medium">
                  View All
                </Link>
              </div>
              
              <div className="space-y-4">
                {bookings.map((booking) => (
                  <div key={booking.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center">
                        <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center mr-3">
                          <span className="text-white font-bold">{booking.client.charAt(0)}</span>
                        </div>
                        <div>
                          <h3 className="font-semibold text-gray-900">{booking.client}</h3>
                          <p className="text-sm text-gray-600">{booking.service}</p>
                        </div>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                        booking.status === 'confirmed' ? 'bg-blue-100 text-blue-800' :
                        booking.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                        booking.status === 'completed' ? 'bg-green-100 text-green-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                      </span>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600">
                      <div className="flex items-center">
                        <Calendar size={14} className="mr-2" />
                        {booking.date}
                      </div>
                      <div className="flex items-center">
                        <Clock size={14} className="mr-2" />
                        {booking.time}
                      </div>
                      <div className="flex items-center">
                        <MapPin size={14} className="mr-2" />
                        {booking.location}
                      </div>
                      <div className="flex items-center">
                        <DollarSign size={14} className="mr-2" />
                        KSh {booking.amount}
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between mt-4 pt-3 border-t border-gray-100">
                      <div className="flex items-center text-sm text-gray-600">
                        <Phone size={14} className="mr-2" />
                        {booking.phone}
                      </div>
                      <div className="flex space-x-2">
                        {booking.status === 'pending' && (
                          <>
                            <Button size="sm" variant="secondary">Decline</Button>
                            <Button size="sm">Accept</Button>
                          </>
                        )}
                        {booking.status === 'confirmed' && (
                          <Button size="sm">Mark Complete</Button>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Performance Chart */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6">Monthly Performance</h2>
              <div className="grid grid-cols-3 gap-6 text-center">
                <div className="p-4 bg-blue-50 rounded-lg">
                  <TrendingUp className="text-blue-600 mx-auto mb-2" size={32} />
                  <p className="text-2xl font-bold text-blue-600">+25%</p>
                  <p className="text-sm text-gray-600">Bookings Growth</p>
                </div>
                <div className="p-4 bg-green-50 rounded-lg">
                  <DollarSign className="text-green-600 mx-auto mb-2" size={32} />
                  <p className="text-2xl font-bold text-green-600">+18%</p>
                  <p className="text-sm text-gray-600">Revenue Growth</p>
                </div>
                <div className="p-4 bg-yellow-50 rounded-lg">
                  <Star className="text-yellow-600 mx-auto mb-2" size={32} />
                  <p className="text-2xl font-bold text-yellow-600">4.8</p>
                  <p className="text-sm text-gray-600">Rating This Month</p>
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Profile Completion */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Profile Completion</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Basic Info</span>
                  <span className="text-sm font-medium text-green-600">✓ Complete</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Services</span>
                  <span className="text-sm font-medium text-green-600">✓ Complete</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Portfolio</span>
                  <span className="text-sm font-medium text-yellow-600">⚠ Incomplete</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-4">
                  <div className="bg-blue-600 h-2 rounded-full" style={{width: '75%'}}></div>
                </div>
                <p className="text-sm text-gray-600">75% Complete</p>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <Button className="w-full justify-start">
                  <Calendar size={16} className="mr-2" />
                  View Schedule
                </Button>
                <Button variant="secondary" className="w-full justify-start">
                  <Users size={16} className="mr-2" />
                  Manage Services
                </Button>
                <Button variant="secondary" className="w-full justify-start">
                  <Star size={16} className="mr-2" />
                  View Reviews
                </Button>
              </div>
            </div>

            {/* Tips */}
            <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl p-6 text-white">
              <h3 className="text-lg font-bold mb-3">💡 Pro Tip</h3>
              <p className="text-sm text-blue-100 mb-4">
                Complete your portfolio to get 40% more bookings! Add photos of your work and detailed service descriptions.
              </p>
              <Button className="bg-white text-blue-600 hover:bg-gray-100 text-sm">
                Complete Profile
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}