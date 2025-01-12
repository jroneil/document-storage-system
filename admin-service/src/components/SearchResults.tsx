'use client'

import { useState, useEffect } from 'react'
import Popup from './Popup'
import ResultsDisplay from './ResultsDisplay'
import { getPreferences } from '@/lib/userPreferences'
import { Button } from './ui/button'

interface SavedSearch {
  name: string
  criteria: Record<string, any>
}

interface DocumentResult {
  id: string
  title: string
  description: string
  type: string
  date: string
  status: string
}

export default function SearchResults() {
  const [showResults, setShowResults] = useState(false)
  const [results, setResults] = useState<DocumentResult[]>([])
  const [savedSearches, setSavedSearches] = useState<SavedSearch[]>([])
  const [showSavedSearches, setShowSavedSearches] = useState(false)

  // Load saved searches on mount
  useEffect(() => {
    const loadSavedSearches = async () => {
      try {
        const preferences = await getPreferences()
        setSavedSearches(preferences.savedSearches)
      } catch (error) {
        console.error('Failed to load saved searches:', error)
      }
    }
    loadSavedSearches()
  }, [])

  // Mock data for demonstration
  const mockResults = [
    { 
      id: '1', 
      title: 'Document 1', 
      description: 'Sample document description 1',
      type: 'PDF', 
      date: '2023-01-01', 
      status: 'Approved' 
    },
    { 
      id: '2', 
      title: 'Document 2', 
      description: 'Sample document description 2',
      type: 'DOCX', 
      date: '2023-02-15', 
      status: 'Pending' 
    },
    { 
      id: '3', 
      title: 'Document 3', 
      description: 'Sample document description 3',
      type: 'XLSX', 
      date: '2023-03-20', 
      status: 'Rejected' 
    }
  ]

  const handleSearch = () => {
    // TODO: Replace with actual search logic
    setResults(mockResults)
    setShowResults(true)
  }

  const handleLoadSearch = (searchCriteria: Record<string, any>) => {
    // TODO: Implement search with loaded criteria
    console.log('Loading search:', searchCriteria)
    handleSearch()
  }

  const handleSelect = (id: string) => {
    // TODO: Handle document selection
    console.log('Selected document:', id)
    setShowResults(false)
  }

  return (
    <div className="space-y-4">
      <div className="flex gap-2">
        <Button onClick={handleSearch}>
          Search
        </Button>
        <Button 
          variant="outline" 
          onClick={() => setShowSavedSearches(!showSavedSearches)}
        >
          {showSavedSearches ? 'Hide' : 'Show'} Saved Searches
        </Button>
      </div>

      {showSavedSearches && (
        <div className="space-y-2">
          {savedSearches.map((search, index) => (
            <div 
              key={index}
              className="p-2 border rounded hover:bg-gray-50 cursor-pointer"
              onClick={() => handleLoadSearch(search.criteria)}
            >
              <div className="font-medium">{search.name}</div>
              <div className="text-sm text-gray-500">
                {Object.entries(search.criteria).map(([key, value]) => (
                  <div key={key}>{key}: {JSON.stringify(value)}</div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {showResults && (
        <Popup onClose={() => setShowResults(false)}>
          <ResultsDisplay 
            results={results} 
            onSelect={handleSelect}
          />
        </Popup>
      )}
    </div>
  )
}
