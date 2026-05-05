/**
 * EXAMPLE API CALLS - Demonstrates API integration patterns.
 * DELETE this file and create your own domain API calls.
 */
import { apiClient } from './client';
import type { Item, ItemCreateRequest, ItemUpdateRequest, Tag } from '../types';
import type { PaginatedResponse } from '../types/api';

export interface ItemsQueryParams {
  page?: number;
  page_size?: number;
  search?: string;
  tags?: string[];
  sort_by?: 'title_asc' | 'title_desc' | 'created_at_desc';
}

export const itemsApi = {
  getItems: async (params: ItemsQueryParams = {}): Promise<PaginatedResponse<Item>> => {
    const response = await apiClient.get<PaginatedResponse<Item>>('/items', { params });
    return response.data;
  },

  getItem: async (id: string): Promise<Item> => {
    const response = await apiClient.get<Item>(`/items/${id}`);
    return response.data;
  },

  createItem: async (data: ItemCreateRequest): Promise<Item> => {
    const response = await apiClient.post<Item>('/items', data);
    return response.data;
  },

  updateItem: async (id: string, data: ItemUpdateRequest): Promise<Item> => {
    const response = await apiClient.put<Item>(`/items/${id}`, data);
    return response.data;
  },

  deleteItem: async (id: string): Promise<void> => {
    await apiClient.delete(`/items/${id}`);
  },

  getTags: async (): Promise<{ tags: Tag[] }> => {
    const response = await apiClient.get<{ tags: Tag[] }>('/tags');
    return response.data;
  },

  createTag: async (name: string): Promise<Tag> => {
    const response = await apiClient.post<Tag>('/tags', { name });
    return response.data;
  },
};