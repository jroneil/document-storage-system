import { v4 as uuid } from 'uuid';

export interface DocumentMetadata {
  document_id: string;
  document_title: string;
  file_name: string;
  file_size: number;
  file_type: string;
  upload_date: Date;
  last_modified_date: Date;
  user_id: string;
  tags: string[];
  description: string;
  storage_path: string;
  version: number;
  checksum: string;
  acl?: { [key: string]: any };
  thumbnail_path?: string;
  expiration_date?: Date;
  category?: string;
  division?: string;
  business_unit?: string;
  brand_id?: string;
  document_type: string;
  region?: string;
  country?: string;
  languages: string[];
  alternate_part_numbers?: string[];
}

export interface BrandMetadata {
  document_id: string;
  available_countries: string[];
  languages: string[];
  brand_colors: string[];
  brand_logo_path: string;
  campaign_name?: string;
  product_line?: string;
}
