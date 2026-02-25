#!/bin/bash

# This script manually deploys the Todo AI Chatbot using kubectl from Helm templates
# It simulates what Helm would do when installing the chart

# Create a temporary directory for rendered templates
mkdir -p temp-manifests

# Render the templates by replacing the Helm template variables manually
# We'll create a basic version with our default values

# Create the Secret first
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: todo-backend-secrets
  namespace: default
type: Opaque
data:
  openai_api_key: TlVMTF9PUEVOSUdfQVBJX0tFWQ==
EOF

# Create the ServiceAccount
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: todo-chatbot
  namespace: default
automountServiceAccountToken: true
EOF

# Create the Backend Deployment
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-chatbot-backend
  namespace: default
  labels:
    app: todo-chatbot-backend
    helm.sh/chart: todo-chatbot-1.0.0
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 1
  selector:
    matchLabels:
      app: todo-chatbot-backend
      app.kubernetes.io/name: todo-chatbot
      app.kubernetes.io/instance: todo-chatbot
  template:
    metadata:
      labels:
        app: todo-chatbot-backend
        app.kubernetes.io/name: todo-chatbot
        app.kubernetes.io/instance: todo-chatbot
    spec:
      serviceAccountName: todo-chatbot
      containers:
        - name: backend
          image: todo-backend:latest
          imagePullPolicy: Never
          ports:
            - name: http
              containerPort: 8000
              protocol: TCP
          env:
            - name: DATABASE_URL
              value: "postgresql://neondb_owner:npg_ZHpDlAIVvQ67@ep-late-star-aip8khsg-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require"
            - name: ASYNC_DATABASE_URL
              value: "postgresql+asyncpg://neondb_owner:npg_ZHpDlAIVvQ67@ep-late-star-aip8khsg-pooler.c-4.us-east-1.aws.neon.tech/neondb?ssl=true"
            - name: SECRET_KEY
              value: "your-super-secret-jwt-key-change-in-production"
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: todo-backend-secrets
                  key: openai_api_key
            - name: DEBUG
              value: "false"
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 10
            periodSeconds: 15
            timeoutSeconds: 2
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 5
            periodSeconds: 15
            timeoutSeconds: 2
            failureThreshold: 3
EOF

# Create the Frontend Deployment
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-chatbot-frontend
  namespace: default
  labels:
    app: todo-chatbot-frontend
    helm.sh/chart: todo-chatbot-1.0.0
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 1
  selector:
    matchLabels:
      app: todo-chatbot-frontend
      app.kubernetes.io/name: todo-chatbot
      app.kubernetes.io/instance: todo-chatbot
  template:
    metadata:
      labels:
        app: todo-chatbot-frontend
        app.kubernetes.io/name: todo-chatbot
        app.kubernetes.io/instance: todo-chatbot
    spec:
      serviceAccountName: todo-chatbot
      containers:
        - name: frontend
          image: todo-frontend:latest
          imagePullPolicy: Never
          ports:
            - name: http
              containerPort: 3000
              protocol: TCP
          env:
            - name: NEXT_PUBLIC_API_BASE_URL
              value: "http://todo-chatbot-backend:8000/api"
            - name: NEXT_PUBLIC_BACKEND_URL
              value: "http://todo-chatbot-backend:8000"
          livenessProbe:
            httpGet:
              path: /
              port: http
          readinessProbe:
            httpGet:
              path: /
              port: http
EOF

# Create the Backend Service
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: todo-chatbot-backend
  namespace: default
  labels:
    app: todo-chatbot-backend
    helm.sh/chart: todo-chatbot-1.0.0
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
spec:
  type: ClusterIP
  ports:
    - port: 8000
      targetPort: http
      protocol: TCP
      name: http
  selector:
    app: todo-chatbot-backend
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
EOF

# Create the Frontend Service
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: todo-chatbot-frontend
  namespace: default
  labels:
    app: todo-chatbot-frontend
    helm.sh/chart: todo-chatbot-1.0.0
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
spec:
  type: ClusterIP
  ports:
    - port: 3000
      targetPort: http
      protocol: TCP
      name: http
  selector:
    app: todo-chatbot-frontend
    app.kubernetes.io/name: todo-chatbot
    app.kubernetes.io/instance: todo-chatbot
EOF

echo "Todo AI Chatbot deployed successfully!"
echo "Backend service: todo-chatbot-backend:8000"
echo "Frontend service: todo-chatbot-frontend:3000"

# Show deployment status
kubectl get deployments
kubectl get services
kubectl get pods