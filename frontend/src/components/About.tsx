import React from 'react';
import { Link } from 'react-router-dom';

const About: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <nav className="mb-8">
        <div className="flex space-x-4">
          <Link to="/" className="text-blue-600 hover:text-blue-800">Home</Link>
          <Link to="/about" className="text-blue-600 hover:text-blue-800">About</Link>
          <Link to="/jobs" className="text-blue-600 hover:text-blue-800">Jobs</Link>
        </div>
      </nav>
      
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">About JobLink</h1>
        <p className="text-gray-600 mb-4">
          JobLink is a modern job search platform that connects talented professionals 
          with amazing opportunities.
        </p>
        <p className="text-gray-600">
          Our mission is to make job searching simple, efficient, and successful for everyone.
        </p>
      </div>
    </div>
  );
};

export default About;