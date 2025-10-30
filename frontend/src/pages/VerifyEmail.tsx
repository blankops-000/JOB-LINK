import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Button from '../components/Button';

const VerifyEmail = () => {
  const [message, setMessage] = useState('Verifying your email...');
  const [isSuccess, setIsSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const verifyEmail = async () => {
      try {
        const token = new URLSearchParams(location.search).get('token');
        if (!token) {
          throw new Error('No verification token provided');
        }

        // TODO: Replace with actual API call
        // await api.get(`/auth/verify-email?token=${token}`);
        
        setIsSuccess(true);
        setMessage('Your email has been verified successfully! Redirecting to login...');
        setTimeout(() => navigate('/login'), 3000);
      } catch (error) {
        setIsSuccess(false);
        setMessage('The verification link is invalid or has expired. Please request a new one.');
      } finally {
        setIsLoading(false);
      }
    };

    verifyEmail();
  }, [location, navigate]);

  const handleResend = async () => {
    try {
      setIsLoading(true);
      setMessage('Sending new verification email...');
      // TODO: Replace with actual API call
      // await api.post('/auth/resend-verification', { email: userEmail });
      setMessage('A new verification link has been sent to your email.');
      setIsSuccess(true);
    } catch (error) {
      setMessage('Failed to send verification email. Please try again later.');
      setIsSuccess(false);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
            {isSuccess ? 'Email Verified!' : 'Email Verification'}
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            {isSuccess 
              ? 'Your email has been verified successfully.'
              : 'Please wait while we verify your email address.'
            }
          </p>
        </div>
        
        <div className={`p-4 rounded-md ${
          isLoading 
            ? 'bg-blue-50 border-l-4 border-blue-400' 
            : isSuccess 
              ? 'bg-green-50 border-l-4 border-green-400'
              : 'bg-red-50 border-l-4 border-red-400'
        }`}>
          <div className="flex">
            <div className="flex-shrink-0">
              {isLoading ? (
                <svg className="h-5 w-5 text-blue-400 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : isSuccess ? (
                <svg className="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              )}
            </div>
            <div className="ml-3">
              <p className={`text-sm ${
                isLoading ? 'text-blue-700' : isSuccess ? 'text-green-700' : 'text-red-700'
              }`}>
                {message}
              </p>
            </div>
          </div>
        </div>

        {!isLoading && !isSuccess && (
          <div className="space-y-4">
            <Button
              onClick={handleResend}
              variant="primary"
              size="lg"
              className="w-full justify-center"
              disabled={isLoading}
            >
              {isLoading ? 'Sending...' : 'Resend Verification Email'}
            </Button>
            
            <div className="text-center text-sm">
              <button
                onClick={() => navigate('/login')}
                className="font-medium text-blue-600 hover:text-blue-500"
              >
                Back to login
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default VerifyEmail;
