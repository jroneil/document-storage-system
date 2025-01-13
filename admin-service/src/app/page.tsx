'use client';

import { useState } from 'react';
import { Users, FileText, Database, Settings, BarChart2 } from 'lucide-react';

export default function AdminPage() {
  const [stats] = useState({
    users: 1234,
    documents: 5678,
    storage: '2.3 TB',
  });

  return (
    <>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Dashboard Overview</h1>
        <p className="text-gray-600">Welcome back! Here's what's happening in your system.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-black-50 p-6 rounded-lg shadow-sm">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-medium text-gray-600">Total Users</h2>
            <Users className="w-5 h-5 text-blue-500" />
          </div>
          <p className="mt-2 text-3xl font-semibold text-gray-900">{stats.users}</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-medium text-gray-600">Documents</h2>
            <FileText className="w-5 h-5 text-green-500" />
          </div>
          <p className="mt-2 text-3xl font-semibold text-gray-900">{stats.documents}</p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-medium text-gray-600">Storage Used</h2>
            <Database className="w-5 h-5 text-purple-500" />
          </div>
          <p className="mt-2 text-3xl font-semibold text-gray-900">{stats.storage}</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <a 
          href="/admin/users" 
          className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow"
        >
          <div className="flex items-center space-x-3 mb-2">
            <div className="p-2 bg-blue-50 rounded-lg">
              <Users className="w-5 h-5 text-blue-500" />
            </div>
            <h2 className="font-medium text-gray-900">Users</h2>
          </div>
          <p className="text-sm text-gray-600 mb-4">Manage system users and permissions</p>
          <span className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center">
            Manage users
            <span className="ml-2">→</span>
          </span>
        </a>

        <a 
          href="/admin/settings" 
          className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow"
        >
          <div className="flex items-center space-x-3 mb-2">
            <div className="p-2 bg-green-50 rounded-lg">
              <Settings className="w-5 h-5 text-green-500" />
            </div>
            <h2 className="font-medium text-gray-900">Settings</h2>
          </div>
          <p className="text-sm text-gray-600 mb-4">Configure system settings and preferences</p>
          <span className="text-sm text-green-600 hover:text-green-700 font-medium flex items-center">
            Manage settings
            <span className="ml-2">→</span>
          </span>
        </a>

        <a 
          href="/admin/analytics" 
          className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow"
        >
          <div className="flex items-center space-x-3 mb-2">
            <div className="p-2 bg-purple-50 rounded-lg">
              <BarChart2 className="w-5 h-5 text-purple-500" />
            </div>
            <h2 className="font-medium text-gray-900">Analytics</h2>
          </div>
          <p className="text-sm text-gray-600 mb-4">View detailed system usage statistics</p>
          <span className="text-sm text-purple-600 hover:text-purple-700 font-medium flex items-center">
            View analytics
            <span className="ml-2">→</span>
          </span>
        </a>
      </div>
    </>
  );
}