import React, { useState } from 'react';
import { DocumentMetadata, BrandMetadata } from '@/types/document'; // Assuming you have a document.ts file in types directory
import { apiClient } from '@/lib/apiClient';

interface MetadataFormProps {
  initialDocumentMetadata?: DocumentMetadata;
  initialBrandMetadata?: BrandMetadata;
}

const MetadataForm: React.FC<MetadataFormProps> = ({ initialDocumentMetadata, initialBrandMetadata }) => {
  const [documentMetadata, setDocumentMetadata] = useState<DocumentMetadata>(initialDocumentMetadata || {
    document_id: '',
    document_title: '',
    file_name: '',
    file_size: 0,
    file_type: '',
    upload_date: new Date(),
    last_modified_date: new Date(),
    user_id: '',
    tags: [],
    description: '',
    storage_path: '',
    version: 1,
    checksum: '',
    document_type: '',
    languages: []
  });

  const [brandMetadata, setBrandMetadata] = useState<BrandMetadata>(initialBrandMetadata || {
    document_id: '',
    available_countries: [],
    languages: [],
    brand_colors: [],
    brand_logo_path: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>, metadataType: 'document' | 'brand') => {
    const { name, value } = e.target;
    if (metadataType === 'document') {
      setDocumentMetadata(prev => ({ ...prev, [name]: value }));
    } else {
      setBrandMetadata(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Implement API call using apiClient to create or update metadata
      console.log('Document Metadata:', documentMetadata);
      console.log('Brand Metadata:', brandMetadata);
      // Example:
      // const response = await apiClient.post('/metadata', { documentMetadata, brandMetadata });
      // console.log('Response:', response);
    } catch (error) {
      console.error('Error creating/updating metadata:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="grid grid-cols-1 gap-4">
      {/* Document Metadata Fields */}
      <div>
        <label htmlFor="document_title" className="block text-sm font-medium text-gray-700">Document Title</label>
        <input
          type="text"
          name="document_title"
          id="document_title"
          value={documentMetadata.document_title}
          onChange={(e) => handleChange(e, 'document')}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
      </div>

      {/* Brand Metadata Fields */}
      <div>
        <label htmlFor="brand_logo_path" className="block text-sm font-medium text-gray-700">Brand Logo Path</label>
        <input
          type="text"
          name="brand_logo_path"
          id="brand_logo_path"
          value={brandMetadata.brand_logo_path}
          onChange={(e) => handleChange(e, 'brand')}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        />
      </div>

      <button type="submit" className="inline-flex items-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
        Submit
      </button>
    </form>
  );
};

export default MetadataForm;