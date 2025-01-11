package com.oneil.dms.ingestion;

import org.springframework.boot.autoconfigure.domain.EntityScan;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
@EntityScan
@Table
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class FileMetadata {
    private String documentId;
    private String fileType;
    private long fileSize;
    private String filename;
    private String documentName;
    
    
    // Add other metadata fields as needed

    // Getters and Setters
}
