import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            Document Management System
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Advanced metadata management with dynamic properties, branding, and user permissions
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">
              Metadata Editor Demo
            </h2>
            <p className="text-gray-600 text-center mb-8">
              Experience the comprehensive metadata editing interface with support for:
            </p>
            
            <div className="grid md:grid-cols-2 gap-8 mb-8">
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 font-bold">1</span>
                  </div>
                  <span className="text-gray-700">Document Header Information</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 font-bold">2</span>
                  </div>
                  <span className="text-gray-700">Standard Metadata (2-column layout)</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 font-bold">3</span>
                  </div>
                  <span className="text-gray-700">Branding Configuration</span>
                </div>
              </div>
              
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 font-bold">4</span>
                  </div>
                  <span className="text-gray-700">Dynamic Metadata Fields</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 font-bold">5</span>
                  </div>
                  <span className="text-gray-700">Edit/View Mode Toggle</span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 font-bold">6</span>
                  </div>
                  <span className="text-gray-700">User Permission Controls</span>
                </div>
              </div>
            </div>

            <div className="text-center">
              <Link 
                href="/metadata-edit"
                className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-8 rounded-lg transition-colors duration-200 text-lg"
              >
                Launch Metadata Editor
              </Link>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-3">Header Section</h3>
              <p className="text-gray-600">
                Document ID, title, publication date, status, file size, and other essential header information.
              </p>
            </div>
            
            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-3">Standard Properties</h3>
              <p className="text-gray-600">
                Organized in a clean 2-column layout with categories, tags, descriptions, and business metadata.
              </p>
            </div>
            
            <div className="bg-white rounded-xl shadow-md p-6">
              <h3 className="text-xl font-semibold text-gray-800 mb-3">Dynamic Metadata</h3>
              <p className="text-gray-600">
                User-defined custom fields, campaign data, geographic targeting, and brand-specific properties.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
