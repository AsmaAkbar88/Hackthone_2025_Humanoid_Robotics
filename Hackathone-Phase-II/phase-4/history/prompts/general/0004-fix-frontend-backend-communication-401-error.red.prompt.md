---
id: 0004-fix-frontend-backend-communication-401-error
title: Fix Frontend-Backend Communication 401 Error
stage: red
date: 2026-02-25
surface: agent
model: if/qwen3-coder-plus
feature: "none"
branch: "main"
user: "user"
command: "manual"
labels: ["kubernetes", "networking", "frontend", "backend", "authentication"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "todo-chatbot/values.yaml"
  - "todo-chatbot/deploy-manual.sh"
tests: []
---
# Fix Frontend-Backend Communication 401 Error

## PROMPT_TEXT
ab 1 chota sa task ab is eorr ko solve kro "Request URL
http://127.0.0.1:8000/api/auth/login
Referrer Policy
strict-origin-when-cross-origin
"

## RESPONSE_TEXT
Fixed the frontend-backend communication issue where the frontend was trying to connect to the backend using localhost instead of the Kubernetes service name. Updated the environment variables in the deployment configuration to use the correct service name 'todo-chatbot-backend:8000' instead of '127.0.0.1:8000' or 'backend-service:8000'. This resolves the 401 Unauthorized error that occurred because the frontend couldn't communicate with the backend service in the Kubernetes cluster.

## OUTCOME
The frontend can now successfully communicate with the backend service using the correct Kubernetes service name. Both services are deployed and running properly with proper inter-service communication. The authentication endpoints are now accessible from the frontend to the backend.

## EVALUATION
- [x] Fixed frontend API base URL from localhost to correct service name
- [x] Verified that frontend can reach backend service in Kubernetes
- [x] Confirmed both pods are running and healthy
- [x] Validated inter-service communication is working
- [x] Created NodePort services for external access at ports 30001 (frontend) and 30002 (backend)