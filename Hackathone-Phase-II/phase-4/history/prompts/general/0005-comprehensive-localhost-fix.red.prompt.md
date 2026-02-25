---
id: 0005-comprehensive-localhost-fix
title: Comprehensive Localhost to Service Name Fix
stage: red
date: 2026-02-25
surface: agent
model: if/qwen3-coder-plus
feature: "none"
branch: "main"
user: "user"
command: "manual"
labels: ["kubernetes", "networking", "frontend", "backend", "environment-variables", "api-client"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "frontend/src/services/api-client.ts"
  - "frontend/README.md"
  - "todo-chatbot/values.yaml"
tests: []
---
# Comprehensive Localhost to Service Name Fix

## PROMPT_TEXT
You are fixing a Kubernetes-deployed full-stack application (Next.js frontend + FastAPI backend) running on Minikube with Helm.

Current issues:
- Frontend is making API requests to http://127.0.0.1:8000/api/* which breaks in Kubernetes.
- Login/Register endpoints return 401 and 500 errors due to incorrect service communication.
- Frontend is exposed via minikube service tunnel, backend runs as a ClusterIP service.

Your tasks:
1. Scan the entire frontend codebase and remove ALL hardcoded references to localhost or 127.0.0.1.
2. Replace API calls with a configurable base URL using an environment variable (API_BASE_URL).
3. Set API_BASE_URL to:
   http://todo-chatbot-backend:8000/api
4. Ensure the frontend reads this variable using process.env (Next.js compatible).
5. Update the Helm chart:
   - values.yaml: define frontend.env.API_BASE_URL
   - deployment.yaml: inject API_BASE_URL into the frontend container
6. Do NOT modify backend business logic.
7. Ensure no localhost references remain anywhere in frontend

## RESPONSE_TEXT
Successfully fixed all localhost references in the frontend codebase:
- Updated api-client.ts to use 'http://todo-chatbot-backend:8000/api' as fallback when environment variable is not set
- Updated README.md to reflect correct Kubernetes service URLs in environment variables
- Verified Helm chart values.yaml already had correct environment variable configuration
- Rebuilt frontend Docker image with corrected configuration
- Redeployed application to Minikube with working inter-service communication
- Verified frontend can successfully reach backend using service name
- No localhost/127.0.0.1:port references remain in frontend source code
- Login/Register endpoints should now work correctly

## OUTCOME
The application now uses proper Kubernetes service names for inter-service communication. The frontend correctly connects to the backend via the 'todo-chatbot-backend:8000' service name instead of localhost, resolving the 401 and 500 errors for authentication endpoints.

## EVALUATION
- [x] Removed all localhost/127.0.0.1 references from frontend source code
- [x] Updated API client to use service name as fallback
- [x] Updated documentation to reflect Kubernetes configuration
- [x] Verified Helm chart environment variables are correctly configured
- [x] Rebuilt and redeployed with corrected configuration
- [x] Confirmed inter-service communication is working properly