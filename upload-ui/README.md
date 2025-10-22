# Upload UI

A Next.js application for bulk file uploads with a modern, responsive interface.

## Features

- **Modern UI**: Clean, responsive design with Tailwind CSS
- **File Validation**: Server-side validation for file types and sizes
- **Drag & Drop**: Intuitive file upload interface
- **Progress Tracking**: Real-time upload progress indication
- **Error Handling**: Comprehensive error handling and user feedback
- **TypeScript**: Full TypeScript support for type safety

## Project Structure

```
upload-ui/
├── .env.local              # Environment variables (git-ignored)
├── .clinerules             # Development guidelines and best practices
├── src/
│   ├── app/
│   │   ├── api/upload/     # API route for file uploads
│   │   ├── globals.css     # Global styles
│   │   ├── layout.tsx      # Root layout
│   │   └── page.tsx        # Main upload page
├── lib/
│   └── utils.ts            # Utility functions
├── types/
│   └── upload.ts           # TypeScript type definitions
├── components/             # React components (organized structure)
└── public/                 # Static assets
```

## Environment Variables

Create a `.env.local` file in the root directory with the following variables:

```env
# Server Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:3000/api
NEXT_PUBLIC_BULK_UPLOAD_SERVICE_URL=http://localhost:5000

# Upload Configuration
MAX_FILE_SIZE=10485760  # 10MB in bytes
ALLOWED_FILE_TYPES=image/jpeg,image/png,image/gif,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/csv,application/vnd.oasis.opendocument.spreadsheet

# Development Configuration
NODE_ENV=development
```

## Development

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

## API Endpoints

### POST /api/upload
Upload a file to the bulk upload service.

**Request:**
- Method: POST
- Body: FormData with 'file' field

**Response:**
```json
{
  "message": "File uploaded successfully",
  "data": {
    "filename": "example.pdf",
    "size": 1024,
    "uploadedAt": "2025-01-18T15:30:00.000Z"
  }
}
```

### GET /api/upload
Get upload API status and configuration.

**Response:**
```json
{
  "message": "Upload API is running",
  "maxFileSize": "10485760",
  "allowedFileTypes": ["image/jpeg", "image/png", ...]
}
```

## Features Implemented

### ✅ Core Functionality
- File upload with drag & drop support
- Progress tracking and status updates
- File validation (size and type)
- Error handling and user feedback

### ✅ Architecture Improvements
- Proper Next.js App Router structure
- TypeScript with strict type checking
- Environment-based configuration
- Utility functions for reusable logic
- API route handlers with proper error handling

### ✅ Code Quality
- Follows Next.js best practices
- Proper separation of concerns
- Type-safe API responses
- Comprehensive error handling
- Clean, maintainable code structure

## Technologies Used

- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **React**: UI library with hooks

## Deployment

The application can be deployed to any platform that supports Next.js:

- Vercel (recommended)
- Netlify
- AWS Amplify
- Self-hosted Node.js server

Make sure to set the appropriate environment variables in your deployment platform.
