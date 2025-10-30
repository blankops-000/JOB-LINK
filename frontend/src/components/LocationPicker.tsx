import { useState } from 'react';
import { MapPin, Navigation } from 'lucide-react';
import { useGeolocation } from '../hooks/useGeolocation';
import Button from './Button';

interface LocationPickerProps {
  onLocationSelect: (location: string, lat?: number, lng?: number) => void;
  currentLocation?: string;
}

export default function LocationPicker({ onLocationSelect, currentLocation }: LocationPickerProps) {
  const [manualLocation, setManualLocation] = useState(currentLocation || '');
  const { latitude, longitude, error, loading, getCurrentLocation } = useGeolocation();

  const handleUseCurrentLocation = () => {
    getCurrentLocation();
  };

  const handleLocationConfirm = () => {
    if (latitude && longitude) {
      // Reverse geocoding would go here - for now use coordinates
      const locationString = `${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
      onLocationSelect(locationString, latitude, longitude);
    }
  };

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Location
        </label>
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <MapPin className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
            <input
              type="text"
              value={manualLocation}
              onChange={(e) => setManualLocation(e.target.value)}
              placeholder="Enter your location"
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <Button
            onClick={handleUseCurrentLocation}
            disabled={loading}
            className="px-3"
          >
            <Navigation size={16} />
          </Button>
        </div>
      </div>

      {loading && (
        <p className="text-sm text-blue-600">Getting your location...</p>
      )}

      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}

      {latitude && longitude && (
        <div className="bg-green-50 p-3 rounded-lg">
          <p className="text-sm text-green-700">
            Location found: {latitude.toFixed(4)}, {longitude.toFixed(4)}
          </p>
          <Button onClick={handleLocationConfirm} className="mt-2">
            Use This Location
          </Button>
        </div>
      )}

      {manualLocation && (
        <Button 
          onClick={() => onLocationSelect(manualLocation)}
          className="w-full"
        >
          Use Manual Location
        </Button>
      )}
    </div>
  );
}