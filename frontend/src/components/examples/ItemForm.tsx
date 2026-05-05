/**
 * EXAMPLE COMPONENT - Demonstrates form with validation patterns.
 * DELETE this file and create your own domain components.
 */
import React, { useState } from 'react';
import type { Item, ItemCreateRequest } from '../../types';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';
import { validateRequired } from '../../utils/validators';

interface ItemFormProps {
  item?: Item;
  onSubmit: (data: ItemCreateRequest) => Promise<void>;
  onCancel?: () => void;
}

export const ItemForm: React.FC<ItemFormProps> = ({ item, onSubmit, onCancel }) => {
  const [title, setTitle] = useState(item?.title || '');
  const [description, setDescription] = useState(item?.description || '');
  const [tagInput, setTagInput] = useState(item?.tags.map((t) => t.name).join(', ') || '');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!validateRequired(title)) {
      setError('Title is required');
      return;
    }

    const tagNames = tagInput
      .split(',')
      .map((t) => t.trim())
      .filter((t) => t.length > 0);

    setIsLoading(true);
    try {
      await onSubmit({ title, description, tag_names: tagNames });
    } catch (err: unknown) {
      const axiosError = err as { response?: { data?: { detail?: string } } };
      setError(axiosError.response?.data?.detail || 'Failed to save item.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="rounded-md bg-red-50 p-3 text-sm text-red-700">{error}</div>
      )}
      <Input
        label="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Enter item title"
        required
      />
      <div>
        <label className="block text-sm font-medium text-gray-700">Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter item description"
          rows={4}
          className="input-field mt-1"
        />
      </div>
      <Input
        label="Tags (comma-separated)"
        value={tagInput}
        onChange={(e) => setTagInput(e.target.value)}
        placeholder="tag1, tag2, tag3"
      />
      <div className="flex gap-3">
        <Button type="submit" isLoading={isLoading}>
          {item ? 'Update Item' : 'Create Item'}
        </Button>
        {onCancel && (
          <Button type="button" variant="secondary" onClick={onCancel}>
            Cancel
          </Button>
        )}
      </div>
    </form>
  );
};