import { useState } from 'react';
import Modal from './Modal';
import Input from './Input';
import Button from './Button';

interface BookingModalProps {
  isOpen: boolean;
  onClose: () => void;
  provider: {
    id: string;
    name: string;
    hourly_rate: number;
  } | null;
  onSubmit: (bookingData: any) => void;
}

export default function BookingModal({ isOpen, onClose, provider, onSubmit }: BookingModalProps) {
  const [formData, setFormData] = useState({
    service_date: '',
    duration_hours: 1,
    notes: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (provider) {
      onSubmit({
        provider_id: provider.id,
        ...formData
      });
    }
  };

  const totalAmount = provider ? provider.hourly_rate * formData.duration_hours : 0;

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Book Service">
      {provider && (
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <h4 className="font-medium text-gray-900">{provider.name}</h4>
            <p className="text-sm text-gray-600">${provider.hourly_rate}/hour</p>
          </div>

          <Input
            label="Service Date & Time"
            type="datetime-local"
            value={formData.service_date}
            onChange={(e) => setFormData({...formData, service_date: e.target.value})}
            required
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Duration (hours)
            </label>
            <select
              value={formData.duration_hours}
              onChange={(e) => setFormData({...formData, duration_hours: parseInt(e.target.value)})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              {[1,2,3,4,5,6,7,8].map(hour => (
                <option key={hour} value={hour}>{hour} hour{hour > 1 ? 's' : ''}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Additional Notes
            </label>
            <textarea
              value={formData.notes}
              onChange={(e) => setFormData({...formData, notes: e.target.value})}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              placeholder="Any special requirements..."
            />
          </div>

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex justify-between items-center">
              <span className="font-medium">Total Amount:</span>
              <span className="text-xl font-bold text-primary-600">${totalAmount}</span>
            </div>
          </div>

          <div className="flex space-x-3">
            <Button type="button" variant="secondary" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit">
              Confirm Booking
            </Button>
          </div>
        </form>
      )}
    </Modal>
  );
}