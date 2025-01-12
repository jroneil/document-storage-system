"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { DatePicker } from "@/components/ui/date-picker";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export function SearchForm() {
  const [searchParams, setSearchParams] = useState({
    documentName: "",
    division: "",
    businessUnit: "",
    startDate: null,
    endDate: null,
    documentType: "",
  });

  const handleSearch = (e) => {
    e.preventDefault();
    // TODO: Implement search logic
  };

  return (
    <form onSubmit={handleSearch} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <Input
          placeholder="Document Name"
          value={searchParams.documentName}
          onChange={(e) =>
            setSearchParams({ ...searchParams, documentName: e.target.value })
          }
        />

        <Select
          value={searchParams.division}
          onValueChange={(value) =>
            setSearchParams({ ...searchParams, division: value })
          }
        >
          <SelectTrigger>
            <SelectValue placeholder="Select Division" />
          </SelectTrigger>
          <SelectContent>
            {/* TODO: Fetch divisions from API */}
            <SelectItem value="division1">Division 1</SelectItem>
            <SelectItem value="division2">Division 2</SelectItem>
          </SelectContent>
        </Select>

        <Select
          value={searchParams.businessUnit}
          onValueChange={(value) =>
            setSearchParams({ ...searchParams, businessUnit: value })
          }
        >
          <SelectTrigger>
            <SelectValue placeholder="Select Business Unit" />
          </SelectTrigger>
          <SelectContent>
            {/* TODO: Fetch business units from API */}
            <SelectItem value="unit1">Business Unit 1</SelectItem>
            <SelectItem value="unit2">Business Unit 2</SelectItem>
          </SelectContent>
        </Select>

        <DatePicker
          selected={searchParams.startDate}
          onChange={(date) =>
            setSearchParams({ ...searchParams, startDate: date })
          }
          placeholderText="Start Date"
        />

        <DatePicker
          selected={searchParams.endDate}
          onChange={(date) =>
            setSearchParams({ ...searchParams, endDate: date })
          }
          placeholderText="End Date"
        />

        <Select
          value={searchParams.documentType}
          onValueChange={(value) =>
            setSearchParams({ ...searchParams, documentType: value })
          }
        >
          <SelectTrigger>
            <SelectValue placeholder="Select Document Type" />
          </SelectTrigger>
          <SelectContent>
            {/* TODO: Fetch document types from API */}
            <SelectItem value="type1">Document Type 1</SelectItem>
            <SelectItem value="type2">Document Type 2</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="flex justify-end">
        <Button type="submit">Search</Button>
      </div>
    </form>
  );
}
