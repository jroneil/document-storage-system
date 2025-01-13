import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

// Create configured axios instance
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true
});
type filtertype = string | number | boolean | object; // Or any union that fits
// User Preferences Endpoints
export interface SearchCriteria {
  query: string;
  filters: Record<string, filtertype>;
  sortBy?: string;
  sortOrder?: string;
  name?: string;
}

export const saveSearchCriteria = async (criteria: SearchCriteria) => {
  return apiClient.post('/user-preferences/save-search', criteria);
};

export const updateDisplayPreferences = async (preferences: {
  visibleColumns: string[];
  columnOrder: string[];
  pageSize?: number;
}) => {
  return apiClient.post('/user-preferences/update-display-preferences', preferences);
};

export const getPreferences = async () => {
  return apiClient.get('/user-preferences/get-preferences');
};

// Storage Service Endpoints
export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return apiClient.post('/storage/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

export const deleteFile = async (filePath: string) => {
  return apiClient.delete('/storage/delete', {
    data: { file_path: filePath }
  });
};

// Processing Service Endpoints
export const extractText = async (filePath: string) => {
  return apiClient.post('/processing/extract-text', {
    file_path: filePath
  });
};

export const generateThumbnail = async (imagePath: string, outputPath: string) => {
  return apiClient.post('/processing/generate-thumbnail', {
    image_path: imagePath,
    output_path: outputPath
  });
};

// Notification Service Endpoints
export const sendEmail = async (to: string, subject: string, body: string) => {
  return apiClient.post('/notification/send-email', {
    to,
    subject,
    body
  });
};

// AI Service Endpoints
export const analyzeContent = async (text: string) => {
  return apiClient.post('/ai/analyze-content', {
    text
  });
};

// Metadata Service Endpoints
export const saveMetadata = async (metadata: object) => {
  return apiClient.post('/metadata/save-metadata', metadata);
};

// Ingestion Service Endpoints
export const uploadDocument = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return apiClient.post('/ingestion/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
};

