export default function AdminPage() {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm">
      <h1 className="text-2xl font-bold mb-6">Admin Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="p-6 bg-gray-50 rounded-lg">
          <h2 className="font-semibold mb-2">Users</h2>
          <p className="text-gray-600">Manage system users</p>
        </div>
        <div className="p-6 bg-gray-50 rounded-lg">
          <h2 className="font-semibold mb-2">Settings</h2>
          <p className="text-gray-600">Configure system settings</p>
        </div>
        <div className="p-6 bg-gray-50 rounded-lg">
          <h2 className="font-semibold mb-2">Analytics</h2>
          <p className="text-gray-600">View system usage statistics</p>
        </div>
      </div>
    </div>
  )
}
