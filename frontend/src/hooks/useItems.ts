/**
 * EXAMPLE HOOK - Demonstrates React Query patterns.
 * DELETE this file and create your own domain hooks.
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { itemsApi, type ItemsQueryParams } from '../api/items';
import type { ItemCreateRequest, ItemUpdateRequest } from '../types';

export const useItems = (params: ItemsQueryParams = {}) => {
  return useQuery({
    queryKey: ['items', params],
    queryFn: () => itemsApi.getItems(params),
  });
};

export const useItem = (id: string) => {
  return useQuery({
    queryKey: ['items', id],
    queryFn: () => itemsApi.getItem(id),
    enabled: !!id,
  });
};

export const useCreateItem = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ItemCreateRequest) => itemsApi.createItem(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
    },
  });
};

export const useUpdateItem = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: ItemUpdateRequest }) =>
      itemsApi.updateItem(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
    },
  });
};

export const useDeleteItem = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => itemsApi.deleteItem(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
    },
  });
};

export const useTags = () => {
  return useQuery({
    queryKey: ['tags'],
    queryFn: () => itemsApi.getTags(),
  });
};