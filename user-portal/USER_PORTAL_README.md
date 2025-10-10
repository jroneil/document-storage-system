# User Portal - Document Management System

A Next.js-based user portal for managing users, projects, and documents in the Document Management System.

## Features

- **User Authentication**: Login and registration with secure password handling
- **Project Management**: Create and manage projects
- **User Dashboard**: View all projects and their statistics
- **Responsive Design**: Mobile-friendly interface built with Tailwind CSS
- **Type-Safe API**: TypeScript types for all API interactions

## Tech Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context API
- **API Client**: Custom fetch-based client

## Project Structure

```
user-portal/
├── src/
│   ├── app/                    # Next.js app router pages
│   │   ├── layout.tsx         # Root layout with AuthProvider
│   │   ├── page.tsx           # Home page
│   │   ├── login/             # Login page
│   │   ├── register/          # Registration page
│   │   └── dashboard/         # Dashboard page
│   ├── contexts/              # React contexts
│   │   └── AuthContext.tsx    # Authentication context
│   ├── lib/                   # Utilities and API client
│   │   └── api.ts             # API client
│   └── types/                 # TypeScript type definitions
│       ├── user.ts            # User-related types
│       └── project.ts         # Project-related types
├── .env.local.example         # Environment variables template
└── package.json               # Dependencies
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd user-portal
npm install
```

### 2. Configure Environment Variables

Create a `.env.local` file from the example:

```bash
cp .env.local.example .env.local
```

Update the API URL in `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start the Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
npm start
```

## Available Pages

### Home Page (`/`)
- Landing page with navigation to login/register

### Login Page (`/login`)
- User authentication
- Redirects to dashboard on successful login
- Link to registration page

### Registration Page (`/register`)
- New user account creation
- Form validation
- Redirects to login page after successful registration

### Dashboard Page (`/dashboard`)
- Protected route (requires authentication)
- Displays user's projects
- Create new projects
- Project statistics (documents, storage, status)
- Logout functionality

## API Integration

The portal connects to the metadata service API for all user and project operations.

### User APIs
- `POST /users/` - Create new user
- `GET /users/` - List users
- `GET /users/{id}` - Get user details
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user
- `POST /users/authenticate` - Login
- `POST /users/{id}/change-password` - Change password

### Project APIs
- `POST /projects/` - Create project
- `GET /projects/` - List projects
- `GET /projects/user/{user_id}` - Get user's projects
- `GET /projects/{id}` - Get project details
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project
- `POST /projects/{id}/archive` - Archive project
- `GET /projects/{id}/statistics` - Get project statistics

## Type Definitions

### User Types

```typescript
type UserRole = 'admin' | 'manager' | 'member' | 'viewer';

interface User {
  user_id: string;
  username: string;
  email: string;
  full_name?: string;
  role: UserRole;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
  last_login?: string;
  // ... additional fields
}
```

### Project Types

```typescript
type ProjectStatus = 'active' | 'archived' | 'deleted';
type ProjectRole = 'owner' | 'admin' | 'editor' | 'viewer';

interface Project {
  project_id: string;
  name: string;
  description?: string;
  status: ProjectStatus;
  owner_id?: string;
  storage_used: number;
  document_count: number;
  is_public: boolean;
  // ... additional fields
}
```

## Authentication Flow

1. User navigates to `/login`
2. Submits credentials
3. API authenticates user
4. User data stored in localStorage and React Context
5. User redirected to `/dashboard`
6. Protected routes check for authenticated user
7. On logout, clear localStorage and Context

## Project Management

### Creating a Project

1. Click "New Project" button
2. Fill in project details:
   - Name (required)
   - Description (optional)
   - Public visibility (optional)
3. Submit form
4. Project created with current user as owner
5. Dashboard refreshes to show new project

### Viewing Projects

Dashboard displays:
- Project name and description
- Document count
- Storage used
- Project status
- Creation date
- Tags

## Styling

The portal uses Tailwind CSS for styling with a clean, modern design:

- **Colors**: Blue primary (#3B82F6), Gray neutrals
- **Layout**: Responsive grid system
- **Components**: Cards, buttons, forms, modals
- **Typography**: System fonts (Geist Sans, Geist Mono)

## Development Guidelines

### Adding New Pages

1. Create page in `src/app/[route]/page.tsx`
2. Add 'use client' directive if using hooks
3. Implement page component
4. Add navigation links where needed

### Adding New API Endpoints

1. Add types in `src/types/`
2. Add methods to `src/lib/api.ts`
3. Use in components

### State Management

- Use React Context for global state (authentication)
- Use local state for component-specific data
- Use useEffect for data fetching

## Error Handling

- API errors displayed in red alert boxes
- Form validation errors shown inline
- Loading states for async operations
- Network error handling

## Security Considerations

1. **Authentication**: User credentials stored securely
2. **Password Requirements**: Minimum 8 characters
3. **Protected Routes**: Dashboard requires authentication
4. **API Communication**: CORS-enabled API calls
5. **Input Validation**: Client and server-side validation

## Future Enhancements

- [ ] Implement JWT-based authentication
- [ ] Add password reset functionality
- [ ] Email verification system
- [ ] User profile editing
- [ ] Project detail pages
- [ ] Document upload interface
- [ ] Project collaboration features
- [ ] User search and filtering
- [ ] Project sharing
- [ ] Activity logs
- [ ] Notifications
- [ ] Dark mode support

## Troubleshooting

### Cannot connect to API
- Verify metadata service is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify CORS is enabled on the API

### Login not working
- Check username and password
- Verify user exists in database
- Check browser console for errors

### Projects not loading
- Ensure user is authenticated
- Check API connectivity
- Verify database has user's projects

### Build errors
- Run `npm install` to ensure all dependencies are installed
- Delete `.next` folder and rebuild
- Check for TypeScript errors

## Contributing

1. Create a feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## License

MIT License

## Support

For issues or questions, please refer to the main project documentation.
