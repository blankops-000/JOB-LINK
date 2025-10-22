import React from 'react';

const Services = () => {
  const services = [
    {
      title: 'Job Matching',
      description: 'AI-powered job matching based on skills and preferences'
    },
    {
      title: 'Resume Builder',
      description: 'Professional resume templates and building tools'
    },
    {
      title: 'Interview Prep',
      description: 'Mock interviews and preparation resources'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Our Services</h1>
        <div className="grid md:grid-cols-3 gap-6">
          {services.map((service, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-3">
                {service.title}
              </h3>
              <p className="text-gray-600">{service.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Services;