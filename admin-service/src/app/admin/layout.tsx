import { getServerSession } from "next-auth"
import { authOptions } from "../../auth"
import { redirect } from "next/navigation"
import AdminNav from "@/components/AdminNav"

export default async function AdminLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session = await getServerSession(authOptions)

  if (!session) {
    redirect("/login")
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <AdminNav />
      <main className="p-6">{children}</main>
    </div>
  )
}
