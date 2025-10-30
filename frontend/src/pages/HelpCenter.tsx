import { useState } from 'react';
import { Search, ChevronDown, ChevronRight, MessageCircle, Phone, Mail } from 'lucide-react';
import Button from '../components/Button';

export default function HelpCenter() {
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedFaq, setExpandedFaq] = useState<number | null>(null);

  const faqs = [
    {
      id: 1,
      category: 'Getting Started',
      question: 'How do I book a service on JobLink?',
      answer: 'To book a service: 1) Browse providers or search for specific services, 2) Select a provider and click "Book Now", 3) Choose your preferred date and time, 4) Provide service details, 5) Confirm and pay securely through M-Pesa or card.'
    },
    {
      id: 2,
      category: 'Payments',
      question: 'What payment methods do you accept?',
      answer: 'We accept M-Pesa mobile money, Visa, Mastercard, and other major credit/debit cards. All payments are processed securely and your card details are never stored.'
    },
    {
      id: 3,
      category: 'Safety',
      question: 'How do you verify service providers?',
      answer: 'All providers undergo ID verification, background checks, and skill assessments. We also verify insurance and licenses where applicable. Look for verification badges on provider profiles.'
    },
    {
      id: 4,
      category: 'Booking Management',
      question: 'Can I cancel or reschedule my booking?',
      answer: 'Yes, you can cancel or reschedule up to 24 hours before your appointment. Go to "My Bookings" in your dashboard to manage your appointments. Cancellation fees may apply based on timing.'
    },
    {
      id: 5,
      category: 'For Providers',
      question: 'How do I become a service provider?',
      answer: 'Click "Join as Provider" and complete the registration process. You\'ll need to provide ID verification, relevant certifications, and pass our background check. Once approved, you can start receiving bookings.'
    },
    {
      id: 6,
      category: 'Pricing',
      question: 'How are service prices determined?',
      answer: 'Providers set their own hourly rates based on their experience and market rates. You can see the exact cost before booking, including any additional fees. No hidden charges.'
    }
  ];

  const categories = [
    { name: 'Getting Started', icon: '🚀', count: 8 },
    { name: 'Payments', icon: '💳', count: 6 },
    { name: 'Safety & Security', icon: '🛡️', count: 5 },
    { name: 'Booking Management', icon: '📅', count: 7 },
    { name: 'For Providers', icon: '👷', count: 9 },
    { name: 'Technical Issues', icon: '🔧', count: 4 }
  ];

  const filteredFaqs = faqs.filter(faq => 
    faq.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
    faq.answer.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl font-bold mb-4">How can we help you?</h1>
          <p className="text-xl text-blue-100 mb-8">
            Find answers to common questions or get in touch with our support team
          </p>
          
          {/* Search */}
          <div className="relative max-w-2xl mx-auto">
            <Search className="absolute left-4 top-4 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search for help..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-4 py-4 text-gray-900 bg-white rounded-lg shadow-lg focus:ring-2 focus:ring-blue-300 focus:outline-none"
            />
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Categories Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-6 sticky top-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4">Browse by Category</h3>
              <div className="space-y-2">
                {categories.map((category) => (
                  <button
                    key={category.name}
                    className="w-full text-left p-3 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <span className="text-2xl mr-3">{category.icon}</span>
                        <span className="font-medium text-gray-900">{category.name}</span>
                      </div>
                      <span className="text-sm text-gray-500">{category.count}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3 space-y-8">
            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white rounded-xl shadow-lg p-6 text-center">
                <MessageCircle className="w-12 h-12 text-blue-600 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Live Chat</h3>
                <p className="text-gray-600 mb-4">Get instant help from our support team</p>
                <Button className="w-full">Start Chat</Button>
              </div>
              
              <div className="bg-white rounded-xl shadow-lg p-6 text-center">
                <Phone className="w-12 h-12 text-green-600 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Call Us</h3>
                <p className="text-gray-600 mb-4">Speak directly with our support team</p>
                <Button variant="secondary" className="w-full">+254 769 496 916</Button>
              </div>
              
              <div className="bg-white rounded-xl shadow-lg p-6 text-center">
                <Mail className="w-12 h-12 text-purple-600 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Email Support</h3>
                <p className="text-gray-600 mb-4">Send us a detailed message</p>
                <Button variant="secondary" className="w-full">Send Email</Button>
              </div>
            </div>

            {/* FAQs */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Frequently Asked Questions</h2>
              
              <div className="space-y-4">
                {filteredFaqs.map((faq) => (
                  <div key={faq.id} className="border border-gray-200 rounded-lg">
                    <button
                      onClick={() => setExpandedFaq(expandedFaq === faq.id ? null : faq.id)}
                      className="w-full text-left p-4 flex items-center justify-between hover:bg-gray-50 transition-colors"
                    >
                      <div>
                        <span className="inline-block px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full mr-3">
                          {faq.category}
                        </span>
                        <span className="font-medium text-gray-900">{faq.question}</span>
                      </div>
                      {expandedFaq === faq.id ? (
                        <ChevronDown className="w-5 h-5 text-gray-500" />
                      ) : (
                        <ChevronRight className="w-5 h-5 text-gray-500" />
                      )}
                    </button>
                    
                    {expandedFaq === faq.id && (
                      <div className="px-4 pb-4">
                        <p className="text-gray-700 leading-relaxed">{faq.answer}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {filteredFaqs.length === 0 && (
                <div className="text-center py-8">
                  <p className="text-gray-500">No FAQs found matching your search.</p>
                </div>
              )}
            </div>

            {/* Contact CTA */}
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-8 text-center text-white">
              <h2 className="text-2xl font-bold mb-4">Still need help?</h2>
              <p className="text-blue-100 mb-6">
                Our support team is available 24/7 to assist you with any questions or concerns.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button className="bg-white text-blue-600 hover:bg-gray-100">
                  Contact Support
                </Button>
                <Button className="border-2 border-white text-white hover:bg-white hover:text-blue-600">
                  Schedule a Call
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}