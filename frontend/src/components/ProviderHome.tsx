import { Link } from 'react-router-dom';
import { Calendar, DollarSign, Users, TrendingUp, Plus, Eye } from 'lucide-react';
import Button from './Button';

export default function ProviderHome() {
  return (
    <div>
      {/* Provider Hero Section */}
      <div className="bg-gradient-to-r from-green-600 to-blue-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-5xl font-bold mb-6">Grow Your Business</h1>
            <p className="text-xl text-green-100 mb-8 max-w-2xl mx-auto">
              Manage bookings, track earnings, and connect with more customers on JobLink.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/provider-dashboard">
                <Button className="bg-white text-green-600 hover:bg-gray-100 px-8 py-4">
                  <Calendar size={20} className="mr-2" />
                  View Dashboard
                </Button>
              </Link>
              <Link to="/profile">
                <Button className="border-2 border-white text-white hover:bg-white hover:text-green-600 px-8 py-4">
                  <Eye size={20} className="mr-2" />
                  Update Profile
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Your Business Overview</h2>
          <div className="grid md:grid-cols-4 gap-8">
            <div className="bg-blue-50 rounded-xl p-6 text-center">
              <Calendar className="text-blue-600 mx-auto mb-4" size={32} />
              <div className="text-3xl font-bold text-gray-900 mb-2">0</div>
              <div className="text-gray-600">Pending Bookings</div>
            </div>
            <div className="bg-green-50 rounded-xl p-6 text-center">
              <DollarSign className="text-green-600 mx-auto mb-4" size={32} />
              <div className="text-3xl font-bold text-gray-900 mb-2">KSh 0</div>
              <div className="text-gray-600">This Month</div>
            </div>
            <div className="bg-purple-50 rounded-xl p-6 text-center">
              <Users className="text-purple-600 mx-auto mb-4" size={32} />
              <div className="text-3xl font-bold text-gray-900 mb-2">0</div>
              <div className="text-gray-600">Total Clients</div>
            </div>
            <div className="bg-yellow-50 rounded-xl p-6 text-center">
              <TrendingUp className="text-yellow-600 mx-auto mb-4" size={32} />
              <div className="text-3xl font-bold text-gray-900 mb-2">0.0</div>
              <div className="text-gray-600">Average Rating</div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Quick Actions</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <Link to="/profile" className="group">
              <div className="bg-white group-hover:shadow-lg rounded-xl p-6 text-center transition-shadow">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Plus className="text-blue-600" size={24} />
                </div>
                <h3 className="text-xl font-semibold mb-2">Complete Profile</h3>
                <p className="text-gray-600">Add photos, services, and pricing</p>
              </div>
            </Link>
            <Link to="/provider-dashboard" className="group">
              <div className="bg-white group-hover:shadow-lg rounded-xl p-6 text-center transition-shadow">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Calendar className="text-green-600" size={24} />
                </div>
                <h3 className="text-xl font-semibold mb-2">Manage Bookings</h3>
                <p className="text-gray-600">View and respond to requests</p>
              </div>
            </Link>
            <Link to="/reviews" className="group">
              <div className="bg-white group-hover:shadow-lg rounded-xl p-6 text-center transition-shadow">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <TrendingUp className="text-purple-600" size={24} />
                </div>
                <h3 className="text-xl font-semibold mb-2">View Reviews</h3>
                <p className="text-gray-600">See customer feedback</p>
              </div>
            </Link>
          </div>
        </div>
      </div>

      {/* Earnings Chart */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">📊 Earnings Overview</h2>
          <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-xl p-8">
            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">KSh 0</div>
                <div className="text-gray-600">This Week</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">KSh 0</div>
                <div className="text-gray-600">This Month</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-purple-600">KSh 0</div>
                <div className="text-gray-600">Total Earned</div>
              </div>
            </div>
            <div className="bg-white rounded-lg p-6 h-32 flex items-center justify-center">
              <div className="text-center text-gray-500">
                <TrendingUp size={32} className="mx-auto mb-2" />
                <p>Earnings chart will appear here once you start getting bookings</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Notifications & Messages */}
      <div className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">🔔 Recent Activity</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white rounded-xl p-6">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <Calendar className="mr-2 text-blue-600" size={24} />
                Booking Requests
              </h3>
              <div className="space-y-3">
                <div className="p-3 bg-blue-50 rounded-lg">
                  <p className="text-sm text-gray-600">No new booking requests</p>
                  <p className="text-xs text-gray-500">Complete your profile to start receiving bookings</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-xl p-6">
              <h3 className="text-xl font-semibold mb-4 flex items-center">
                <Users className="mr-2 text-green-600" size={24} />
                Customer Messages
              </h3>
              <div className="space-y-3">
                <div className="p-3 bg-green-50 rounded-lg">
                  <p className="text-sm text-gray-600">No new messages</p>
                  <p className="text-xs text-gray-500">Messages from customers will appear here</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">📈 Performance Metrics</h2>
          <div className="grid md:grid-cols-4 gap-6">
            <div className="bg-blue-50 rounded-xl p-6 text-center">
              <div className="text-2xl font-bold text-blue-600 mb-2">0%</div>
              <div className="text-gray-600 text-sm">Response Rate</div>
              <div className="text-xs text-gray-500 mt-1">Target: 90%+</div>
            </div>
            <div className="bg-green-50 rounded-xl p-6 text-center">
              <div className="text-2xl font-bold text-green-600 mb-2">0%</div>
              <div className="text-gray-600 text-sm">Completion Rate</div>
              <div className="text-xs text-gray-500 mt-1">Target: 95%+</div>
            </div>
            <div className="bg-purple-50 rounded-xl p-6 text-center">
              <div className="text-2xl font-bold text-purple-600 mb-2">0 min</div>
              <div className="text-gray-600 text-sm">Avg Response Time</div>
              <div className="text-xs text-gray-500 mt-1">Target: &lt;2hrs</div>
            </div>
            <div className="bg-yellow-50 rounded-xl p-6 text-center">
              <div className="text-2xl font-bold text-yellow-600 mb-2">0%</div>
              <div className="text-gray-600 text-sm">Profile Complete</div>
              <div className="text-xs text-gray-500 mt-1">Target: 100%</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tips for Success */}
      <div className="py-16 bg-gradient-to-r from-blue-600 to-green-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">💡 Pro Tips</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white/10 backdrop-blur rounded-xl p-6">
              <h3 className="text-xl font-semibold mb-4">📸 Complete Profile</h3>
              <p className="text-blue-100 mb-4">
                Add photos, detailed descriptions, and competitive pricing to get 3x more bookings.
              </p>
              <Link to="/profile" className="text-white hover:text-blue-200 font-medium">
                Update Profile →
              </Link>
            </div>
            <div className="bg-white/10 backdrop-blur rounded-xl p-6">
              <h3 className="text-xl font-semibold mb-4">⚡ Quick Response</h3>
              <p className="text-blue-100 mb-4">
                Respond to booking requests within 2 hours to increase your booking rate.
              </p>
              <Link to="/provider-dashboard" className="text-white hover:text-blue-200 font-medium">
                Check Requests →
              </Link>
            </div>
            <div className="bg-white/10 backdrop-blur rounded-xl p-6">
              <h3 className="text-xl font-semibold mb-4">⭐ Quality Service</h3>
              <p className="text-blue-100 mb-4">
                Maintain high ratings by delivering excellent service and communication.
              </p>
              <Link to="/reviews" className="text-white hover:text-blue-200 font-medium">
                View Reviews →
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}