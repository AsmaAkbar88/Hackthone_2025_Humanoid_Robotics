# Use Node 20 as base image
FROM node:20-alpine

# Set environment variables (these will be available at build time)
ENV NODE_ENV=production
ENV NEXT_PUBLIC_API_BASE_URL=http://todo-chatbot-backend:8000/api
ENV NEXT_PUBLIC_BACKEND_URL=http://todo-chatbot-backend:8000

# Set work directory
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache libc6-compat python3 make g++

# Copy package files first to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the Next.js application
RUN npm run build

# Expose port
EXPOSE 3000

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Change ownership of the app directory
RUN chown -R nextjs:nodejs /app
USER nextjs

# Run the application
CMD ["npm", "start"]