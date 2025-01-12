'use client';

import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from './ui/dialog';
import { saveSearch } from '@/lib/userPreferences';
import { useToast } from './ui/use-toast';

interface SaveSearchModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  searchCriteria: {
    query: string;
    filters: Record<string, any>;
    name?: string;
  };
}

export function SaveSearchModal({ open, onOpenChange, searchCriteria }: SaveSearchModalProps) {
  const { toast } = useToast();
  const [name, setName] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  const handleSave = async () => {
    if (!name.trim()) {
      toast({
        title: 'Error',
        description: 'Please enter a name for your search',
        variant: 'destructive',
      });
      return;
    }

    try {
      setIsSaving(true);
      await saveSearch({
        name,
        criteria: searchCriteria
      });
      
      toast({
        title: 'Success',
        description: 'Search criteria saved successfully',
      });
      onOpenChange(false);
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Failed to save search criteria',
        variant: 'destructive',
      });
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Save Search</DialogTitle>
        </DialogHeader>
        
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <div className="text-right">
              Name
            </div>
            <Input
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="col-span-3"
              placeholder="Enter a name for your search"
            />
          </div>
        </div>

        <DialogFooter>
          <Button 
            type="submit"
            onClick={handleSave}
            disabled={isSaving}
          >
            {isSaving ? 'Saving...' : 'Save Search'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
