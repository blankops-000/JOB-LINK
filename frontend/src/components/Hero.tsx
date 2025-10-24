import { Link } from 'react-router-dom';

export default function Hero() {
  return (
    <div className="relative bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-800 overflow-hidden">
      <div className="absolute inset-0 bg-black opacity-20"></div>
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="text-center">
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 animate-fade-in">
            Find Your Perfect
            <span className="block text-yellow-400">Service Provider</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-200 mb-8 max-w-3xl mx-auto">
            Connect with trusted professionals in your area. Book services, read reviews, and get the job done right.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/providers" className="bg-yellow-400 hover:bg-yellow-500 text-gray-900 font-bold py-4 px-8 rounded-full text-lg transition-all transform hover:scale-105">
              Find Services
            </Link>
            <Link to="/register" className="border-2 border-white text-white hover:bg-white hover:text-gray-900 font-bold py-4 px-8 rounded-full text-lg transition-all">
              Join as Provider
            </Link>
          </div>
        </div>
      </div>
      
      {/* Floating elements */}
      <div className="absolute top-20 left-10 w-20 h-20 bg-yellow-400 rounded-full opacity-20 animate-bounce"></div>
      <div className="absolute bottom-20 right-10 w-16 h-16 bg-purple-400 rounded-full opacity-30 animate-pulse"></div>
    </div>
  );
}