# K3s Quick Start Guide

This is a quick reference guide for deploying the Document Storage System on k3s.

## Prerequisites Checklist

- [ ] k3s cluster running on Proxmox
- [ ] kubectl installed and configured
- [ ] Docker installed (for building images)
- [ ] Docker registry account (Docker Hub, Harbor, etc.)

## Step-by-Step Deployment

### 1. Update Secrets (CRITICAL!)

```bash
cd k3s
nano base/secrets.yaml
```

**Update these passwords:**
- POSTGRES_PASSWORD
- MONGO_PASSWORD
- RABBITMQ_DEFAULT_PASS
- MINIO_ROOT_PASSWORD

### 2. Configure Docker Registry

```bash
# Set your registry
export DOCKER_REGISTRY="docker.io/yourusername"
export IMAGE_TAG="v1.0.0"

# Update manifests
sed -i 's/YOUR_REGISTRY/'"$DOCKER_REGISTRY"'/g' base/microservices.yaml
sed -i 's/YOUR_REGISTRY/'"$DOCKER_REGISTRY"'/g' overlays/production/kustomization.yaml
sed -i 's/YOUR_REGISTRY/'"$DOCKER_REGISTRY"'/g' overlays/development/kustomization.yaml
```

### 3. Update Domain Names

```bash
nano base/ingress.yaml
```

Replace `yourdomain.com` with your actual domain.

For local testing, add to `/etc/hosts`:
```
<k3s-node-ip> dms.yourdomain.com
<k3s-node-ip> api.dms.yourdomain.com
<k3s-node-ip> minio.dms.yourdomain.com
```

### 4. Build Docker Images

```bash
# Build all images
./build-images.sh build

# Push to registry
./build-images.sh push

# Or do both
./build-images.sh all
```

### 5. Deploy to k3s

**For Development:**
```bash
./deploy.sh development
```

**For Production:**
```bash
./deploy.sh production
```

### 6. Verify Deployment

```bash
# Check pods
kubectl get pods -n document-storage

# Check services
kubectl get svc -n document-storage

# Check ingress
kubectl get ingress -n document-storage

# View logs
kubectl logs -n document-storage -l app=api-gateway
```

### 7. Initialize MinIO

```bash
# Port forward to MinIO console
kubectl port-forward -n document-storage svc/minio 9001:9001

# Access at http://localhost:9001
# Login: minioadmin / (your password from secrets)
# Create bucket: "documents"
```

## Access Your Services

- **Web UI**: http://dms.yourdomain.com
- **API**: http://api.dms.yourdomain.com
- **MinIO**: http://minio.dms.yourdomain.com
- **RabbitMQ**: http://rabbitmq.dms.yourdomain.com

## Common Commands

### View Logs
```bash
kubectl logs -n document-storage deployment/api-gateway -f
```

### Scale Service
```bash
kubectl scale deployment/api-gateway --replicas=5 -n document-storage
```

### Restart Service
```bash
kubectl rollout restart deployment/api-gateway -n document-storage
```

### Update Service Image
```bash
kubectl set image deployment/api-gateway api-gateway=registry/api-gateway:v1.1.0 -n document-storage
```

### Port Forward for Local Access
```bash
# API Gateway
kubectl port-forward -n document-storage svc/api-gateway 8000:8000

# PostgreSQL
kubectl port-forward -n document-storage svc/postgres 5432:5432

# MongoDB
kubectl port-forward -n document-storage svc/mongo 27017:27017
```

## Troubleshooting

### Pods Not Starting?
```bash
kubectl describe pod <pod-name> -n document-storage
```

### Can't Pull Images?
```bash
# Check if images exist in registry
docker pull $DOCKER_REGISTRY/api-gateway:$IMAGE_TAG

# Create image pull secret if needed
kubectl create secret docker-registry regcred \
  --docker-server=$DOCKER_REGISTRY \
  --docker-username=<your-username> \
  --docker-password=<your-password> \
  -n document-storage
```

### Database Connection Issues?
```bash
# Check if databases are ready
kubectl get pods -n document-storage -l app=postgres
kubectl get pods -n document-storage -l app=mongo

# Check logs
kubectl logs -n document-storage statefulset/postgres
kubectl logs -n document-storage statefulset/mongo
```

### Service Not Accessible?
```bash
# Check endpoints
kubectl get endpoints -n document-storage

# Check ingress
kubectl describe ingress -n document-storage dms-ingress
```

## Clean Up

```bash
# Delete everything
kubectl delete namespace document-storage

# Or use kustomize
kubectl delete -k overlays/production/
```

## Next Steps

- Set up SSL certificates with cert-manager
- Configure monitoring with Prometheus/Grafana
- Set up automated backups
- Configure horizontal pod autoscaling

For detailed information, see [README.md](README.md)
