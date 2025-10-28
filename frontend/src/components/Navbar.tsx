import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold text-primary-600">
              JobLink
            </Link>
          </div>
          
          <div className="flex items-center space-x-4">
            <Link to="/providers" className="text-gray-700 hover:text-primary-600">
              Providers
            </Link>
            <Link to="/about" className="text-gray-700 hover:text-primary-600">
              About
            </Link>
            <Link to="/contact" className="text-gray-700 hover:text-primary-600">
              Contact
            </Link>
            
            {user && (
              <Link to="/bookings" className="text-gray-700 hover:text-primary-600">
                My Bookings
              </Link>
            )}
            
            {user ? (
              <>
                <Link to="/profile" className="text-gray-700 hover:text-primary-600">
                  Profile
                </Link>
                {user.role === 'admin' && (
                  <Link to="/dashboard" className="text-gray-700 hover:text-primary-600">
                    Dashboard
                  </Link>
                )}
                <button 
                  onClick={logout}
                  className="btn-secondary"
                >
                  Logout
                </button>
              </>
            ) : (
              <div className="flex space-x-2">
                <Link to="/login" className="btn-secondary">
                  Login
                </Link>
                <Link to="/register" className="btn-primary">
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}