

export type SearchCriteria = string | number | boolean | object; // Or any union that fits

export interface DocumentResult {
  document_id: string; // UUID string representation
  document_title:string;
  file_name: string;
  file_size: number;
  file_type: string;
  upload_date: Date;
  last_modified_date: Date;
  user_id: string; // UUID string representation
  tags?: string[];
  description?: string;
  storage_path: string;
  version: number;
  checksum: string;
  acl?: Record<string, SearchCriteria>; // Represents a generic object/dictionary
  thumbnail_path?: string;
  expiration_date?: Date;
  category?: string;
  division?: string;
  business_unit?: string;
  brand_id?: string; // UUID string representation
  document_type: string;
  region?: string;
  country?: string;
  languages: string[];
  alternate_part_numbers: string[];
}
