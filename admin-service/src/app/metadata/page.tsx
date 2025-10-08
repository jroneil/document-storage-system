import React from 'react';
import MetadataForm from '@/components/MetadataForm';

const MetadataScreen: React.FC = () => {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-4">Metadata Management</h1>
      <MetadataForm />
    </div>
  );
};

export default MetadataScreen;