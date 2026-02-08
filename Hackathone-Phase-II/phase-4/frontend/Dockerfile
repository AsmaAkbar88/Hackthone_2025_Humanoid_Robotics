# Install dependencies only when needed
FROM node:20-alpine AS deps
WORKDIR /app

# Copy package.json and lockfile
COPY package*.json ./

# Install dependencies (both production and dev for building)
RUN npm ci

# Rebuild the source code only when needed
FROM node:20-alpine AS builder
WORKDIR /app

# Copy package.json and lockfile
COPY package*.json ./

# Copy installed dependencies from previous stage
COPY --from=deps /app/node_modules ./node_modules

# Copy source code
COPY . .

# Build the Next.js application
RUN npm run build

# Production image, copy all the files and run next
FROM node:20-alpine AS runner
WORKDIR /app

# Set production environment
ENV NODE_ENV=production

# Copy the built application and dependencies from builder stage
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next/standalone ./standalone
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/node_modules ./node_modules

# Expose port 3000
EXPOSE 3000

# Set the hostname to allow external connections
ENV HOSTNAME=0.0.0.0

# Start the application
CMD ["node", "standalone/server.js"]