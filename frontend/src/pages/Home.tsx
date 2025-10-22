import React from 'react';

const Home = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            Welcome to JobLink
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Connecting professionals with opportunities
          </p>
          <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">
            Get Started
          </button>
        </div>
      </div>
    </div>
  );
};

export default Home;