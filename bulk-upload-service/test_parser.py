#!/usr/bin/env python3
"""
Test script to verify the enhanced metadata parser works with all file formats
"""

import sys
import os
import json

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.services.metadata_parser import MetadataParser

def test_parser():
    """Test the metadata parser with different file formats"""
    parser = MetadataParser()
    
    test_files = [
        'sample_document_metadata.csv',
        'sample_document_metadata.json', 
        'sample_document_metadata.xml'
    ]
    
    print("Testing Metadata Parser with different file formats...")
    print("=" * 60)
    
    for test_file in test_files:
        file_path = os.path.join(os.path.dirname(__file__), test_file)
        
        if not os.path.exists(file_path):
            print(f"[ERROR] Test file not found: {test_file}")
            continue
            
        print(f"\n[TESTING] {test_file}")
        print("-" * 40)
        
        try:
            result = parser.parse_file(file_path, "test-job-123")
            
            print(f"[SUCCESS] Successfully parsed {test_file}")
            print(f"   Job ID: {result['job_id']}")
            print(f"   Records processed: {len(result['records'])}")
            print(f"   Validation errors: {len(result['validation_errors'])}")
            
            if result['records']:
                first_record = result['records'][0]
                print(f"   First record ID: {first_record['record_id'][:16]}...")
                print(f"   File name: {first_record['asset']['file_name']}")
                print(f"   File size: {first_record['asset']['file_size']}")
                print(f"   Tags: {first_record['metadata']['tags']}")
                print(f"   Languages: {first_record['metadata']['languages']}")
            
            if result['validation_errors']:
                print(f"   [WARNING] Validation errors found:")
                for error in result['validation_errors']:
                    print(f"      Row {error['row_num']}: {error['error']}")
                    
        except Exception as e:
            print(f"[ERROR] Failed to parse {test_file}: {e}")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Parser test completed!")

if __name__ == "__main__":
    test_parser()
