export type UserRole = 'admin' | 'manager' | 'member' | 'viewer';

export interface User {
  user_id: string;
  username: string;
  email: string;
  full_name?: string;
  role: UserRole;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
  last_login?: string;
  profile_picture?: string;
  phone_number?: string;
  department?: string;
  job_title?: string;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
  full_name?: string;
  role?: UserRole;
  phone_number?: string;
  department?: string;
  job_title?: string;
}

export interface UserUpdate {
  email?: string;
  full_name?: string;
  role?: UserRole;
  is_active?: boolean;
  phone_number?: string;
  department?: string;
  job_title?: string;
  profile_picture?: string;
  password?: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface PasswordChange {
  old_password: string;
  new_password: string;
}

export interface UserListResponse {
  users: User[];
  total: number;
  page: number;
  page_size: number;
}
