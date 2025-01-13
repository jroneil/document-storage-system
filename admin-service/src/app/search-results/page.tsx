// app/search-results/page.tsx
import SearchResults from "@/components/SearchResults";
import { DocumentResult } from "@/types/document";


export default async function SearchResultsPage() {
  try {
    // Assuming you're fetching data here
    const results: DocumentResult[] = []; // Replace with your actual data fetching
    const selectedColumns: string[] = []; // Replace with your actual columns

    return (
      <SearchResults 
        results={results} 
        selectedColumns={selectedColumns} 
      />
    );
  } catch (error) {
    console.error('Error loading search results:', error);
    return <div>Error loading search results</div>;
  }
}