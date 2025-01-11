package com.oneil.dms.ingestion.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/files")
public class FileUploadController {

    // Endpoint for file upload
    @PostMapping("/upload")
    public ResponseEntity<String> uploadFile(@RequestParam("file") MultipartFile file) {
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().body("File is empty!");
        }
        // Validate file type and size
        String fileType = file.getContentType();
        long fileSize = file.getSize();
        if (!isValidFileType(fileType)) {
            return ResponseEntity.badRequest().body("Invalid file type!");
        }
        if (fileSize > 10485760) { // 10 MB limit
            return ResponseEntity.badRequest().body("File size exceeds the limit!");
        }
        // Process the file
        fileService.handleFileUpload(file);
        return ResponseEntity.ok("File uploaded successfully!");
    }

    @PostMapping("/bulk-upload")
    public ResponseEntity<String> uploadBulkFiles(@RequestParam("file") MultipartFile file) {
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().body("File is empty!");
        }
        // Validate file type
        String fileType = file.getContentType();
        if (!isValidFileType(fileType)) {
            return ResponseEntity.badRequest().body("Invalid file type!");
        }
        // Process the bulk file
        fileService.handleBulkFileUpload(file);
        return ResponseEntity.ok("Bulk upload processed successfully!");
    }

    private boolean isValidFileType(String fileType) {
        // Add logic to validate file types (e.g., image/jpeg, application/pdf)
        return true; // Placeholder
    }
}
