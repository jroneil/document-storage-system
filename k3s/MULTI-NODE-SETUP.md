# K3s Multi-Node Cluster Setup (3 VMs on Proxmox)

You have a proper k3s cluster with 3 Linux VMs - this is the ideal setup for high availability!

## Your Setup

```
Proxmox Server
├── VM1 (k3s master node)
├── VM2 (k3s worker node)  
└── VM3 (k3s worker node)
```

Or if you have HA masters:
```
Proxmox Server
├── VM1 (k3s master)
├── VM2 (k3s master)  
└── VM3 (k3s master)
```

## Quick Start Guide

### Step 1: Find Your Master Node

SSH into each VM and check which is the master:

```bash
# Check if this node is a master
kubectl get nodes

# If you see nodes listed, this is a master!
```

Usually the first VM you set up k3s on is the master.

### Step 2: SSH to Master Node

```bash
# From your Windows machine
ssh root@<master-vm-ip>

# Or ssh into Proxmox first, then to the VM
ssh root@<proxmox-ip>
# Then find your VM
qm list
# SSH to the VM
```

### Step 3: Transfer Project Files

**Option A: Git (Recommended)**
```bash
# On the master node
cd /root
git clone https://github.com/your-repo/document-storage-system.git
cd document-storage-system/k3s
```

**Option B: SCP from Windows**
```bash
# From Windows PowerShell/CMD
cd C:\dms2Project
scp -r k3s root@<master-vm-ip>:/root/
```

**Option C: Via Proxmox**
```bash
# Copy to Proxmox first
scp -r k3s root@<proxmox-ip>:/root/

# SSH to Proxmox
ssh root@<proxmox-ip>

# Copy into the VM
scp -r /root/k3s root@<vm-ip>:/root/
```

### Step 4: Verify Your Cluster

On the master node:

```bash
# Check all nodes
kubectl get nodes

# You should see something like:
# NAME    STATUS   ROLES                  AGE   VERSION
# vm1     Ready    control-plane,master   10d   v1.27.3+k3s1
# vm2     Ready    <none>                 10d   v1.27.3+k3s1
# vm3     Ready    <none>                 10d   v1.27.3+k3s1

# Check cluster resources
kubectl top nodes
```

### Step 5: Update Configuration

```bash
cd /root/k3s

# Update secrets (IMPORTANT!)
nano base/secrets.yaml

# Set your Docker registry
export DOCKER_REGISTRY="docker.io/yourusername"
export IMAGE_TAG="v1.0.0"

# Update manifests
sed -i 's/YOUR_REGISTRY/'"$DOCKER_REGISTRY"'/g' base/microservices.yaml
sed -i 's/YOUR_REGISTRY/'"$DOCKER_REGISTRY"'/g' overlays/production/kustomization.yaml
sed -i 's/YOUR_REGISTRY/'"$DOCKER_REGISTRY"'/g' overlays/development/kustomization.yaml

# Update domain names
nano base/ingress.yaml
```

### Step 6: Build Images

You have two options for building Docker images:

**Option A: Build on Master Node** (if Docker is installed)
```bash
cd /root/k3s
chmod +x build-images.sh
./build-images.sh all
```

**Option B: Build on Windows** (recommended)
```powershell
# On your Windows machine with Docker Desktop
cd C:\dms2Project

# Build all images
docker-compose build

# Tag and push each service
docker tag api-gateway docker.io/yourusername/api-gateway:v1.0.0
docker push docker.io/yourusername/api-gateway:v1.0.0
# ... repeat for all services
```

### Step 7: Deploy to Cluster

On the master node:

```bash
cd /root/k3s
chmod +x deploy.sh

# Deploy to production
./deploy.sh production

# Or manually:
kubectl apply -f base/namespace.yaml
kubectl apply -f base/secrets.yaml
kubectl apply -f base/configmap.yaml
kubectl apply -k overlays/production/
```

### Step 8: Watch Deployment

```bash
# Watch pods being created
kubectl get pods -n document-storage -w

# Check which node each pod is on
kubectl get pods -n document-storage -o wide

# You should see pods distributed across all 3 nodes!
```

## Understanding Pod Distribution

With 3 nodes, Kubernetes will automatically distribute your pods:

```
VM1 (Master):
  - postgres-0
  - api-gateway-xxxxx-1
  - metadata-service-xxxxx-1

VM2 (Worker):
  - mongo-0
  - api-gateway-xxxxx-2
  - ingestion-service-xxxxx-1

VM3 (Worker):
  - rabbitmq-0
  - storage-service-xxxxx-1
  - search-service-xxxxx-1
```

This gives you:
- **High Availability**: If one node fails, services continue on others
- **Load Balancing**: Traffic is distributed across nodes
- **Resource Optimization**: Workload spread across all VMs

## Accessing Services

### From Within Proxmox Network

Add to your Windows `C:\Windows\System32\drivers\etc\hosts`:

```
<any-vm-ip> dms.yourdomain.com
<any-vm-ip> api.dms.yourdomain.com
<any-vm-ip> minio.dms.yourdomain.com
```

You can use ANY node's IP - k3s will route traffic correctly!

### Port Forwarding (For Testing)

```bash
# SSH to master node
ssh root@<master-vm-ip>

# Forward API Gateway to test
kubectl port-forward -n document-storage svc/api-gateway 8000:8000

# Access from Windows at: http://<master-vm-ip>:8000
```

## Common Commands

All commands run on the **master node**:

### Check Cluster Status
```bash
kubectl get nodes
kubectl top nodes
kubectl get pods -n document-storage -o wide
```

### View Logs
```bash
kubectl logs -n document-storage deployment/api-gateway
kubectl logs -n document-storage -l app=api-gateway --all-containers=true
```

### Scale Services
```bash
kubectl scale deployment/api-gateway --replicas=6 -n document-storage
# Pods will spread across all 3 nodes
```

### Restart Service
```bash
kubectl rollout restart deployment/api-gateway -n document-storage
```

### Check Resource Usage
```bash
kubectl top pods -n document-storage
kubectl describe node vm1
kubectl describe node vm2
kubectl describe node vm3
```

## Advanced: Control from Windows

If you want to run kubectl from your Windows machine:

### One-Time Setup:

1. **Install kubectl on Windows:**
   ```powershell
   choco install kubernetes-cli
   ```

2. **Get kubeconfig from master:**
   ```bash
   ssh root@<master-vm-ip>
   cat /etc/rancher/k3s/k3s.yaml
   ```

3. **Save to Windows:**
   ```powershell
   mkdir $env:USERPROFILE\.kube
   notepad $env:USERPROFILE\.kube\config
   ```
   
   Paste the content and change `127.0.0.1` to your master VM IP

4. **Test from Windows:**
   ```powershell
   kubectl get nodes
   # Should show all 3 nodes!
   ```

Now you can run kubectl commands from Windows PowerShell!

## Troubleshooting

### Pods stuck on one node

```bash
# Check node resources
kubectl describe nodes

# Check pod distribution
kubectl get pods -n document-storage -o wide

# If unbalanced, you may need to enable pod anti-affinity
# (already configured in production overlay)
```

### Can't access services

```bash
# Check if traefik ingress is running
kubectl get pods -n kube-system -l app.kubernetes.io/name=traefik

# Check ingress
kubectl get ingress -n document-storage
kubectl describe ingress dms-ingress -n document-storage
```

### Node down or not ready

```bash
# Check node status
kubectl get nodes

# Check what's wrong
kubectl describe node vm2

# SSH to the problematic node
ssh root@<vm2-ip>
sudo systemctl status k3s-agent
```

## Benefits of Your 3-Node Setup

✅ **High Availability**: Services survive node failures
✅ **Load Distribution**: Work spread across 3 VMs
✅ **Better Performance**: More resources available
✅ **Production Ready**: Proper cluster setup
✅ **Scalability**: Can add more nodes easily

## Next Steps

1. Deploy the application (follow steps above)
2. Monitor pod distribution: `kubectl get pods -n document-storage -o wide`
3. Test failover by shutting down a node
4. Set up monitoring with Prometheus/Grafana
5. Configure ingress with your actual domain/IP

Your 3-node k3s cluster is perfect for running this document storage system!
