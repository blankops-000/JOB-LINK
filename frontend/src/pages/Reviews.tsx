import { useState } from 'react';
import { Filter, Search, ThumbsUp, Calendar, User } from 'lucide-react';
import Button from '../components/Button';
import Rating from '../components/Rating';

const reviewsData = [
  {
    id: 1,
    customerName: 'Mary Wanjiku',
    customerInitial: 'M',
    providerName: 'John Mwangi - Plumber',
    service: 'Kitchen Sink Repair',
    rating: 5,
    date: '2024-12-15',
    review: 'Excellent service! John arrived exactly on time and fixed my kitchen sink perfectly. He was professional, clean, and explained everything he was doing. The price was fair and the work quality is outstanding. Highly recommend!',
    helpful: 12,
    verified: true
  },
  {
    id: 2,
    customerName: 'David Kiprotich',
    customerInitial: 'D',
    providerName: 'Sarah Njeri - Electrician',
    service: 'House Wiring',
    rating: 5,
    date: '2024-12-10',
    review: 'Sarah did an amazing job rewiring my house. She was very knowledgeable and safety-conscious. The work was completed on schedule and within budget. I feel much safer now with the new wiring. Will definitely use her services again.',
    helpful: 8,
    verified: true
  },
  {
    id: 3,
    customerName: 'Grace Akinyi',
    customerInitial: 'G',
    providerName: 'Peter Kamau - Cleaner',
    service: 'Deep House Cleaning',
    rating: 4,
    date: '2024-12-08',
    review: 'Peter and his team did a thorough job cleaning my house. They were punctual and brought all their own supplies. The house looked spotless when they finished. Only minor issue was they took a bit longer than expected, but the quality was worth it.',
    helpful: 15,
    verified: true
  },
  {
    id: 4,
    customerName: 'James Ochieng',
    customerInitial: 'J',
    providerName: 'Lucy Wambui - Gardener',
    service: 'Garden Landscaping',
    rating: 5,
    date: '2024-12-05',
    review: 'Lucy transformed my backyard into a beautiful garden! Her creativity and attention to detail are exceptional. She suggested plants that work well in our climate and created a low-maintenance design. Absolutely love the results!',
    helpful: 20,
    verified: true
  },
  {
    id: 5,
    customerName: 'Anne Muthoni',
    customerInitial: 'A',
    providerName: 'Michael Otieno - Painter',
    service: 'Interior Painting',
    rating: 4,
    date: '2024-12-01',
    review: 'Michael painted my living room and bedroom. The finish is smooth and professional. He was clean and respectful of my furniture. Communication was good throughout the project. Would recommend for interior painting work.',
    helpful: 6,
    verified: true
  },
  {
    id: 6,
    customerName: 'Robert Kipchoge',
    customerInitial: 'R',
    providerName: 'Faith Nyambura - Beauty Therapist',
    service: 'Home Spa Treatment',
    rating: 5,
    date: '2024-11-28',
    review: 'Faith provided an incredible spa experience at my home. She brought professional equipment and created a relaxing atmosphere. The massage was therapeutic and exactly what I needed. Very professional and skilled.',
    helpful: 9,
    verified: true
  },
  {
    id: 7,
    customerName: 'Catherine Wanjiru',
    customerInitial: 'C',
    providerName: 'Daniel Mutua - IT Support',
    service: 'Computer Repair',
    rating: 5,
    date: '2024-11-25',
    review: 'Daniel fixed my laptop quickly and efficiently. He diagnosed the problem immediately and had it running like new. His rates are reasonable and he explains technical issues in simple terms. Great IT support!',
    helpful: 11,
    verified: true
  },
  {
    id: 8,
    customerName: 'Samuel Kiptoo',
    customerInitial: 'S',
    providerName: 'Rose Adhiambo - Catering',
    service: 'Birthday Party Catering',
    rating: 4,
    date: '2024-11-20',
    review: 'Rose catered my daughter\'s birthday party and the food was delicious! Everyone complimented the variety and taste. She was organized and professional. The only small issue was running slightly behind schedule, but the quality made up for it.',
    helpful: 7,
    verified: true
  }
];

export default function Reviews() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRating, setFilterRating] = useState('all');
  const [sortBy, setSortBy] = useState('newest');

  const filteredReviews = reviewsData
    .filter(review => 
      review.providerName.toLowerCase().includes(searchTerm.toLowerCase()) ||
      review.service.toLowerCase().includes(searchTerm.toLowerCase()) ||
      review.review.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .filter(review => filterRating === 'all' || review.rating === parseInt(filterRating))
    .sort((a, b) => {
      if (sortBy === 'newest') return new Date(b.date).getTime() - new Date(a.date).getTime();
      if (sortBy === 'oldest') return new Date(a.date).getTime() - new Date(b.date).getTime();
      if (sortBy === 'highest') return b.rating - a.rating;
      if (sortBy === 'helpful') return b.helpful - a.helpful;
      return 0;
    });

  const averageRating = reviewsData.reduce((sum, review) => sum + review.rating, 0) / reviewsData.length;
  const totalReviews = reviewsData.length;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-4">Customer Reviews</h1>
            <p className="text-xl text-blue-100 mb-8">
              See what our customers say about JobLink service providers
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
              <div className="flex items-center">
                <Rating rating={averageRating} size="lg" />
                <span className="ml-3 text-2xl font-bold">{averageRating.toFixed(1)}</span>
              </div>
              <div className="text-lg">
                Based on <span className="font-bold">{totalReviews}</span> verified reviews
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Filters and Search */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search reviews..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Rating Filter */}
            <select
              value={filterRating}
              onChange={(e) => setFilterRating(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Ratings</option>
              <option value="5">5 Stars</option>
              <option value="4">4 Stars</option>
              <option value="3">3 Stars</option>
              <option value="2">2 Stars</option>
              <option value="1">1 Star</option>
            </select>

            {/* Sort By */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
              <option value="highest">Highest Rating</option>
              <option value="helpful">Most Helpful</option>
            </select>

            {/* Clear Filters */}
            <Button 
              onClick={() => {
                setSearchTerm('');
                setFilterRating('all');
                setSortBy('newest');
              }}
              variant="secondary"
            >
              <Filter size={16} className="mr-2" />
              Clear Filters
            </Button>
          </div>
        </div>

        {/* Reviews List */}
        <div className="space-y-6">
          {filteredReviews.map((review) => (
            <div key={review.id} className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mr-4">
                    <span className="text-white font-bold text-lg">{review.customerInitial}</span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">{review.customerName}</h3>
                    <p className="text-sm text-gray-600">Service: {review.service}</p>
                    <p className="text-sm text-blue-600 font-medium">{review.providerName}</p>
                  </div>
                </div>
                <div className="text-right">
                  <Rating rating={review.rating} />
                  <div className="flex items-center text-sm text-gray-500 mt-1">
                    <Calendar size={14} className="mr-1" />
                    {new Date(review.date).toLocaleDateString()}
                  </div>
                  {review.verified && (
                    <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800 mt-2">
                      ✓ Verified
                    </span>
                  )}
                </div>
              </div>

              <p className="text-gray-700 mb-4 leading-relaxed">{review.review}</p>

              <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                <button className="flex items-center text-gray-500 hover:text-blue-600 transition-colors">
                  <ThumbsUp size={16} className="mr-2" />
                  Helpful ({review.helpful})
                </button>
                <div className="flex items-center text-sm text-gray-500">
                  <User size={14} className="mr-1" />
                  Verified Customer
                </div>
              </div>
            </div>
          ))}
        </div>

        {filteredReviews.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">🔍</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No reviews found</h3>
            <p className="text-gray-600">Try adjusting your search or filter criteria</p>
          </div>
        )}

        {/* Call to Action */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-8 mt-12 text-center text-white">
          <h2 className="text-2xl font-bold mb-4">Ready to Experience Quality Service?</h2>
          <p className="text-blue-100 mb-6">
            Join thousands of satisfied customers who trust JobLink for their service needs
          </p>
          <Button className="bg-white text-blue-600 hover:bg-gray-100">
            Find Service Providers
          </Button>
        </div>
      </div>
    </div>
  );
}