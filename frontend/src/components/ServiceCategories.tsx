import { Link } from 'react-router-dom';

const categories = [
  { name: 'Cleaning', icon: '🧹', color: 'bg-blue-100 text-blue-600', count: '120+ providers' },
  { name: 'Plumbing', icon: '🔧', color: 'bg-green-100 text-green-600', count: '85+ providers' },
  { name: 'Electrical', icon: '⚡', color: 'bg-yellow-100 text-yellow-600', count: '95+ providers' },
  { name: 'Gardening', icon: '🌱', color: 'bg-emerald-100 text-emerald-600', count: '70+ providers' },
  { name: 'Beauty', icon: '💄', color: 'bg-pink-100 text-pink-600', count: '110+ providers' },
  { name: 'IT Support', icon: '💻', color: 'bg-purple-100 text-purple-600', count: '60+ providers' },
];

export default function ServiceCategories() {
  return (
    <div className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Popular Services</h2>
          <p className="text-xl text-gray-600">Find the perfect service for your needs</p>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
          {categories.map((category) => (
            <Link
              key={category.name}
              to={`/providers?category=${category.name}`}
              className="group bg-white rounded-2xl p-6 shadow-md hover:shadow-xl transition-all transform hover:-translate-y-2"
            >
              <div className={`w-16 h-16 ${category.color} rounded-2xl flex items-center justify-center text-2xl mb-4 mx-auto group-hover:scale-110 transition-transform`}>
                {category.icon}
              </div>
              <h3 className="text-lg font-semibold text-gray-900 text-center mb-2">{category.name}</h3>
              <p className="text-sm text-gray-500 text-center">{category.count}</p>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}