export type ProjectStatus = 'active' | 'archived' | 'deleted';
export type ProjectRole = 'owner' | 'admin' | 'editor' | 'viewer';

export interface Project {
  project_id: string;
  name: string;
  description?: string;
  status: ProjectStatus;
  owner_id?: string;
  created_at: string;
  updated_at: string;
  start_date?: string;
  end_date?: string;
  tags?: string[];
  metadata?: Record<string, any>;
  storage_quota?: number;
  storage_used: number;
  document_count: number;
  is_public: boolean;
}

export interface ProjectCreate {
  name: string;
  description?: string;
  status?: ProjectStatus;
  owner_id?: string;
  start_date?: string;
  end_date?: string;
  tags?: string[];
  metadata?: Record<string, any>;
  storage_quota?: number;
  is_public?: boolean;
}

export interface ProjectUpdate {
  name?: string;
  description?: string;
  status?: ProjectStatus;
  start_date?: string;
  end_date?: string;
  tags?: string[];
  metadata?: Record<string, any>;
  storage_quota?: number;
  is_public?: boolean;
}

export interface ProjectUser {
  user_id: string;
  username: string;
  email: string;
  full_name?: string;
  role: ProjectRole;
  joined_at: string;
  is_active: boolean;
}

export interface AddUserToProject {
  user_id: string;
  role: ProjectRole;
}

export interface ProjectStatistics {
  project_id: string;
  total_documents: number;
  storage_used: number;
  storage_quota?: number;
  total_users: number;
  active_users: number;
  recent_uploads: number;
}

export interface ProjectListResponse {
  projects: Project[];
  total: number;
  page: number;
  page_size: number;
}
