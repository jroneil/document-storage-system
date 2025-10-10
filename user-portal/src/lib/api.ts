import { User, UserCreate, UserUpdate, UserLogin, UserListResponse, PasswordChange } from '@/types/user';
import { Project, ProjectCreate, ProjectUpdate, ProjectListResponse, ProjectStatistics, AddUserToProject, ProjectUser } from '@/types/project';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    const response = await fetch(url, config);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return {} as T;
    }

    return response.json();
  }

  // User API methods
  async createUser(user: UserCreate): Promise<User> {
    return this.request<User>('/users/', {
      method: 'POST',
      body: JSON.stringify(user),
    });
  }

  async listUsers(params?: {
    skip?: number;
    limit?: number;
    role?: string;
    is_active?: boolean;
    search?: string;
  }): Promise<UserListResponse> {
    const queryParams = new URLSearchParams();
    if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
    if (params?.role) queryParams.append('role', params.role);
    if (params?.is_active !== undefined) queryParams.append('is_active', params.is_active.toString());
    if (params?.search) queryParams.append('search', params.search);

    const query = queryParams.toString();
    return this.request<UserListResponse>(`/users/${query ? '?' + query : ''}`);
  }

  async getUser(userId: string): Promise<User> {
    return this.request<User>(`/users/${userId}`);
  }

  async updateUser(userId: string, update: UserUpdate): Promise<User> {
    return this.request<User>(`/users/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(update),
    });
  }

  async deleteUser(userId: string): Promise<void> {
    return this.request<void>(`/users/${userId}`, {
      method: 'DELETE',
    });
  }

  async authenticateUser(credentials: UserLogin): Promise<User> {
    return this.request<User>('/users/authenticate', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  async changePassword(userId: string, passwords: PasswordChange): Promise<User> {
    return this.request<User>(`/users/${userId}/change-password`, {
      method: 'POST',
      body: JSON.stringify(passwords),
    });
  }

  async verifyUser(userId: string): Promise<User> {
    return this.request<User>(`/users/${userId}/verify`, {
      method: 'POST',
    });
  }

  // Project API methods
  async createProject(project: ProjectCreate): Promise<Project> {
    return this.request<Project>('/projects/', {
      method: 'POST',
      body: JSON.stringify(project),
    });
  }

  async listProjects(params?: {
    skip?: number;
    limit?: number;
    owner_id?: string;
    status?: string;
    is_public?: boolean;
    search?: string;
  }): Promise<ProjectListResponse> {
    const queryParams = new URLSearchParams();
    if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
    if (params?.owner_id) queryParams.append('owner_id', params.owner_id);
    if (params?.status) queryParams.append('status', params.status);
    if (params?.is_public !== undefined) queryParams.append('is_public', params.is_public.toString());
    if (params?.search) queryParams.append('search', params.search);

    const query = queryParams.toString();
    return this.request<ProjectListResponse>(`/projects/${query ? '?' + query : ''}`);
  }

  async listUserProjects(userId: string, params?: {
    skip?: number;
    limit?: number;
    status?: string;
  }): Promise<ProjectListResponse> {
    const queryParams = new URLSearchParams();
    if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
    if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
    if (params?.status) queryParams.append('status', params.status);

    const query = queryParams.toString();
    return this.request<ProjectListResponse>(`/projects/user/${userId}${query ? '?' + query : ''}`);
  }

  async getProject(projectId: string): Promise<Project> {
    return this.request<Project>(`/projects/${projectId}`);
  }

  async updateProject(projectId: string, update: ProjectUpdate): Promise<Project> {
    return this.request<Project>(`/projects/${projectId}`, {
      method: 'PUT',
      body: JSON.stringify(update),
    });
  }

  async deleteProject(projectId: string): Promise<void> {
    return this.request<void>(`/projects/${projectId}`, {
      method: 'DELETE',
    });
  }

  async archiveProject(projectId: string): Promise<Project> {
    return this.request<Project>(`/projects/${projectId}/archive`, {
      method: 'POST',
    });
  }

  async restoreProject(projectId: string): Promise<Project> {
    return this.request<Project>(`/projects/${projectId}/restore`, {
      method: 'POST',
    });
  }

  async addUserToProject(projectId: string, data: AddUserToProject): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/projects/${projectId}/users`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async removeUserFromProject(projectId: string, userId: string): Promise<void> {
    return this.request<void>(`/projects/${projectId}/users/${userId}`, {
      method: 'DELETE',
    });
  }

  async updateUserRole(projectId: string, userId: string, role: string): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/projects/${projectId}/users/${userId}/role`, {
      method: 'PUT',
      body: JSON.stringify({ role }),
    });
  }

  async getProjectUsers(projectId: string): Promise<{ users: ProjectUser[] }> {
    return this.request<{ users: ProjectUser[] }>(`/projects/${projectId}/users`);
  }

  async getProjectStatistics(projectId: string): Promise<ProjectStatistics> {
    return this.request<ProjectStatistics>(`/projects/${projectId}/statistics`);
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
