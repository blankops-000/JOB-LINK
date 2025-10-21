import React from 'react';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <nav className="mb-8">
        <div className="flex space-x-4">
          <Link to="/" className="text-blue-600 hover:text-blue-800">Home</Link>
          <Link to="/about" className="text-blue-600 hover:text-blue-800">About</Link>
          <Link to="/jobs" className="text-blue-600 hover:text-blue-800">Jobs</Link>
        </div>
      </nav>
      
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Welcome to JobLink</h1>
        <p className="text-xl text-gray-600 mb-8">Find your dream job today</p>
        <Link 
          to="/jobs" 
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition duration-200"
        >
          Browse Jobs
        </Link>
      </div>
    </div>
  );
};

export default Home;