import React from 'react';
import { Link } from 'react-router-dom';
import { useItems } from '../hooks/useItems';
import { ItemCard } from '../components/ItemCard';

export const ItemsPage: React.FC = () => {
  const { data, isLoading, error } = useItems();

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-16">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-16">
        <p className="text-red-600">Failed to load items. Please try again later.</p>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Items</h1>
      </div>
      {data && data.items.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {data.items.map((item) => (
            <Link key={item.id} to={`/items/${item.id}`}>
              <ItemCard item={item} />
            </Link>
          ))}
        </div>
      ) : (
        <div className="text-center py-16 text-gray-500">
          <p>No items found.</p>
        </div>
      )}
    </div>
  );
};