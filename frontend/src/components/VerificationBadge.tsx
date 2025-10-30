import { Shield, CheckCircle, Award, FileText } from 'lucide-react';

interface VerificationBadgesProps {
  verifications: {
    idVerified?: boolean;
    backgroundCheck?: boolean;
    insurance?: boolean;
    license?: boolean;
  };
  size?: 'sm' | 'md' | 'lg';
}

export default function VerificationBadges({ verifications, size = 'md' }: VerificationBadgesProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6'
  };

  const badges = [
    {
      key: 'idVerified',
      icon: Shield,
      label: 'ID Verified',
      color: 'text-green-600',
      bgColor: 'bg-green-100'
    },
    {
      key: 'backgroundCheck',
      icon: CheckCircle,
      label: 'Background Checked',
      color: 'text-blue-600',
      bgColor: 'bg-blue-100'
    },
    {
      key: 'insurance',
      icon: Award,
      label: 'Insured',
      color: 'text-purple-600',
      bgColor: 'bg-purple-100'
    },
    {
      key: 'license',
      icon: FileText,
      label: 'Licensed',
      color: 'text-orange-600',
      bgColor: 'bg-orange-100'
    }
  ];

  const verifiedBadges = badges.filter(badge => verifications[badge.key as keyof typeof verifications]);

  if (verifiedBadges.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2">
      {verifiedBadges.map((badge) => {
        const Icon = badge.icon;
        return (
          <div
            key={badge.key}
            className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${badge.bgColor} ${badge.color}`}
            title={badge.label}
          >
            <Icon className={`${sizeClasses[size]} mr-1`} />
            {size !== 'sm' && badge.label}
          </div>
        );
      })}
    </div>
  );
}