'use client'

import { useState } from 'react'
import { SaveSearchModal } from './SaveSearchModal'
import { DocumentResult } from '@/types/document'

interface ResultsDisplayProps {
  results: DocumentResult[]
  onSelect: (id: string) => void
  searchCriteria: {
    query: string
    filters: Record<string, any>
  }
}

export default function ResultsDisplay({ results, onSelect, searchCriteria }: ResultsDisplayProps) {
  const [isSaveModalOpen, setIsSaveModalOpen] = useState(false)
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-2xl font-bold text-gray-900">Search Results</h2>
        <button
          className="px-6 py-2.5 bg-blue-600 text-white font-medium text-sm leading-tight uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
          onClick={() => setIsSaveModalOpen(true)}
        >
          Save Search
        </button>
      </div>

      <div className="space-y-4">
        {results.map(result => (
          <div
            key={result.id}
            className="group p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 cursor-pointer border border-gray-200 hover:border-blue-200"
            onClick={() => onSelect(result.id)}
          >
            <h3 className="text-lg font-semibold text-gray-800 mb-2">{result.title}</h3>
            <p className="text-sm text-gray-600 leading-relaxed">{result.description}</p>
            <div className="mt-4 flex space-x-4">
              <span className="text-xs px-2.5 py-1 rounded-full bg-blue-50 text-blue-700">Document</span>
              <span className="text-xs px-2.5 py-1 rounded-full bg-green-50 text-green-700">Available</span>
            </div>
          </div>
        ))}
      </div>

      <SaveSearchModal
        open={isSaveModalOpen}
        onOpenChange={setIsSaveModalOpen}
        searchCriteria={searchCriteria}
      />
    </div>
  )
}
