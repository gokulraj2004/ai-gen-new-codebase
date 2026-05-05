import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useItem } from '../hooks/useItems';
import { formatDate } from '../utils/formatDate';

export const ItemDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const { data: item, isLoading, error } = useItem(id || '');

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-16">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error || !item) {
    return (
      <div className="text-center py-16">
        <p className="text-red-600">Item not found or failed to load.</p>
        <Link to="/items" className="text-primary-600 hover:underline mt-4 inline-block">
          Back to Items
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <Link to="/items" className="text-primary-600 hover:underline mb-4 inline-block">
        &larr; Back to Items
      </Link>
      <div className="bg-white rounded-lg shadow-md p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">{item.title}</h1>
        <p className="text-gray-600 mb-6">{item.description}</p>
        {item.tags && item.tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-6">
            {item.tags.map((tag) => (
              <span
                key={tag.id}
                className="inline-block bg-primary-100 text-primary-700 text-xs px-2 py-0.5 rounded"
              >
                {tag.name}
              </span>
            ))}
          </div>
        )}
        <div className="border-t pt-4 text-sm text-gray-500">
          <p>Created: {formatDate(item.created_at)}</p>
          {item.updated_at && <p>Updated: {formatDate(item.updated_at)}</p>}
        </div>
      </div>
    </div>
  );
};