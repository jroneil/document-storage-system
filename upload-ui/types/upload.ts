export interface UploadResponse {
  message: string;
  data?: {
    id?: string;
    filename?: string;
    size?: number;
    uploadedAt?: string;
  };
}

export interface UploadError {
  error: string;
}

export interface FileValidationResult {
  isValid: boolean;
  error?: string;
}

export interface UploadProgress {
  progress: number;
  status: 'idle' | 'uploading' | 'success' | 'error';
  message?: string;
}
