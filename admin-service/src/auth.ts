import { NextAuthOptions } from "next-auth"
import { apiClient } from "@/lib/apiClient"
import GoogleProvider from "next-auth/providers/google"

export const authOptions: NextAuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  callbacks: {
    async signIn({ user }) {
      // Save/update user in metadata service
      try {
        await apiClient.post('/api/user-preferences', {
          email: user.email,
          name: user.name,
          image: user.image
        })
        return true
      } catch (error) {
        console.error('Failed to save user preferences:', error)
        return false
      }
    },
    async session({ session }) {
      // Get user preferences from metadata service
      try {
        const { data } = await apiClient.get('/api/user-preferences', {
          params: { email: session.user?.email }
        })
        session.user = {
          ...session.user,
          ...data
        }
      } catch (error) {
        console.error('Failed to fetch user preferences:', error)
      }
      return session
    }
  },
  secret: process.env.NEXTAUTH_SECRET,
}
