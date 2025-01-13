import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone',
  experimental: {
    // Enable if needed for middleware
    // serverActions: true,
  },
  eslint: {
    // Disable ESLint during production build
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
