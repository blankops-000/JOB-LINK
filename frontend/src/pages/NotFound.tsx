import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full text-center">
        <div className="flex justify-center">
          <svg 
            className="h-24 w-24 text-gray-400" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor" 
            aria-hidden="true"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={1} 
              d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" 
            />
          </svg>
        </div>
        
        <h1 className="mt-6 text-6xl font-extrabold text-gray-900">404</h1>
        <h2 className="mt-3 text-2xl font-medium text-gray-900">Page not found</h2>
        
        <p className="mt-4 text-gray-600">
          Sorry, we couldn't find the page you're looking for.
        </p>
        
        <div className="mt-8 space-y-4">
          <Button
            onClick={() => navigate('/')}
            variant="primary"
            size="lg"
            className="w-full justify-center"
          >
            Go back home
          </Button>
          
          <button
            onClick={() => navigate(-1)}
            className="text-sm font-medium text-blue-600 hover:text-blue-500"
          >
            Or go back to previous page
          </button>
        </div>
        
        <div className="mt-10 border-t border-gray-200 pt-6">
          <p className="text-sm text-gray-500">
            Need help?{' '}
            <a 
              href="/contact" 
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              Contact support
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
