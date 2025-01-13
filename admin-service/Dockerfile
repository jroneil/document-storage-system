# Stage 1: Dependencies
FROM node:23-alpine3.20 AS deps
WORKDIR /app

# Copy package files (package.json and package-lock.json)
COPY package.json package-lock.json ./

# Install dependencies using npm ci (which installs exactly what is in package-lock.json)
RUN npm ci

# Stage 2: Builder
FROM node:23-alpine3.20 AS builder
WORKDIR /app

# Copy installed node_modules from the deps stage
COPY --from=deps /app/node_modules ./node_modules

# Copy the rest of the application files
COPY . .

# Build the application (runs `next build`)
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# Stage 3: Runner
FROM node:23-alpine3.20 AS runner
WORKDIR /app

# Set environment variables for production
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

# Create a non-root user for security
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy necessary files from the builder stage
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./.next/standalone
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# Switch to the non-root user for running the app
USER nextjs

# Expose the port the app will run on
EXPOSE 3000

# Set environment variables for port and hostname
ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# Start the app using the server.js
CMD ["node", "server.js"]
