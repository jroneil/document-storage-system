import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
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

    // Validate file type
    const allowedExtensions = ['csv', 'json', 'xml', 'xlsx', 'xls'];
    const fileExtension = file.name.toLowerCase().split('.').pop();
    
    if (!fileExtension || !allowedExtensions.includes(fileExtension)) {
      return NextResponse.json(
        { 
          error: `Unsupported file type: ${fileExtension}. Allowed types: ${allowedExtensions.join(', ')}` 
        },
        { status: 400 }
      );
    }

    // Create new FormData for the bulk upload service
    const bulkUploadFormData = new FormData();
    bulkUploadFormData.append('file', file);

    // Get the bulk upload service URL from environment
    const bulkUploadServiceHost = process.env.BULK_UPLOAD_SERVICE_HOST || 'http://localhost:5004';
    
    // Forward the request to the bulk upload service with timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout for bulk processing

    try {
      const response = await fetch(`${bulkUploadServiceHost}/bulk-upload`, {
        method: 'POST',
        body: bulkUploadFormData,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Bulk upload service error:', {
          status: response.status,
          statusText: response.statusText,
          error: errorText
        });
        
        return NextResponse.json(
          { error: `Bulk upload failed: ${response.statusText}` },
          { status: response.status }
        );
      }

      const data = await response.json();
      
      return NextResponse.json({
        message: data.message || 'Bulk upload processing started',
        job_id: data.job_id,
        records_processed: data.records_processed,
        validation_errors: data.validation_errors,
        source_file: data.source_file
      });

    } catch (fetchError) {
      clearTimeout(timeoutId);
      
      if (fetchError instanceof Error && fetchError.name === 'AbortError') {
        console.error('Bulk upload timeout:', fetchError);
        return NextResponse.json(
          { error: 'Bulk upload timeout - service took too long to respond' },
          { status: 504 }
        );
      }
      
      throw fetchError;
    }

  } catch (error) {
    console.error('Bulk upload API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'Bulk Upload API is running',
    allowed_file_types: ['csv', 'json', 'xml', 'xlsx', 'xls'],
    service_endpoint: '/api/bulk-upload'
  });
}
