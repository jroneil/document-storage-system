'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/apiClient';
import { Search, Filter, X } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { SearchCriteria } from '@/types/document';

interface SearchFormProps {
    onSearch: (criteria: Record<string, SearchCriteria>) => void;
}

export default function SearchPage() {
    const router = useRouter();
    
    const handleSearch = async (filters: Record<string, SearchCriteria>) => {
        try {
            // Convert filters to query params
            const queryParams = new URLSearchParams();
            Object.entries(filters).forEach(([key, value]) => {
                if (value) {
                    queryParams.append(key, String(value));
                }
            });
            
            // Redirect to search results with filters
            router.push(`/search-results?${queryParams.toString()}`);
        } catch (error) {
            console.error('Search error:', error);
        }
    };

    return (
        <SearchForm onSearch={handleSearch} />
    );
}

export function SearchForm({ onSearch }: SearchFormProps) {
    // Define filters with correct type
    const [filters, setFilters] = useState<Record<string, string>>({
        fileName: '',
        fileType: '',
        category: '',
        division: '',
        businessUnit: '',
        documentType: '',
        region: '',
        country: '',
        language: '',
    });

    const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSearch(filters);
    };

    const handleReset = () => {
        setFilters({
            fileName: '',
            fileType: '',
            category: '',
            division: '',
            businessUnit: '',
            documentType: '',
            region: '',
            country: '',
            language: '',
        });
    };

    const handleFilterChange = (key: string, value: string) => {
        setFilters((prevFilters) => ({
            ...prevFilters,
            [key]: value,
        }));
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-lg shadow-md">
            {/* Search Bar */}
            <div className="flex flex-col md:flex-row gap-4 items-center">
                <Input
                    placeholder="Search by file name..."
                    value={filters.fileName}
                    onChange={(e) => handleFilterChange('fileName', e.target.value)}
                    className="flex-1"
                />
                <Button
                    type="button"
                    variant="outline"
                    onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
                    className="flex items-center"
                >
                    <Filter className="w-4 h-4 mr-2" />
                    Filters
                </Button>
                <Button type="submit" className="flex items-center">
                    <Search className="w-4 h-4 mr-2" />
                    Search
                </Button>
            </div>

            {/* Advanced Filters */}
            {showAdvancedFilters && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 bg-gray-50 border rounded-lg">
                    {/* Document Type */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Document Type</label>
                        <Select value={filters.documentType} onValueChange={(value) => handleFilterChange('documentType', value)}>
                            <SelectTrigger className="bg-white">
                                <SelectValue placeholder="Select Document Type" />
                            </SelectTrigger>
                            <SelectContent className='bg-white'>
                                <SelectItem value="manual">Manual</SelectItem>
                                <SelectItem value="report">Report</SelectItem>
                                <SelectItem value="specification">Specification</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    {/* Division */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Division</label>
                        <Select value={filters.division} onValueChange={(value) => handleFilterChange('division', value)}>
                            <SelectTrigger className="bg-white">
                                <SelectValue placeholder="Select Division" />
                            </SelectTrigger>
                            <SelectContent className="bg-white">
                                <SelectItem value="sales">Sales</SelectItem>
                                <SelectItem value="engineering">Engineering</SelectItem>
                                <SelectItem value="marketing">Marketing</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    {/* Business Unit */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Business Unit</label>
                        <Select value={filters.businessUnit} onValueChange={(value) => handleFilterChange('businessUnit', value)}>
                            <SelectTrigger className="bg-white">
                                <SelectValue placeholder="Select Business Unit" />
                            </SelectTrigger>
                            <SelectContent className="bg-white">
                                <SelectItem value="automotive">Automotive</SelectItem>
                                <SelectItem value="aerospace">Aerospace</SelectItem>
                                <SelectItem value="industrial">Industrial</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    {/* Region */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Region</label>
                        <Select value={filters.region} onValueChange={(value) => handleFilterChange('region', value)}>
                            <SelectTrigger className="bg-white">
                                <SelectValue placeholder="Select Region" />
                            </SelectTrigger>
                            <SelectContent className="bg-white">
                                <SelectItem value="na">North America</SelectItem>
                                <SelectItem value="emea">EMEA</SelectItem>
                                <SelectItem value="apac">APAC</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    {/* Language */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Language</label>
                        <Select value={filters.language} onValueChange={(value) => handleFilterChange('language', value)}>
                            <SelectTrigger className="bg-white">
                                <SelectValue placeholder="Select Language" />
                            </SelectTrigger>
                            <SelectContent className="bg-white">
                                <SelectItem value="en">English</SelectItem>
                                <SelectItem value="es">Spanish</SelectItem>
                                <SelectItem value="fr">French</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    {/* Clear Filters Button */}
                    <div className="col-span-1 md:col-span-3 flex justify-end">
                        <Button
                            type="button"
                            variant="ghost"
                            onClick={handleReset}
                            className="text-red-500 hover:text-red-700"
                        >
                            <X className="w-4 h-4 mr-2" />
                            Clear Filters
                        </Button>
                    </div>
                </div>
            )}
        </form>
    );
}
