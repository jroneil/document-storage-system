import * as React from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogTrigger,
} from "@/components/ui/dialog";

interface Column {
  id: string;
  label: string;
}

interface ColumnSelectorProps {
  columns: Column[];
  selectedColumns: string[];
  onSelect: (selected: string[]) => void;
}

export function ColumnSelector({
  columns,
  selectedColumns,
  onSelect,
}: ColumnSelectorProps) {
  const [selected, setSelected] = React.useState<string[]>(selectedColumns);
  const [unselected, setUnselected] = React.useState<string[]>(
    columns
      .filter((col) => !selectedColumns.includes(col.id))
      .map((col) => col.id)
  );

  const moveToSelected = (id: string) => {
    setUnselected(unselected.filter((item) => item !== id));
    setSelected([...selected, id]);
  };

  const moveToUnselected = (id: string) => {
    setSelected(selected.filter((item) => item !== id));
    setUnselected([...unselected, id]);
  };

  const handleSave = () => {
    onSelect(selected);
  };

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>Select Columns</Button>
      </DialogTrigger>
      <DialogContent className="w-96">
        <div className="flex space-x-4">
          {/* Unselected Columns */}
          <div className="flex-1">
            <h3 className="text-sm font-medium text-gray-600">Unselected</h3>
            <div className="border p-2 rounded h-64 overflow-auto">
              {unselected.map((id) => {
                const column = columns.find((col) => col.id === id);
                return (
                  <div
                    key={id}
                    className="flex items-center justify-between p-1"
                  >
                    <span className="text-sm">{column?.label}</span>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => moveToSelected(id)}
                    >
                      →
                    </Button>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Selected Columns */}
          <div className="flex-1">
            <h3 className="text-sm font-medium text-gray-600">Selected</h3>
            <div className="border p-2 rounded h-64 overflow-auto">
              {selected.map((id) => {
                const column = columns.find((col) => col.id === id);
                return (
                  <div
                    key={id}
                    className="flex items-center justify-between p-1"
                  >
                    <span className="text-sm">{column?.label}</span>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => moveToUnselected(id)}
                    >
                      ←
                    </Button>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Save Button */}
        <div className="mt-4 flex justify-end space-x-2">
          <Button variant="outline" onClick={() => onSelect(selectedColumns)}>
            Cancel
          </Button>
          <Button onClick={handleSave}>Save</Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}

