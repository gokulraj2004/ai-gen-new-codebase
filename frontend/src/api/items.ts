import apiClient from './client';
import type { Item, PaginatedResponse } from '../types';

export interface ListItemsParams {
  page?: number;
  page_size?: number;
  search?: string;
  tag?: string;
  sort_by?: string;
  sort_order?: string;
}

export const itemsApi = {
  list: async (params?: ListItemsParams): Promise<PaginatedResponse<Item>> => {
    const response = await apiClient.get<PaginatedResponse<Item>>('/items', { params });
    return response.data;
  },

  get: async (id: string): Promise<Item> => {
    const response = await apiClient.get<Item>(`/items/${id}`);
    return response.data;
  },

  create: async (data: { title: string; description?: string; tags?: string[] }): Promise<Item> => {
    const response = await apiClient.post<Item>('/items', data);
    return response.data;
  },

  update: async (id: string, data: { title?: string; description?: string; tags?: string[] }): Promise<Item> => {
    const response = await apiClient.put<Item>(`/items/${id}`, data);
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/items/${id}`);
  },
};