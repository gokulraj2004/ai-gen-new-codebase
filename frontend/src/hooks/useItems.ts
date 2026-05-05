import { useQuery } from '@tanstack/react-query';
import apiClient from '../api/client';
import type { Item, PaginatedResponse } from '../types';

export type { Item };

export function useItems(page = 1, pageSize = 20) {
  return useQuery<PaginatedResponse<Item>>({
    queryKey: ['items', page, pageSize],
    queryFn: async () => {
      const response = await apiClient.get<PaginatedResponse<Item>>('/items', {
        params: { page, page_size: pageSize },
      });
      return response.data;
    },
  });
}

export function useItem(id: string) {
  return useQuery<Item>({
    queryKey: ['item', id],
    queryFn: async () => {
      const response = await apiClient.get<Item>(`/items/${id}`);
      return response.data;
    },
    enabled: !!id,
  });
}