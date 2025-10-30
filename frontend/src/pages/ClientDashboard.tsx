import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Calendar, MapPin, Star, Clock, CreditCard, Search, Plus } from 'lucide-react';
import { useAuth } from '../hooks/useAuthHook';
import Button from '../components/Button';

export default function ClientDashboard() {
  const { user } = useAuth();
  const [recentBookings] = useState([
    {
      id: 1,
      provider: 'John Mwangi',
      service: 'Plumbing',
      date: '2024-12-20',
      time: '10:00 AM',
      status: 'confirmed',
      amount: 2500,
      location: 'Nairobi'
    },
    {
      id: 2,
      provider: 'Sarah Njeri',
      service: 'House Cleaning',
      date: '2024-12-18',
      time: '2:00 PM',
      status: 'completed',
      amount: 3000,
      location: 'Kiambu'
    }
  ]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Welcome back, {user?.name}!</h1>
              <p className="text-gray-600">Manage your bookings and find new services</p>
            </div>
            <Link to="/providers">
              <Button className="inline-flex items-center">
                <Plus size={16} className="mr-2" />
                Book New Service
              </Button>
            </Link>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <Calendar className="text-blue-600" size={24} />
                  </div>
                  <div className="ml-4">
                    <p className="text-2xl font-bold text-gray-900">5</p>
                    <p className="text-sm text-gray-600">Total Bookings</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                    <Star className="text-green-600" size={24} />
                  </div>
                  <div className="ml-4">
                    <p className="text-2xl font-bold text-gray-900">4.8</p>
                    <p className="text-sm text-gray-600">Avg Rating Given</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                    <CreditCard className="text-purple-600" size={24} />
                  </div>
                  <div className="ml-4">
                    <p className="text-2xl font-bold text-gray-900">KSh 12,500</p>
                    <p className="text-sm text-gray-600">Total Spent</p>
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
                {recentBookings.map((booking) => (
                  <div key={booking.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-2">
                          <h3 className="font-semibold text-gray-900">{booking.service}</h3>
                          <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                            booking.status === 'confirmed' ? 'bg-blue-100 text-blue-800' :
                            booking.status === 'completed' ? 'bg-green-100 text-green-800' :
                            'bg-gray-100 text-gray-800'
                          }`}>
                            {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                          </span>
                        </div>
                        <p className="text-gray-600 mb-2">Provider: {booking.provider}</p>
                        <div className="flex items-center text-sm text-gray-500 space-x-4">
                          <div className="flex items-center">
                            <Calendar size={14} className="mr-1" />
                            {booking.date} at {booking.time}
                          </div>
                          <div className="flex items-center">
                            <MapPin size={14} className="mr-1" />
                            {booking.location}
                          </div>
                          <div className="flex items-center">
                            <CreditCard size={14} className="mr-1" />
                            KSh {booking.amount}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <Link to="/providers">
                  <Button className="w-full justify-start">
                    <Search size={16} className="mr-2" />
                    Find Services
                  </Button>
                </Link>
                <Link to="/bookings">
                  <Button variant="secondary" className="w-full justify-start">
                    <Calendar size={16} className="mr-2" />
                    My Bookings
                  </Button>
                </Link>
                <Link to="/profile">
                  <Button variant="secondary" className="w-full justify-start">
                    <Clock size={16} className="mr-2" />
                    Update Profile
                  </Button>
                </Link>
              </div>
            </div>

            {/* Favorite Services */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Popular Services</h3>
              <div className="space-y-3">
                <Link to="/providers?category=Cleaning" className="block p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                  <div className="flex items-center">
                    <span className="text-2xl mr-3">🧹</span>
                    <div>
                      <p className="font-medium">House Cleaning</p>
                      <p className="text-sm text-gray-600">120+ providers</p>
                    </div>
                  </div>
                </Link>
                <Link to="/providers?category=Plumbing" className="block p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                  <div className="flex items-center">
                    <span className="text-2xl mr-3">🔧</span>
                    <div>
                      <p className="font-medium">Plumbing</p>
                      <p className="text-sm text-gray-600">85+ providers</p>
                    </div>
                  </div>
                </Link>
                <Link to="/providers?category=Electrical" className="block p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                  <div className="flex items-center">
                    <span className="text-2xl mr-3">⚡</span>
                    <div>
                      <p className="font-medium">Electrical</p>
                      <p className="text-sm text-gray-600">95+ providers</p>
                    </div>
                  </div>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}