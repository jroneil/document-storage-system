import { SearchForm } from "@/components/SearchForm";
import { SearchResults } from "@/components/SearchResults";
import { SaveSearchModal } from "@/components/SaveSearchModal";
import { ColumnSelector } from "@/components/ColumnSelector";
import { UploadDocumentModal } from "@/components/UploadDocumentModal";
import { BulkUploadModal } from "@/components/BulkUploadModal";

export default function SearchPage() {
  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Document Search</h1>
        <div className="flex gap-2">
          <SaveSearchModal />
          <ColumnSelector />
          <UploadDocumentModal />
          <BulkUploadModal />
        </div>
      </div>
      
      <SearchForm />
      <SearchResults />
    </div>
  );
}
