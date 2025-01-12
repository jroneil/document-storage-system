import { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import { apiClient } from "@/lib/apiClient";

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      name?: string | null;
      email?: string | null;
      image?: string | null;
    };
  }
}

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        try {
          const response = await apiClient.post("/auth/login", {
            email: credentials?.email,
            password: credentials?.password
          });
          
          if (response.data) {
            return response.data;
          }
          return null;
        } catch (error) {
          console.error("Login error:", error);
          return null;
        }
      }
    })
  ],
  callbacks: {
    async session({ session, token }) {
      if (token) {
        session.user = {
          id: token.sub || "",
          name: token.name,
          email: token.email,
          image: token.picture
        };
      }
      return session;
    },
    async jwt({ token, user }) {
      if (user) {
        token.sub = user.id;
        token.name = user.name;
        token.email = user.email;
        token.picture = user.image;
      }
      return token;
    }
  },
  pages: {
    signIn: "/login"
  },
  session: {
    strategy: "jwt"
  }
};
