'use client'

import SaveSearchModal from './SaveSearchModal'

import { DocumentResult } from '@/types/document'

interface ResultsDisplayProps {
  results: DocumentResult[]
  onSelect: (id: string) => void
}

export default function ResultsDisplay({ results, onSelect }: ResultsDisplayProps) {

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Search Results</h2>
        <SaveSearchModal />
      </div>

      <div className="space-y-2">
        {results.map(result => (
          <div 
            key={result.id} 
            className="p-4 border rounded-lg hover:bg-gray-50 cursor-pointer"
            onClick={() => onSelect(result.id)}
          >
            <h3 className="font-medium">{result.title}</h3>
            <p className="text-sm text-gray-600">{result.description}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
