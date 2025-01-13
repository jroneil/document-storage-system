import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { DocumentResult } from "@/types/document";
import React from "react";

interface SearchResultProps {
  results?: DocumentResult[];  // Make results optional
  selectedColumns?: string[];  // Make selectedColumns optional
}

function SearchResults({ 
  results = [],  // Provide default empty array
  selectedColumns = []  // Provide default empty array
}: SearchResultProps) {
  const formatDate = (date: Date) => {
    return new Date(date).toLocaleDateString();
  };

  // Add a guard clause for extra safety
  if (!results) return null;

  return (
    <div className="space-y-4">
      {results.map((doc) => (
        <Card key={doc.document_id} className="p-4">
          <div className="flex justify-between items-start">
            <div>
              <h3 className="font-medium">{doc.file_name}</h3>
              <div className="mt-2 space-y-1 text-sm text-gray-600">
                {selectedColumns.includes("type") && (
                  <p>Type: {doc.document_type}</p>
                )}
                {selectedColumns.includes("date") && (
                  <p>Upload Date: {formatDate(doc.upload_date)}</p>
                )}
                {selectedColumns.includes("division") && doc.division && (
                  <p>Division: {doc.division}</p>
                )}
                {selectedColumns.includes("business_unit") && doc.business_unit && (
                  <p>Business Unit: {doc.business_unit}</p>
                )}
              </div>
              {doc.tags && doc.tags.length > 0 && (
                <div className="mt-2 flex gap-2">
                  {doc.tags.map((tag, index) => (
                    <Badge key={index} variant="secondary">
                      {tag}
                    </Badge>
                  ))}
                </div>
              )}
            </div>
            <Button variant="outline" size="sm">
              View
            </Button>
          </div>
        </Card>
      ))}
    </div>
  );
}

export default SearchResults;