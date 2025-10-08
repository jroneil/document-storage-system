# Document Storage System - K3s Deployment Guide

This guide provides comprehensive instructions for deploying the Document Storage System on a k3s cluster running on Proxmox.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Detailed Setup](#detailed-setup)
4. [Configuration](#configuration)
5. [Deployment](#deployment)
6. [Post-Deployment](#post-deployment)
7. [Monitoring](#monitoring)
8. [Troubleshooting](#troubleshooting)
9. [Scaling](#scaling)
10. [Backup and Recovery](#backup-and-recovery)

## Prerequisites

### Hardware Requirements

- **Minimum**: 4 CPU cores, 8GB RAM, 100GB storage
- **Recommended**: 8 CPU cores, 16GB RAM, 200GB+ storage
- Proxmox server with virtualization enabled

### Software Requirements

- k3s cluster (v1.25+)
- kubectl CLI tool
- Docker (for building images)
- Access to a Docker registry (Docker Hub, Harbor, etc.)

### k3s Installation on Proxmox

If you haven't installed k3s yet:

```bash
# On your Proxmox VM or LXC container
curl -sfL https://get.k3s.io | sh -

# Get the kubeconfig
sudo cat /etc/rancher/k3s/k3s.yaml > ~/.kube/config

# Verify installation
kubectl get nodes
```

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd dms2Project/k3s
```

### 2. Configure Environment

```bash
# Set your Docker registry
export DOCKER_REGISTRY="docker.io/yourusername"
export IMAGE_TAG="v1.0.0"

# Update secrets (IMPORTANT!)
nano base/secrets.yaml
```

### 3. Build and Push Images

```bash
# Make scripts executable
chmod +x build-images.sh deploy.sh

# Build all Docker images
./build-images.sh build

# Push to registry
./build-images.sh push
```

### 4. Update Configuration

```bash
# Update image registry in base/microservices.yaml
sed -i 's/YOUR_REGISTRY/docker.io\/yourusername/g' base/microservices.yaml

# Update domain names in base/ingress.yaml
nano base/ingress.yaml
```

### 5. Deploy

```bash
# Deploy to development
./deploy.sh development

# Or deploy to production
./deploy.sh production
```

## Detailed Setup

### 1. Configure Secrets

Edit `k3s/base/secrets.yaml` and update all passwords and credentials:

```yaml
# Database credentials
POSTGRES_PASSWORD: <strong-password>
MONGO_PASSWORD: <strong-password>

# RabbitMQ credentials
RABBITMQ_DEFAULT_PASS: <strong-password>

# MinIO credentials
MINIO_ROOT_PASSWORD: <strong-password>
```

**⚠️ WARNING**: Never commit production secrets to version control!

### 2. Configure Storage

The default configuration uses k3s local-path provisioner. For production, consider:

- **NFS Storage**: For shared storage across nodes
- **Longhorn**: For distributed block storage
- **Rook-Ceph**: For object, block, and file storage

To use NFS storage, update `k3s/base/persistent-volumes.yaml`:

```yaml
storageClassName: nfs-client  # instead of local-path
```

### 3. Configure Ingress

Update domain names in `k3s/base/ingress.yaml`:

```yaml
spec:
  rules:
  - host: dms.yourdomain.com  # Your domain
```

For local development, update `/etc/hosts`:

```bash
<k3s-node-ip> dms.yourdomain.com
<k3s-node-ip> api.dms.yourdomain.com
<k3s-node-ip> minio.dms.yourdomain.com
```

### 4. SSL/TLS Configuration

The ingress is configured to use cert-manager for automatic SSL certificates.

Install cert-manager:

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

Create a ClusterIssuer:

```bash
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: traefik
EOF
```

## Configuration

### Environment-Specific Configurations

#### Development

- Single replica for most services
- Latest image tags
- Debug mode enabled
- Lower resource limits

#### Production

- Multiple replicas (3+ for high availability)
- Versioned image tags
- Debug mode disabled
- Higher resource limits

### Resource Allocation

Current resource allocation per service:

| Service | Replicas (Dev) | Replicas (Prod) | Memory Request | Memory Limit | CPU Request | CPU Limit |
|---------|----------------|-----------------|----------------|--------------|-------------|-----------|
| API Gateway | 2 | 3 | 256Mi | 512Mi | 250m | 500m |
| Ingestion | 2 | 3 | 256Mi | 512Mi | 250m | 500m |
| Metadata | 2 | 3 | 256Mi | 512Mi | 250m | 500m |
| Storage | 2 | 3 | 256Mi | 512Mi | 250m | 500m |
| Processing | 2 | 3 | 512Mi | 1Gi | 500m | 1000m |
| Search | 2 | 3 | 256Mi | 512Mi | 250m | 500m |
| AI Service | 1 | 2 | 512Mi | 2Gi | 500m | 2000m |
| Notification | 2 | 3 | 128Mi | 256Mi | 100m | 250m |

## Deployment

### Initial Deployment

```bash
# Navigate to k3s directory
cd k3s

# Deploy infrastructure first
kubectl apply -f base/namespace.yaml
kubectl apply -f base/secrets.yaml
kubectl apply -f base/configmap.yaml
kubectl apply -f base/persistent-volumes.yaml

# Deploy databases and message queue
kubectl apply -f base/postgres.yaml
kubectl apply -f base/mongodb.yaml
kubectl apply -f base/rabbitmq.yaml
kubectl apply -f base/minio.yaml
kubectl apply -f base/elasticsearch.yaml

# Wait for infrastructure to be ready
kubectl wait --for=condition=ready pod -l app=postgres -n document-storage --timeout=300s
kubectl wait --for=condition=ready pod -l app=mongo -n document-storage --timeout=300s
kubectl wait --for=condition=ready pod -l app=rabbitmq -n document-storage --timeout=300s
kubectl wait --for=condition=ready pod -l app=elasticsearch -n document-storage --timeout=300s

# Deploy microservices
kubectl apply -k overlays/production/

# Deploy ingress
kubectl apply -f base/ingress.yaml
```

### Using Deployment Script

```bash
# Make script executable
chmod +x deploy.sh

# Deploy to development
./deploy.sh development

# Deploy to production
./deploy.sh production
```

### Rolling Updates

```bash
# Update image tags in kustomization.yaml
# Then apply changes
kubectl apply -k overlays/production/

# Or update specific service
kubectl set image deployment/api-gateway api-gateway=your-registry/api-gateway:v1.1.0 -n document-storage

# Monitor rollout
kubectl rollout status deployment/api-gateway -n document-storage
```

### Rollback

```bash
# Rollback to previous version
kubectl rollout undo deployment/api-gateway -n document-storage

# Rollback to specific revision
kubectl rollout undo deployment/api-gateway --to-revision=2 -n document-storage
```

## Post-Deployment

### 1. Initialize MinIO

Create the documents bucket:

```bash
# Get MinIO pod
kubectl get pods -n document-storage -l app=minio

# Port forward to MinIO console
kubectl port-forward -n document-storage svc/minio 9001:9001

# Access console at http://localhost:9001
# Username: minioadmin
# Password: (from secrets.yaml)

# Create bucket named "documents"
```

### 2. Initialize Databases

PostgreSQL and MongoDB will auto-initialize with the configured databases.

### 3. Verify Services

```bash
# Check all pods are running
kubectl get pods -n document-storage

# Check services
kubectl get svc -n document-storage

# Check ingress
kubectl get ingress -n document-storage

# View logs
kubectl logs -n document-storage deployment/api-gateway
```

### 4. Access Applications

- Web UI: `http://dms.yourdomain.com`
- API: `http://api.dms.yourdomain.com`
- MinIO Console: `http://minio.dms.yourdomain.com`
- RabbitMQ Management: `http://rabbitmq.dms.yourdomain.com`
- MailHog: `http://mailhog.dms.yourdomain.com`

## Monitoring

### Basic Monitoring

```bash
# Watch pods
kubectl get pods -n document-storage -w

# View resource usage
kubectl top nodes
kubectl top pods -n document-storage

# View events
kubectl get events -n document-storage --sort-by='.lastTimestamp'
```

### Logs

```bash
# View logs for a service
kubectl logs -n document-storage deployment/api-gateway

# Follow logs
kubectl logs -n document-storage deployment/api-gateway -f

# View logs from all replicas
kubectl logs -n document-storage -l app=api-gateway

# View logs with timestamps
kubectl logs -n document-storage deployment/api-gateway --timestamps
```

### Installing Prometheus & Grafana (Optional)

```bash
# Add helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install kube-prometheus-stack
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace

# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Default credentials: admin/prom-operator
```

## Troubleshooting

### Common Issues

#### 1. Pods Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n document-storage

# Common causes:
# - Image pull errors: Check registry credentials
# - Resource constraints: Check node resources
# - Volume mount errors: Check PVC status
```

#### 2. Database Connection Issues

```bash
# Check database pods
kubectl logs -n document-storage statefulset/postgres
kubectl logs -n document-storage statefulset/mongo

# Test connectivity from a service pod
kubectl exec -it -n document-storage deployment/metadata-service -- sh
# Then: ping postgres, ping mongo
```

#### 3. Service Not Accessible

```bash
# Check service endpoints
kubectl get endpoints -n document-storage

# Check ingress
kubectl describe ingress -n document-storage dms-ingress

# Check traefik logs (k3s default ingress controller)
kubectl logs -n kube-system deployment/traefik
```

#### 4. Persistent Volume Issues

```bash
# Check PVC status
kubectl get pvc -n document-storage

# Check PV status
kubectl get pv

# If using local-path, check node storage
df -h
```

### Debug Mode

Enable debug logging for a service:

```bash
kubectl set env deployment/api-gateway DEBUG=true -n document-storage
```

### Port Forwarding for Local Access

```bash
# Forward API Gateway
kubectl port-forward -n document-storage svc/api-gateway 8000:8000

# Forward PostgreSQL
kubectl port-forward -n document-storage svc/postgres 5432:5432

# Forward MongoDB
kubectl port-forward -n document-storage svc/mongo 27017:27017
```

## Scaling

### Manual Scaling

```bash
# Scale a deployment
kubectl scale deployment/api-gateway --replicas=5 -n document-storage

# Scale all at once
kubectl scale deployment --all --replicas=3 -n document-storage
```

### Horizontal Pod Autoscaling

```bash
# Create HPA
kubectl autoscale deployment api-gateway \
  --min=2 --max=10 \
  --cpu-percent=80 \
  -n document-storage

# View HPA status
kubectl get hpa -n document-storage
```

### Resource Limits

Update resource limits in production overlay:

```yaml
# k3s/overlays/production/resource-patch.yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

## Backup and Recovery

### Database Backups

#### PostgreSQL

```bash
# Create backup
kubectl exec -n document-storage statefulset/postgres -- \
  pg_dump -U admin document_storage > backup.sql

# Restore backup
kubectl exec -i -n document-storage statefulset/postgres -- \
  psql -U admin document_storage < backup.sql
```

#### MongoDB

```bash
# Create backup
kubectl exec -n document-storage statefulset/mongo -- \
  mongodump --username admin --password <password> --out /tmp/backup

# Copy backup
kubectl cp document-storage/mongo-0:/tmp/backup ./mongo-backup

# Restore backup
kubectl cp ./mongo-backup document-storage/mongo-0:/tmp/restore
kubectl exec -n document-storage statefulset/mongo -- \
  mongorestore --username admin --password <password> /tmp/restore
```

### Volume Backups

```bash
# Using Velero for backup
velero backup create dms-backup --include-namespaces document-storage

# Restore
velero restore create --from-backup dms-backup
```

## Maintenance

### Updates

1. Update image tags in overlays
2. Apply changes: `kubectl apply -k overlays/production/`
3. Monitor rollout: `kubectl rollout status deployment/<name> -n document-storage`

### Cleanup

```bash
# Delete all resources
kubectl delete namespace document-storage

# Or use kustomize
kubectl delete -k overlays/production/
```

## Support

For issues or questions:
- Check logs: `kubectl logs -n document-storage deployment/<service-name>`
- View events: `kubectl get events -n document-storage`
- Create an issue in the repository

## License

[Your License Here]
