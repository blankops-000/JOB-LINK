export default function About() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl font-bold mb-6">About JobLink</h1>
          <p className="text-xl max-w-3xl mx-auto">
            Connecting communities through trusted service providers since 2025
          </p>
        </div>
      </div>

      {/* Mission Section */}
      <div className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl font-bold text-gray-900 mb-6">Our Mission</h2>
              <p className="text-lg text-gray-600 mb-6">
                We believe everyone deserves access to quality services. JobLink bridges the gap between 
                skilled service providers and people who need their expertise.
              </p>
              <div className="space-y-4">
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center mr-4">
                    <span className="text-white font-bold">✓</span>
                  </div>
                  <span className="text-gray-700">Verified service providers</span>
                </div>
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center mr-4">
                    <span className="text-white font-bold">✓</span>
                  </div>
                  <span className="text-gray-700">Secure payment processing</span>
                </div>
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center mr-4">
                    <span className="text-white font-bold">✓</span>
                  </div>
                  <span className="text-gray-700">24/7 customer support</span>
                </div>
              </div>
            </div>
            <div className="bg-gradient-to-br from-blue-100 to-purple-100 rounded-2xl p-8">
              <div className="text-center">
                <div className="text-6xl mb-4">🤝</div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Building Trust</h3>
                <p className="text-gray-600">
                  Every service provider is vetted and reviewed to ensure quality and reliability.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">500+</div>
              <div className="text-gray-600">Service Providers</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-green-600 mb-2">2,000+</div>
              <div className="text-gray-600">Happy Customers</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-purple-600 mb-2">15+</div>
              <div className="text-gray-600">Service Categories</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-yellow-600 mb-2">4.8★</div>
              <div className="text-gray-600">Average Rating</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}