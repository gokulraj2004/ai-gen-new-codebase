/**
 * EXAMPLE TYPES - Demonstrates TypeScript interface patterns.
 * DELETE this file and create your own domain types.
 */

export interface Tag {
  id: string;
  name: string;
  created_at: string;
}

export interface Item {
  id: string;
  title: string;
  description: string;
  tags: Tag[];
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface ItemCreateRequest {
  title: string;
  description: string;
  tag_names: string[];
}

export interface ItemUpdateRequest {
  title?: string;
  description?: string;
  tag_names?: string[];
}