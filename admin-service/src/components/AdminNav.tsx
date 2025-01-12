"use client"

import Link from "next/link"
import { signOut } from "next-auth/react"

export default function AdminNav() {
  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/admin" className="text-lg font-bold">
              Admin Dashboard
            </Link>
          </div>
          <div className="flex items-center">
            <button
              onClick={() => signOut()}
              className="text-gray-500 hover:text-gray-700"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
