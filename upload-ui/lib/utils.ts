import { FileValidationResult } from '../types/upload';

/**
 * Validates a file against size and type constraints
 */
export function validateFile(file: File): FileValidationResult {
  const maxFileSize = parseInt(process.env.MAX_FILE_SIZE || '10485760'); // 10MB default
  const allowedTypes = (process.env.ALLOWED_FILE_TYPES || '').split(',');

  // Check file size
  if (file.size > maxFileSize) {
    return {
      isValid: false,
      error: `File size exceeds maximum limit of ${maxFileSize / 1024 / 1024}MB`
    };
  }

  // Check file type
  if (!allowedTypes.includes(file.type)) {
    return {
      isValid: false,
      error: 'File type not allowed'
    };
  }

  return { isValid: true };
}

/**
 * Formats file size in human-readable format
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Utility for conditional CSS classes
 */
export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
}
