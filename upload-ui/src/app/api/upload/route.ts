import { NextRequest, NextResponse } from 'next/server';
import { validateFile } from '../../../../lib/utils';
import { UploadResponse, UploadError } from '../../../../types/upload';

export async function POST(request: NextRequest): Promise<NextResponse<UploadResponse | UploadError>> {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    // Validate file exists
    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      );
    }

    // Validate file using utility function
    const validation = validateFile(file);
    if (!validation.isValid) {
      return NextResponse.json(
        { error: validation.error || 'File validation failed' },
        { status: 400 }
      );
    }

    // Extract metadata fields
    const metadata = {
      brand: formData.get('brand') as string,
      business: formData.get('business') as string,
      unit: formData.get('unit') as string,
      doc_type: formData.get('doc_type') as string,
      doc_name: formData.get('doc_name') as string,
      doc_date: formData.get('doc_date') as string,
      revision: formData.get('revision') as string,
      owner_team: formData.get('owner_team') as string,
    };

    // Validate metadata
    if (!Object.values(metadata).every(value => value && value.trim())) {
      return NextResponse.json(
        { error: 'All metadata fields are required' },
        { status: 400 }
      );
    }

    // Create new FormData for the upload service
    const uploadFormData = new FormData();
    uploadFormData.append('file', file);
    
    // Add metadata fields to the form data
    Object.entries(metadata).forEach(([key, value]) => {
      uploadFormData.append(key, value);
    });

    // Get the upload service URL from environment
    const uploadServiceHost = process.env.UPLOAD_SERVICE_HOST || 'http://localhost:5003';
    
    // Forward the request to the upload service with timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

    try {
      const response = await fetch(`${uploadServiceHost}/upload-document`, {
        method: 'POST',
        body: uploadFormData,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Upload service error:', {
          status: response.status,
          statusText: response.statusText,
          error: errorText
        });
        
        return NextResponse.json(
          { error: `Upload failed: ${response.statusText}` },
          { status: response.status }
        );
      }

      const data = await response.json();
      
      return NextResponse.json({
        message: 'Document uploaded successfully',
        data: {
          filename: file.name,
          size: file.size,
          uploadedAt: new Date().toISOString(),
          metadata,
          ...data
        }
      });

    } catch (fetchError) {
      clearTimeout(timeoutId);
      
      if (fetchError instanceof Error && fetchError.name === 'AbortError') {
        console.error('Upload timeout:', fetchError);
        return NextResponse.json(
          { error: 'Upload timeout - service took too long to respond' },
          { status: 504 }
        );
      }
      
      throw fetchError;
    }

  } catch (error) {
    console.error('Upload API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'Upload API is running',
    maxFileSize: process.env.MAX_FILE_SIZE,
    allowedFileTypes: process.env.ALLOWED_FILE_TYPES?.split(',')
  });
}
