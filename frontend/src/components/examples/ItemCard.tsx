/**
 * EXAMPLE COMPONENT - Demonstrates card display patterns.
 * DELETE this file and create your own domain components.
 */
import React from 'react';
import { Link } from 'react-router-dom';
import type { Item } from '../../types';
import { formatDate } from '../../utils/formatDate';

interface ItemCardProps {
  item: Item;
}

export const ItemCard: React.FC<ItemCardProps> = ({ item }) => {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm transition-shadow hover:shadow-md">
      <Link to={`/items/${item.id}`}>
        <h3 className="text-lg font-semibold text-gray-900 hover:text-primary-600">
          {item.title}
        </h3>
      </Link>
      <p className="mt-2 text-sm text-gray-600 line-clamp-2">{item.description}</p>
      {item.tags.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-2">
          {item.tags.map((tag) => (
            <span
              key={tag.id}
              className="inline-flex items-center rounded-full bg-primary-50 px-2.5 py-0.5 text-xs font-medium text-primary-700"
            >
              {tag.name}
            </span>
          ))}
        </div>
      )}
      <p className="mt-3 text-xs text-gray-400">{formatDate(item.created_at)}</p>
    </div>
  );
};