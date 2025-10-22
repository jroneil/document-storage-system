export interface Document {
  document_id: string;
  file_name: string;
  file_size: number;
  file_type: string;
  upload_date: string;
  last_modified_date: string;
  user_id: string;
  tags: string[];
  description?: string;
  storage_path: string;
  version: number;
  checksum: string;
  acl?: any;
  thumbnail_path?: string;
  expiration_date?: string;
  category?: string;
  division?: string;
  business_unit?: string;
  brand_id?: string;
  document_type: string;
  status?: 'draft' | 'published' | 'archived';
}

export interface Brand {
  brand_id: string;
  name: string;
  required_metadata: Record<string, string>;
}

export interface DynamicMetadata {
  document_id: string;
  available_countries: string[];
  languages: string[];
  brand_colors: string[];
  brand_logo_path: string;
  campaign_name: string;
  product_line: string;
  custom_fields?: Record<string, any>;
}

export interface User {
  user_id: string;
  role: 'user' | 'admin';
  name: string;
}

export interface MetadataFormData {
  document: Document;
  brand?: Brand;
  dynamicMetadata: DynamicMetadata;
  customFields: Record<string, any>;
}
