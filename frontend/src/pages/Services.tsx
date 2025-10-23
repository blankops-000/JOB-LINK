const Services = () => {
  const services = [
    { name: 'Cleaning', description: 'Professional cleaning services' },
    { name: 'Plumbing', description: 'Expert plumbing solutions' },
    { name: 'Tutoring', description: 'Educational support services' },
    { name: 'Cooking', description: 'Personal chef services' }
  ]

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Our Services</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {services.map((service, index) => (
          <div key={index} className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">{service.name}</h3>
            <p className="text-gray-600">{service.description}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Services