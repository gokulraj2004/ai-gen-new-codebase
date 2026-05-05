/**
 * EXAMPLE COMPONENT - Demonstrates list with pagination patterns.
 * DELETE this file and create your own domain components.
 */
import React from 'react';
import type { Item } from '../../types';
import { ItemCard } from './ItemCard';
import { Spinner } from '../ui/Spinner';
import { Pagination } from '../ui/Pagination';

interface ItemListProps {
  items: Item[];
  loading: boolean;
  page: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

export const ItemList: React.FC<ItemListProps> = ({
  items,
  loading,
  page,
  totalPages,
  onPageChange,
}) => {
  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="flex h-64 flex-col items-center justify-center text-gray-500">
        <p className="text-lg font-medium">No items found</p>
        <p className="text-sm">Create your first item to get started.</p>
      </div>
    );
  }

  return (
    <div>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {items.map((item) => (
          <ItemCard key={item.id} item={item} />
        ))}
      </div>
      {totalPages > 1 && (
        <div className="mt-6">
          <Pagination page={page} totalPages={totalPages} onPageChange={onPageChange} />
        </div>
      )}
    </div>
  );
};