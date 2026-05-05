export interface User {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
}

export interface Tag {
  id: string;
  name: string;
}

export interface Item {
  id: string;
  title: string;
  description: string | null;
  user_id: string;
  tags: Tag[];
  created_at: string;
  updated_at: string;
}

export interface ItemCreateRequest {
  title: string;
  description: string;
  tags: string[];
}

export interface ItemUpdateRequest {
  title?: string;
  description?: string;
  tags?: string[];
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}