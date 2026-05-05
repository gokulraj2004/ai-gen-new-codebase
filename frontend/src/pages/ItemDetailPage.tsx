import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { apiClient } from '../api/client';
import { formatDate } from '../utils/formatDate';

interface Item {
  id: string;
  title: string;
  description: string;
  created_at: string;
  updated_at: string;
  owner_id: string;
}

export const ItemDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const [item, setItem] = useState<Item | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchItem = async () => {
      try {
        const response = await apiClient.get(`/items/${id}`);
        setItem(response.data);
      } catch {
        setError('Failed to load item');
      } finally {
        setLoading(false);
      }
    };
    fetchItem();
  }, [id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-gray-500">Loading item...</div>
      </div>
    );
  }

  if (error || !item) {
    return (
      <div className="text-center py-12">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded inline-block">
          {error || 'Item not found'}
        </div>
        <div className="mt-4">
          <Link to="/items" className="text-primary-600 hover:underline">
            Back to Items
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <Link to="/items" className="text-primary-600 hover:underline mb-4 inline-block">
        &larr; Back to Items
      </Link>
      <div className="bg-white border border-gray-200 rounded-lg p-8">
        <h1 className="text-3xl font-bold mb-4">{item.title}</h1>
        <p className="text-gray-700 mb-6 whitespace-pre-wrap">{item.description}</p>
        <div className="text-sm text-gray-400 space-y-1">
          <p>Created: {formatDate(item.created_at)}</p>
          <p>Updated: {formatDate(item.updated_at)}</p>
        </div>
      </div>
    </div>
  );
};