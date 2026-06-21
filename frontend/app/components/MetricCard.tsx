interface MetricCardProps {
  label: string;
  value: string | number;
  color: 'blue' | 'green' | 'red' | 'purple';
}

export default function MetricCard({ label, value, color }: MetricCardProps) {
  const colorClasses = {
    blue: 'bg-blue-900/20 border-blue-800 text-blue-400',
    green: 'bg-green-900/20 border-green-800 text-green-400',
    red: 'bg-red-900/20 border-red-800 text-red-400',
    purple: 'bg-purple-900/20 border-purple-800 text-purple-400'
  };

  return (
    <div className={`${colorClasses[color]} border rounded-lg p-4`}>
      <p className="text-sm text-gray-400">{label}</p>
      <p className="text-3xl font-bold mt-2">{value}</p>
    </div>
  );
}