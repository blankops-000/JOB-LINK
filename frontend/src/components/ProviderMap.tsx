import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

interface Provider {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
  location: string;
}

interface ProviderMapProps {
  providers: Provider[];
  center: [number, number];
}

const AnyMapContainer = MapContainer as React.ComponentType<{
  center: [number, number];
  zoom: number;
  className: string;
  children: React.ReactNode;
}>;

export default function ProviderMap({ providers, center }: ProviderMapProps) {
  return (
    <div className="h-96 w-full rounded-lg overflow-hidden">
      <AnyMapContainer center={center} zoom={13} className="h-full w-full">
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {providers.map((provider) => (
          <Marker key={provider.id} position={[provider.latitude, provider.longitude]}>
            <Popup>
              <div>
                <h3 className="font-semibold">{provider.name}</h3>
                <p className="text-sm text-gray-600">{provider.location}</p>
              </div>
            </Popup>
          </Marker>
        ))}
      </AnyMapContainer>
      <div className="text-xs text-gray-500 mt-1">© OpenStreetMap contributors</div>
    </div>
  );
}