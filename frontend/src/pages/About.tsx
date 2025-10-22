import React from 'react';

const About = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">About JobLink</h1>
        <div className="bg-white rounded-lg shadow-md p-6">
          <p className="text-gray-600 mb-4">
            JobLink is a platform designed to connect job seekers with employers,
            making the hiring process more efficient and effective.
          </p>
          <p className="text-gray-600">
            Our mission is to bridge the gap between talent and opportunity,
            helping professionals find their dream jobs and companies find the right candidates.
          </p>
        </div>
      </div>
    </div>
  );
};

export default About;