import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Uses pages directory by default since src/pages exists
  env: {
    MAX_FILE_SIZE: process.env.MAX_FILE_SIZE,
    ALLOWED_FILE_TYPES: process.env.ALLOWED_FILE_TYPES,
    NEXT_PUBLIC_BULK_UPLOAD_SERVICE_URL: process.env.NEXT_PUBLIC_BULK_UPLOAD_SERVICE_URL,
  },
};

export default nextConfig;
