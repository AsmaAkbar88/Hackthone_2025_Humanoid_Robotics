# Todo AI Chatbot Helm Chart

A Helm chart for deploying the Todo AI Chatbot application with frontend (Next.js) and backend (FastAPI) services.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- Docker images `todo-frontend:latest` and `todo-backend:latest` available in your cluster

## Parameters

### Frontend Parameters

| Name                            | Description                                                 | Value              |
| ------------------------------- | ----------------------------------------------------------- | ------------------ |
| `frontend.enabled`              | Enable frontend deployment                                  | `true`             |
| `frontend.replicaCount`         | Number of frontend pods                                     | `1`                |
| `frontend.image.repository`     | Frontend image repository                                   | `todo-frontend`    |
| `frontend.image.pullPolicy`     | Frontend image pull policy                                  | `Never`            |
| `frontend.image.tag`            | Frontend image tag                                          | `latest`           |
| `frontend.service.type`         | Frontend service type                                       | `ClusterIP`        |
| `frontend.service.port`         | Frontend service port                                       | `3000`             |
| `frontend.service.targetPort`   | Frontend target port                                        | `3000`             |

### Backend Parameters

| Name                            | Description                                                 | Value              |
| ------------------------------- | ----------------------------------------------------------- | ------------------ |
| `backend.enabled`               | Enable backend deployment                                   | `true`             |
| `backend.replicaCount`          | Number of backend pods                                      | `1`                |
| `backend.image.repository`      | Backend image repository                                    | `todo-backend`     |
| `backend.image.pullPolicy`      | Backend image pull policy                                   | `Never`            |
| `backend.image.tag`             | Backend image tag                                           | `latest`           |
| `backend.service.type`          | Backend service type                                        | `ClusterIP`        |
| `backend.service.port`          | Backend service port                                        | `8000`             |
| `backend.service.targetPort`    | Backend target port                                         | `8000`             |

### Global Parameters

| Name                      | Description                                                | Value              |
| ------------------------- | ---------------------------------------------------------- | ------------------ |
| `nameOverride`            | String to partially override todo-chatbot.fullname       | `""`               |
| `fullnameOverride`        | String to fully override todo-chatbot.fullname           | `""`               |
| `serviceAccount.create`   | Create service account                                     | `true`             |
| `serviceAccount.name`     | Service account name to use                                | `""`               |

## Installing the Chart

To install the chart with the release name `todo-chatbot`:

```bash
# First, ensure your Docker images are available in the cluster
# For Minikube:
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# For other clusters, push your images to a registry and update the values

# Install the chart
helm install todo-chatbot . --values values.yaml
```

## Upgrading the Chart

```bash
helm upgrade todo-chatbot . --values values.yaml
```

## Uninstalling the Chart

```bash
helm uninstall todo-chatbot
```

## Configuration Examples

### Local Development (Minikube)

For local development with Minikube, the default values are already configured to use local images:

```bash
# Build Docker images locally
docker build -t todo-frontend:latest ./frontend
docker build -t todo-backend:latest ./backend

# Load images into Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# Install the chart
helm install todo-chatbot .
```

### Production Deployment

For production, you would typically update the values.yaml to use your image registry:

```yaml
frontend:
  image:
    repository: your-registry/todo-frontend
    pullPolicy: Always
    tag: "v1.0.0"

backend:
  image:
    repository: your-registry/todo-backend
    pullPolicy: Always
    tag: "v1.0.0"
```

## Service Architecture

The chart deploys:

- **Frontend Service**: Next.js application serving the UI
- **Backend Service**: FastAPI application with MCP server and AI integration
- **Ingress Configuration**: Routes frontend traffic to the Next.js app and API traffic to the backend
- **Secrets**: Manages sensitive data like API keys

## Accessing the Application

### Using Port Forwarding

```bash
# Access frontend
kubectl port-forward svc/todo-chatbot-frontend 3000:3000

# Access backend
kubectl port-forward svc/todo-chatbot-backend 8000:8000
```

### Using Ingress

If ingress is enabled, you can access the application through the configured hostnames.

## Environment Variables

The chart configures important environment variables:

- Frontend connects to backend via `http://backend-service:8000`
- Backend is configured with database URLs and API keys

## Secrets Management

The chart creates a secret `todo-backend-secrets` that holds sensitive information like the OpenAI API key. Update the `openaiApiKey` in values.yaml with your actual base64-encoded API key for production use.

## Troubleshooting

1. **Images not found**: Ensure your Docker images are available in the Kubernetes cluster
2. **Networking issues**: Check that services can communicate with each other by name
3. **API errors**: Verify that the frontend is correctly configured with the backend service URL

For more information on accessing and managing your Todo AI Chatbot deployment, run:

```bash
helm status todo-chatbot
```