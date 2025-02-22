package com.oneil.dms.ingestion.service;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.oneil.dms.ingestion.FileMetadata;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.UUID;

@Service
public class FileService {

    public void handleFileUpload(MultipartFile file) {
        // Generate unique document ID
        String documentId = generateDocumentId();
        // Extract metadata
        FileMetadata metadata = extractMetadata(file, documentId);
        // Send message to the message queue
        sendMessageToQueue(metadata);
    }

    public void handleBulkFileUpload(MultipartFile file) {
        // Logic to read and process Excel/CSV file
        // For demonstration, we'll assume it's a CSV file
        try (BufferedReader br = new BufferedReader(new InputStreamReader(file.getInputStream()))) {
            String line;
            while ((line = br.readLine()) != null) {
                // Parse each line and create metadata
                String[] metadataFields = line.split(","); // Assuming CSV format
                FileMetadata metadata = new FileMetadata();
                metadata.setDocumentId(generateDocumentId());
                metadata.setFileType(metadataFields[0]); // Example field
                metadata.setFileSize(Long.parseLong(metadataFields[1])); // Example field
                // Send message to the message queue
                sendMessageToQueue(metadata);
            }
        } catch (IOException e) {
            e.printStackTrace(); // Handle exception appropriately
        }
    }

    private String generateDocumentId() {
        return UUID.randomUUID().toString();
    }

    private FileMetadata extractMetadata(MultipartFile file, String documentId) {
        FileMetadata metadata = new FileMetadata();
        metadata.setDocumentId(documentId);
        metadata.setFileType(file.getContentType());
        metadata.setFileSize(file.getSize());
        // Add logic to extract additional metadata if needed
        return metadata;
    }

    private void sendMessageToQueue(FileMetadata metadata) {
        // Logic to send metadata to the message queue (RabbitMQ/Kafka)
    }
}

class FileMetadata {
    private String documentId;
    private String fileType;
    private long fileSize;

    public String getDocumentId() {
        return documentId;
    }

    public void setDocumentId(String documentId) {
        this.documentId = documentId;
    }

    public String getFileType() {
        return fileType;
    }

    public void setFileType(String fileType) {
        this.fileType = fileType;
    }

    public long getFileSize() {
        return fileSize;
    }

    public void setFileSize(long fileSize) {
        this.fileSize = fileSize;
    }
}
