import Rating from './Rating';
import Button from './Button';

interface Provider {
  id: string;
  name: string;
  service_category: string;
  location: string;
  hourly_rate: number;
  rating: number;
  image_url?: string;
  description: string;
}

interface ProviderCardProps {
  provider: Provider;
  onBook: (providerId: string) => void;
}

export default function ProviderCard({ provider, onBook }: ProviderCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      {provider.image_url && (
        <img 
          src={provider.image_url} 
          alt={provider.name}
          className="w-full h-48 object-cover"
        />
      )}
      <div className="p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-2">{provider.name}</h3>
        <p className="text-blue-600 font-medium mb-1">{provider.service_category}</p>
        <p className="text-gray-600 mb-2">{provider.location}</p>
        <p className="text-gray-700 text-sm mb-4 line-clamp-2">{provider.description}</p>
        
        <div className="flex items-center justify-between mb-4">
          <Rating rating={provider.rating} />
          <span className="text-lg font-bold text-gray-900">
            ${provider.hourly_rate}/hr
          </span>
        </div>
        
        <Button 
          onClick={() => onBook(provider.id)}
          className="w-full"
        >
          Book Now
        </Button>
      </div>
    </div>
  );
}