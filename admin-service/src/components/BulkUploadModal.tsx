import * as React from "react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

export function BulkUploadModal() {
  return (
    <Dialog >
      <DialogTrigger asChild>
        <Button>Bulk Upload</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Bulk Upload Documents</DialogTitle>
          <div className="text-sm text-muted-foreground">
            Upload multiple documents at once. Click upload when you're done.
          </div>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          {/* File upload input will go here */}
        </div>
        <DialogFooter>
          <Button type="submit">Upload</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
