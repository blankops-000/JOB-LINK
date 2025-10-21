import React from 'react';
import { Link } from 'react-router-dom';

const Jobs: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <nav className="mb-8">
        <div className="flex space-x-4">
          <Link to="/" className="text-blue-600 hover:text-blue-800">Home</Link>
          <Link to="/about" className="text-blue-600 hover:text-blue-800">About</Link>
          <Link to="/jobs" className="text-blue-600 hover:text-blue-800">Jobs</Link>
        </div>
      </nav>
      
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Available Jobs</h1>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">Frontend Developer</h3>
            <p className="text-gray-600 mb-4">Build amazing user interfaces with React</p>
            <span className="text-blue-600 font-medium">$70,000 - $90,000</span>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">Backend Developer</h3>
            <p className="text-gray-600 mb-4">Create robust server-side applications</p>
            <span className="text-blue-600 font-medium">$75,000 - $95,000</span>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">Full Stack Developer</h3>
            <p className="text-gray-600 mb-4">Work on both frontend and backend</p>
            <span className="text-blue-600 font-medium">$80,000 - $100,000</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Jobs;