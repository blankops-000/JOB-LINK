import { useState, useEffect } from 'react';
import api from '../services/authService';

interface Stats {
  total_users: number;
  total_bookings: number;
  total_revenue: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get('/admin/stats');
        setStats(response.data);
      } catch (error) {
        console.error('Failed to fetch stats:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading dashboard...</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Admin Dashboard</h1>
      
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card text-center">
            <h3 className="text-lg font-medium text-gray-900 mb-2">Total Users</h3>
            <p className="text-3xl font-bold text-primary-600">{stats.total_users}</p>
          </div>
          <div className="card text-center">
            <h3 className="text-lg font-medium text-gray-900 mb-2">Total Bookings</h3>
            <p className="text-3xl font-bold text-primary-600">{stats.total_bookings}</p>
          </div>
          <div className="card text-center">
            <h3 className="text-lg font-medium text-gray-900 mb-2">Total Revenue</h3>
            <p className="text-3xl font-bold text-primary-600">${stats.total_revenue}</p>
          </div>
        </div>
      )}
      
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
        <p className="text-gray-500">Activity feed coming soon...</p>
      </div>
    </div>
  );
}