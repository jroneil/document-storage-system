'use client';

import { useState } from 'react';
import MetadataEditScreen from '@/components/MetadataEditScreen';
import { Document, Brand, DynamicMetadata, User, MetadataFormData } from '@/types/metadata';

// Mock data for demonstration
const mockDocument: Document = {
  document_id: '123e4567-e89b-12d3-a456-426614174000',
  file_name: 'Product Launch Presentation.pdf',
  file_size: 5242880, // 5MB
  file_type: 'application/pdf',
  upload_date: '2024-01-15T10:30:00Z',
  last_modified_date: '2024-01-20T14:45:00Z',
  user_id: 'user-123',
  tags: ['marketing', 'product', 'launch'],
  description: 'Presentation for the upcoming product launch event',
  storage_path: '/documents/product-launch.pdf',
  version: 2,
  checksum: 'abc123def456',
  acl: { read: ['user-123', 'admin'], write: ['user-123'] },
  thumbnail_path: '/thumbnails/product-launch.jpg',
  expiration_date: '2024-12-31T23:59:59Z',
  category: 'Marketing',
  division: 'Product Development',
  business_unit: 'Consumer Products',
  brand_id: 'brand-456',
  document_type: 'Presentation',
  status: 'draft'
};

const mockBrand: Brand = {
  brand_id: 'brand-456',
  name: 'TechCorp',
  required_metadata: {
    product_name: 'string',
    price: 'number',
    release_date: 'string',
    target_audience: 'string'
  }
};

const mockDynamicMetadata: DynamicMetadata = {
  document_id: '123e4567-e89b-12d3-a456-426614174000',
  available_countries: ['US', 'CA', 'GB', 'AU'],
  languages: ['en', 'es', 'fr'],
  brand_colors: ['#FF6B35', '#004E89', '#1A936F'],
  brand_logo_path: '/brands/techcorp/logo.png',
  campaign_name: 'Q1 2024 Product Launch',
  product_line: 'Consumer Electronics',
  custom_fields: {
    campaign_budget: '50000',
    target_impressions: '1000000',
    social_media_platforms: 'Facebook,Instagram,Twitter'
  }
};

const mockUser: User = {
  user_id: 'user-123',
  role: 'user',
  name: 'John Doe'
};

const mockAdminUser: User = {
  user_id: 'admin-001',
  role: 'admin',
  name: 'Admin User'
};

export default function MetadataEditPage() {
  const [currentUser, setCurrentUser] = useState<User>(mockUser);
  const [showAdminView, setShowAdminView] = useState(false);

  const handleSave = (data: MetadataFormData) => {
    console.log('Saving metadata:', data);
    // In a real application, this would make API calls to the metadata service
    alert('Metadata saved successfully!');
  };

  const handleCancel = () => {
    console.log('Edit cancelled');
    // Navigate back or reset state
  };

  const toggleUserRole = () => {
    setCurrentUser(showAdminView ? mockUser : mockAdminUser);
    setShowAdminView(!showAdminView);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-800">Metadata Editor</h1>
              <p className="text-gray-600">
                Edit document metadata, branding, and dynamic properties
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600">
                Logged in as: <span className="font-medium">{currentUser.name}</span> 
                ({currentUser.role})
              </div>
              <button
                onClick={toggleUserRole}
                className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition-colors text-sm"
              >
                Switch to {showAdminView ? 'User' : 'Admin'} View
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="py-8">
        <MetadataEditScreen
          document={mockDocument}
          brand={mockBrand}
          dynamicMetadata={mockDynamicMetadata}
          currentUser={currentUser}
          onSave={handleSave}
          onCancel={handleCancel}
        />
      </div>

      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-800 mb-2">Demo Information</h3>
          <div className="space-y-2 text-sm text-blue-700">
            <p><strong>Current User:</strong> {currentUser.name} ({currentUser.role})</p>
            <p><strong>Edit Permissions:</strong> {currentUser.role === 'admin' ? 
              'Can edit all documents' : 
              'Can only edit own documents'}</p>
            <p><strong>Document Owner:</strong> {mockDocument.user_id}</p>
            <p className="mt-4">
              <strong>Note:</strong> This is a demo interface. In a real application, 
              the data would be fetched from the metadata service API and changes would 
              be persisted to the database.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
