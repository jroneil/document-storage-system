import { apiClient } from './apiClient'

type SearchCriteria = string | number | boolean | object; // Or any union that fits

export interface UserPreferences {
  savedSearches: {
    name: string
    criteria: Record<string, SearchCriteria> // Use a union type for SearchCriteria
  }[]
  displayColumns: string[]
}


export const saveSearch = async (search: {
  name: string
  criteria: Record<string, SearchCriteria>
}) => {
  const response = await apiClient.post('/api/user-preferences/save-search', search)
  return response.data
}

export const saveDisplayColumns = async (columns: string[]) => {
  const response = await apiClient.post('/api/user-preferences/save-columns', { columns })
  return response.data
}

export const getPreferences = async (): Promise<UserPreferences> => {
  const response = await apiClient.get('/api/user-preferences')
  return response.data
}
