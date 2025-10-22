# Metadata UI - Design Documentation

## Overview

The Metadata UI is a comprehensive document metadata management interface built with Next.js 15, TypeScript, and Tailwind CSS. It provides a sophisticated editing experience for document metadata with support for standard properties, dynamic fields, branding configurations, and user permission controls.

## Architecture

### Technology Stack
- **Frontend Framework**: Next.js 15 with App Router
- **Language**: TypeScript for type safety
- **Styling**: Tailwind CSS for responsive design
- **State Management**: React Hooks (useState)
- **Build Tool**: Turbopack for fast development

### Project Structure
```
metadata-ui/
├── src/
│   ├── app/
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Landing page
│   │   └── metadata-edit/
│   │       └── page.tsx        # Metadata editor demo
│   ├── components/
│   │   └── MetadataEditScreen.tsx  # Main editor component
│   └── types/
│       └── metadata.ts         # TypeScript interfaces
├── public/                     # Static assets
└── package.json               # Dependencies
```

## Core Components

### 1. MetadataEditScreen Component

The main editor component that handles all metadata editing functionality.

#### Key Features:
- **Edit/View Mode Toggle**: Switch between read-only and editable states
- **Permission-Based Access**: Different access levels for admin vs regular users
- **Form State Management**: Comprehensive form handling with React hooks
- **Responsive Design**: Mobile-first approach with Tailwind CSS

#### Props Interface:
```typescript
interface MetadataEditScreenProps {
  document: Document;
  brand?: Brand;
  dynamicMetadata: DynamicMetadata;
  currentUser: User;
  onSave: (data: MetadataFormData) => void;
  onCancel: () => void;
}
```

### 2. Data Models

#### Document Interface
```typescript
interface Document {
  document_id: string;
  file_name: string;
  file_size: number;
  file_type: string;
  upload_date: string;
  last_modified_date: string;
  user_id: string;
  tags: string[];
  description?: string;
  storage_path: string;
  version: number;
  checksum: string;
  acl?: any;
  thumbnail_path?: string;
  expiration_date?: string;
  category?: string;
  division?: string;
  business_unit?: string;
  brand_id?: string;
  document_type: string;
  status?: 'draft' | 'published' | 'archived';
}
```

#### Brand Interface
```typescript
interface Brand {
  brand_id: string;
  name: string;
  required_metadata: Record<string, string>;
}
```

#### DynamicMetadata Interface
```typescript
interface DynamicMetadata {
  document_id: string;
  available_countries: string[];
  languages: string[];
  brand_colors: string[];
  brand_logo_path: string;
  campaign_name: string;
  product_line: string;
  custom_fields?: Record<string, any>;
}
```

## UI Sections

### 1. Header Section
**Purpose**: Display essential document identification and status information

**Fields**:
- Document ID (read-only)
- Document Number (read-only)
- Title (editable)
- Publication Date (editable)
- Status (editable dropdown)
- File Size (read-only, formatted)
- File Type (read-only)
- Last Modified (read-only)

**Layout**: 4-column responsive grid (collapses on smaller screens)

### 2. Standard Metadata Section
**Purpose**: Manage structured document metadata in a clean 2-column layout

**Left Column**:
- Description (textarea)
- Category (text input)
- Division (text input)
- Tags (comma-separated text input)

**Right Column**:
- Business Unit (text input)
- Document Type (text input)
- Version (number input)
- Expiration Date (date input)

### 3. Branding Section
**Purpose**: Configure brand-specific metadata requirements

**Admin-Only Features**:
- Brand Name editing
- Required Metadata Fields management:
  - Add new fields
  - Edit field names
  - Set field types (String, Number, Boolean, Date, Array)
  - Remove fields
- Brand association options

**Regular User View**: Read-only display of brand information

### 4. Dynamic Metadata Section
**Purpose**: Handle flexible, user-defined metadata

**Predefined Fields**:
- Campaign Name
- Product Line
- Available Countries (comma-separated)
- Languages (comma-separated)
- Brand Colors (comma-separated hex values)
- Brand Logo Path

**Custom Fields Management**:
- Add new custom fields
- Edit field names and values
- Remove fields
- Visual empty state with guidance

## Permission System

### User Roles
- **Admin Users**: Full access to edit all documents and branding
- **Regular Users**: Can only edit their own documents, branding is read-only

### Permission Logic
```typescript
const canEdit = currentUser.role === 'admin' || 
                (currentUser.role === 'user' && document.user_id === currentUser.user_id);
```

### Branding Access Control
- Brand name editing: `isEditMode && currentUser.role === 'admin'`
- Required metadata management: `isEditMode && currentUser.role === 'admin'`
- Brand association: `isEditMode && currentUser.role === 'admin'`

## State Management

### Form Data Structure
```typescript
interface MetadataFormData {
  document: Document;
  brand?: Brand;
  dynamicMetadata: DynamicMetadata;
  customFields: Record<string, any>;
}
```

### State Updates
- **Section-based updates**: Handle changes per metadata section
- **Dynamic field management**: Add, edit, remove custom fields
- **Brand management**: Admin-only branding modifications
- **Form reset**: Cancel operation reverts to original data

## User Experience Features

### 1. Edit/View Mode Toggle
- Clear visual distinction between modes
- Permission-based edit button visibility
- Cancel operation with confirmation

### 2. Responsive Design
- Mobile-first approach
- Grid layouts that adapt to screen size
- Touch-friendly interface elements

### 3. Visual Feedback
- Disabled state styling for read-only fields
- Success/error states for operations
- Loading states for async operations
- Empty state messaging

### 4. Accessibility
- Proper form labels and descriptions
- Keyboard navigation support
- Screen reader compatibility
- Focus management

## Integration Points

### Metadata Service API
The UI is designed to integrate with the metadata service backend:

**Endpoints**:
- `GET /stand-properties/{stand_id}` - Retrieve document metadata
- `POST /stand-properties/` - Create/update document metadata
- `GET /dynamic-metadata/{document_id}` - Retrieve dynamic metadata
- `POST /dynamic-metadata/` - Create/update dynamic metadata
- `GET /brands/{brand_id}` - Retrieve brand information
- `POST /brands/` - Create/update brand configurations

### Data Flow
1. Load initial data from metadata service
2. User makes edits in the UI
3. Validate changes against brand requirements (if applicable)
4. Save changes to metadata service
5. Handle success/error responses

## Development Guidelines

### Component Development
- Use TypeScript for type safety
- Follow React best practices with hooks
- Implement proper error boundaries
- Write comprehensive unit tests

### Styling Approach
- Use Tailwind CSS utility classes
- Maintain consistent spacing and colors
- Follow mobile-first responsive design
- Ensure accessibility compliance

### State Management
- Keep state as local as possible
- Use proper React patterns for updates
- Implement optimistic updates where appropriate
- Handle loading and error states

## Future Enhancements

### Planned Features
1. **Real-time Collaboration**: Multiple users editing simultaneously
2. **Version History**: Track changes to metadata over time
3. **Bulk Operations**: Edit multiple documents at once
4. **Advanced Search**: Filter and search metadata
5. **Export Capabilities**: Export metadata in various formats
6. **Workflow Integration**: Integration with document approval workflows

### Technical Improvements
1. **Performance Optimization**: Virtual scrolling for large datasets
2. **Offline Support**: Local storage and sync capabilities
3. **Internationalization**: Multi-language support
4. **Theme System**: Customizable UI themes
5. **Plugin Architecture**: Extensible field types and validators

## Running the Application

### Development
```bash
cd metadata-ui
npm install
npm run dev
```

### Production Build
```bash
npm run build
npm start
```

### Testing
```bash
npm test
npm run test:coverage
```

## Demo Features

The included demo showcases:
- Mock data with realistic document scenarios
- User role switching (User ↔ Admin)
- Full editing capabilities
- Permission-based access control
- Responsive design testing

Access the demo at `http://localhost:3000` and navigate to `/metadata-edit` to experience the full functionality.
