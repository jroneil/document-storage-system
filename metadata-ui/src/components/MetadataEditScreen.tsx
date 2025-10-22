'use client';

import { useState } from 'react';
import { Document, Brand, DynamicMetadata, User, MetadataFormData } from '@/types/metadata';

interface MetadataEditScreenProps {
  document: Document;
  brand?: Brand;
  dynamicMetadata: DynamicMetadata;
  currentUser: User;
  onSave: (data: MetadataFormData) => void;
  onCancel: () => void;
}

export default function MetadataEditScreen({
  document,
  brand,
  dynamicMetadata,
  currentUser,
  onSave,
  onCancel
}: MetadataEditScreenProps) {
  const [isEditMode, setIsEditMode] = useState(false);
  const [formData, setFormData] = useState<MetadataFormData>({
    document,
    brand,
    dynamicMetadata,
    customFields: {}
  });

  const canEdit = currentUser.role === 'admin' || 
                  (currentUser.role === 'user' && document.user_id === currentUser.user_id);

  const handleInputChange = (section: keyof MetadataFormData, field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }));
  };

  const handleDynamicMetadataChange = (field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      dynamicMetadata: {
        ...prev.dynamicMetadata,
        [field]: value
      }
    }));
  };

  const handleCustomFieldChange = (field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      customFields: {
        ...prev.customFields,
        [field]: value
      }
    }));
  };

  const addCustomField = () => {
    const newKey = `custom_field_${Object.keys(formData.customFields).length + 1}`;
    handleCustomFieldChange(newKey, '');
  };

  const removeCustomField = (field: string) => {
    const newCustomFields = { ...formData.customFields };
    delete newCustomFields[field];
    setFormData(prev => ({ ...prev, customFields: newCustomFields }));
  };

  const updateCustomFieldKey = (oldKey: string, newKey: string) => {
    if (oldKey === newKey) return;
    
    const newCustomFields = { ...formData.customFields };
    const value = newCustomFields[oldKey];
    delete newCustomFields[oldKey];
    newCustomFields[newKey] = value;
    setFormData(prev => ({ ...prev, customFields: newCustomFields }));
  };

  const handleBrandChange = (field: string, value: any) => {
    if (!formData.brand) return;
    
    setFormData(prev => ({
      ...prev,
      brand: {
        ...prev.brand!,
        [field]: value
      }
    }));
  };

  const handleRequiredMetadataChange = (field: string, value: string) => {
    if (!formData.brand) return;
    
    setFormData(prev => ({
      ...prev,
      brand: {
        ...prev.brand!,
        required_metadata: {
          ...prev.brand!.required_metadata,
          [field]: value
        }
      }
    }));
  };

  const addRequiredMetadataField = () => {
    if (!formData.brand) return;
    
    const newField = `new_field_${Object.keys(formData.brand.required_metadata).length + 1}`;
    handleRequiredMetadataChange(newField, 'string');
  };

  const removeRequiredMetadataField = (field: string) => {
    if (!formData.brand) return;
    
    const newRequiredMetadata = { ...formData.brand.required_metadata };
    delete newRequiredMetadata[field];
    
    setFormData(prev => ({
      ...prev,
      brand: {
        ...prev.brand!,
        required_metadata: newRequiredMetadata
      }
    }));
  };

  const handleSave = () => {
    onSave(formData);
    setIsEditMode(false);
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-8">
      {/* Header Section */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-gray-800">Document Header</h2>
          {canEdit && (
            <button
              onClick={() => setIsEditMode(!isEditMode)}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              {isEditMode ? 'Cancel Edit' : 'Edit Metadata'}
            </button>
          )}
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Document ID</label>
            <input
              type="text"
              value={formData.document.document_id}
              disabled
              className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Document Number</label>
            <input
              type="text"
              value={formData.document.document_id.split('-')[0]}
              disabled
              className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
            <input
              type="text"
              value={formData.document.file_name}
              onChange={(e) => handleInputChange('document', 'file_name', e.target.value)}
              disabled={!isEditMode}
              className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Publication Date</label>
            <input
              type="date"
              value={formData.document.upload_date.split('T')[0]}
              onChange={(e) => handleInputChange('document', 'upload_date', e.target.value)}
              disabled={!isEditMode}
              className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select
              value={formData.document.status || 'draft'}
              onChange={(e) => handleInputChange('document', 'status', e.target.value)}
              disabled={!isEditMode}
              className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
            >
              <option value="draft">Draft</option>
              <option value="published">Published</option>
              <option value="archived">Archived</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">File Size</label>
            <input
              type="text"
              value={formatFileSize(formData.document.file_size)}
              disabled
              className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">File Type</label>
            <input
              type="text"
              value={formData.document.file_type}
              disabled
              className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Last Modified</label>
            <input
              type="text"
              value={new Date(formData.document.last_modified_date).toLocaleDateString()}
              disabled
              className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 text-gray-500"
            />
          </div>
        </div>
      </div>

      {/* Standard Metadata Section - 2 Columns */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Standard Metadata</h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column */}
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea
                value={formData.document.description || ''}
                onChange={(e) => handleInputChange('document', 'description', e.target.value)}
                disabled={!isEditMode}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
              <input
                type="text"
                value={formData.document.category || ''}
                onChange={(e) => handleInputChange('document', 'category', e.target.value)}
                disabled={!isEditMode}
                className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Division</label>
              <input
                type="text"
                value={formData.document.division || ''}
                onChange={(e) => handleInputChange('document', 'division', e.target.value)}
                disabled={!isEditMode}
                className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Tags</label>
              <input
                type="text"
                value={formData.document.tags?.join(', ') || ''}
                onChange={(e) => handleInputChange('document', 'tags', e.target.value.split(',').map(tag => tag.trim()))}
                disabled={!isEditMode}
                placeholder="Enter tags separated by commas"
                className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
          </div>

          {/* Right Column */}
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Business Unit</label>
              <input
                type="text"
                value={formData.document.business_unit || ''}
                onChange={(e) => handleInputChange('document', 'business_unit', e.target.value)}
                disabled={!isEditMode}
                className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Document Type</label>
              <input
                type="text"
                value={formData.document.document_type}
                onChange={(e) => handleInputChange('document', 'document_type', e.target.value)}
                disabled={!isEditMode}
                className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Version</label>
              <input
                type="number"
                value={formData.document.version}
                onChange={(e) => handleInputChange('document', 'version', parseInt(e.target.value))}
                disabled={!isEditMode}
                className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Expiration Date</label>
              <input
                type="date"
                value={formData.document.expiration_date?.split('T')[0] || ''}
                onChange={(e) => handleInputChange('document', 'expiration_date', e.target.value)}
                disabled={!isEditMode}
                className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Branding Section */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Branding</h2>
          {isEditMode && currentUser.role === 'admin' && formData.brand && (
            <div className="flex items-center gap-2 text-sm text-blue-600">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Admin: Brand editing enabled
            </div>
          )}
        </div>
        
        {formData.brand ? (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Brand Name</label>
              <input
                type="text"
                value={formData.brand.name}
                onChange={(e) => handleBrandChange('name', e.target.value)}
                disabled={!isEditMode || currentUser.role !== 'admin'}
                className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
            
            <div>
              <div className="flex justify-between items-center mb-4">
                <label className="block text-sm font-medium text-gray-700">Required Metadata Fields</label>
                {isEditMode && currentUser.role === 'admin' && (
                  <button
                    onClick={addRequiredMetadataField}
                    className="px-3 py-1 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors text-sm flex items-center gap-1"
                  >
                    <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                    Add Field
                  </button>
                )}
              </div>
              
              {Object.keys(formData.brand.required_metadata).length === 0 ? (
                <div className="text-center py-4 text-gray-500 border-2 border-dashed border-gray-300 rounded-md">
                  <p>No required metadata fields defined</p>
                  {isEditMode && currentUser.role === 'admin' && (
                    <p className="text-sm mt-1">Click "Add Field" to define required metadata</p>
                  )}
                </div>
              ) : (
                <div className="space-y-3">
                  {Object.entries(formData.brand.required_metadata).map(([field, type]) => (
                    <div key={field} className="flex gap-2 items-start">
                      <div className="flex-1">
                        <label className="block text-sm font-medium text-gray-700 mb-1">Field Name</label>
                        <input
                          type="text"
                          value={field}
                          onChange={(e) => {
                            const newField = e.target.value;
                            if (newField !== field) {
                              handleRequiredMetadataChange(newField, type);
                              removeRequiredMetadataField(field);
                            }
                          }}
                          disabled={!isEditMode || currentUser.role !== 'admin'}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
                          placeholder="Field name"
                        />
                      </div>
                      <div className="flex-1">
                        <label className="block text-sm font-medium text-gray-700 mb-1">Field Type</label>
                        <select
                          value={type}
                          onChange={(e) => handleRequiredMetadataChange(field, e.target.value)}
                          disabled={!isEditMode || currentUser.role !== 'admin'}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
                        >
                          <option value="string">String</option>
                          <option value="number">Number</option>
                          <option value="boolean">Boolean</option>
                          <option value="date">Date</option>
                          <option value="array">Array</option>
                        </select>
                      </div>
                      {isEditMode && currentUser.role === 'admin' && (
                        <div className="pt-6">
                          <button
                            onClick={() => removeRequiredMetadataField(field)}
                            className="px-3 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors flex items-center gap-1"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                            Remove
                          </button>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <p>No brand associated with this document</p>
            {isEditMode && currentUser.role === 'admin' && (
              <div className="mt-4 space-y-2">
                <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">
                  Associate Existing Brand
                </button>
                <button className="block mx-auto px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors text-sm">
                  Create New Brand
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Dynamic Metadata Section */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Dynamic Metadata</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Campaign Name</label>
              <input
                type="text"
                value={formData.dynamicMetadata.campaign_name}
                onChange={(e) => handleDynamicMetadataChange('campaign_name', e.target.value)}
                disabled={!isEditMode}
                className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Product Line</label>
              <input
                type="text"
                value={formData.dynamicMetadata.product_line}
                onChange={(e) => handleDynamicMetadataChange('product_line', e.target.value)}
                disabled={!isEditMode}
                className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Available Countries</label>
              <input
                type="text"
                value={formData.dynamicMetadata.available_countries.join(', ')}
                onChange={(e) => handleDynamicMetadataChange('available_countries', e.target.value.split(',').map(country => country.trim()))}
                disabled={!isEditMode}
                placeholder="Enter country codes separated by commas"
                className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Languages</label>
              <input
                type="text"
                value={formData.dynamicMetadata.languages.join(', ')}
                onChange={(e) => handleDynamicMetadataChange('languages', e.target.value.split(',').map(lang => lang.trim()))}
                disabled={!isEditMode}
                placeholder="Enter language codes separated by commas"
                className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Brand Colors</label>
              <input
                type="text"
                value={formData.dynamicMetadata.brand_colors.join(', ')}
                onChange={(e) => handleDynamicMetadataChange('brand_colors', e.target.value.split(',').map(color => color.trim()))}
                disabled={!isEditMode}
                placeholder="Enter hex colors separated by commas"
                className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Brand Logo Path</label>
              <input
                type="text"
                value={formData.dynamicMetadata.brand_logo_path}
                onChange={(e) => handleDynamicMetadataChange('brand_logo_path', e.target.value)}
                disabled={!isEditMode}
                className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
              />
            </div>
          </div>
        </div>

        {/* Custom Fields Section */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-800">Custom Fields</h3>
            {isEditMode && (
              <button
                onClick={addCustomField}
                className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors flex items-center gap-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                Add Custom Field
              </button>
            )}
          </div>
          
          {Object.keys(formData.customFields).length === 0 ? (
            <div className="text-center py-8 text-gray-500 border-2 border-dashed border-gray-300 rounded-lg">
              <p>No custom fields defined</p>
              {isEditMode && (
                <p className="text-sm mt-2">Click "Add Custom Field" to create your first custom field</p>
              )}
            </div>
          ) : (
            <div className="space-y-3">
              {Object.entries(formData.customFields).map(([key, value]) => (
                <div key={key} className="flex gap-2 items-start">
                  <div className="flex-1">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Field Name</label>
                    <input
                      type="text"
                      value={key}
                      onChange={(e) => updateCustomFieldKey(key, e.target.value)}
                      disabled={!isEditMode}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
                      placeholder="Enter field name"
                    />
                  </div>
                  <div className="flex-1">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Field Value</label>
                    <input
                      type="text"
                      value={value}
                      onChange={(e) => handleCustomFieldChange(key, e.target.value)}
                      disabled={!isEditMode}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md disabled:bg-gray-50 disabled:text-gray-500"
                      placeholder="Enter field value"
                    />
                  </div>
                  {isEditMode && (
                    <div className="pt-6">
                      <button
                        onClick={() => removeCustomField(key)}
                        className="px-3 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors flex items-center gap-1"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                        Remove
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
          
          {isEditMode && Object.keys(formData.customFields).length > 0 && (
            <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
              <p className="text-sm text-blue-700">
                <strong>Tip:</strong> You can edit field names and values. Field names must be unique.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Action Buttons */}
      {isEditMode && (
        <div className="flex justify-end space-x-4 pt-6">
          <button
            onClick={() => {
              setIsEditMode(false);
              setFormData({ document, brand, dynamicMetadata, customFields: {} });
            }}
            className="px-6 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            Save Changes
          </button>
        </div>
      )}
    </div>
  );
}
