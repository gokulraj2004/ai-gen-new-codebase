import React from 'react';
import { formatDate } from '../utils/formatDate';
import type { Item } from '../types';

interface ItemCardProps {
  item: Item;
}

export const ItemCard: React.FC<ItemCardProps> = ({ item }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{item.title}</h3>
      <p className="text-gray-600 text-sm mb-4 line-clamp-3">{item.description}</p>
      {item.tags && item.tags.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-3">
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
      <p className="text-xs text-gray-400">{formatDate(item.created_at)}</p>
    </div>
  );
};