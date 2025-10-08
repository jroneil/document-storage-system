# Remote K3s Setup Guide

This guide explains how to deploy to your k3s cluster running on a Proxmox server from your local Windows machine.

## Two Main Approaches

### Option 1: Work Directly on Proxmox Server (Recommended for Beginners)
### Option 2: Work from Your Local Machine (Recommended for Developers)

---

## Option 1: Work Directly on Proxmox Server

This is the simplest approach - you'll SSH into your Proxmox server and work from there.

### Step 1: Access Your Proxmox Server

**Using SSH:**
```bash
# From Windows Command Prompt or PowerShell
ssh root@<proxmox-server-ip>

# Or if you have a non-root user
ssh username@<proxmox-server-ip>
```

**Using Proxmox Web UI:**
1. Open browser: `https://<proxmox-server-ip>:8006`
2. Login to Proxmox
3. Select your k3s VM/Container
4. Click "Console" button

### Step 2: Transfer Project Files to Proxmox

**Method A: Using Git (Recommended)**
```bash
# On your Proxmox server/VM
git clone https://github.com/your-repo/document-storage-system.git
cd document-storage-system/k3s
```

**Method B: Using SCP from Windows**
```bash
# From your Windows machine (in Command Prompt)
cd C:\dms2Project
scp -r k3s username@<proxmox-server-ip>:/home/username/
```

**Method C: Using WinSCP (GUI)**
1. Download WinSCP: https://winscp.net/
2. Connect to your Proxmox server
3. Drag and drop the `k3s` folder to the server

### Step 3: Deploy from Proxmox Server

Once you're SSH'd into the server:

```bash
# Navigate to the k3s directory
cd /path/to/k3s

# Make scripts executable
chmod +x deploy.sh build-images.sh

# Update secrets
nano base/secrets.yaml

# Set environment variables
export DOCKER_REGISTRY="docker.io/yourusername"
export IMAGE_TAG="v1.0.0"

# Update registry in manifests
sed -i 's/YOUR_REGISTRY/'"$DOCKER_REGISTRY"'/g' base/microservices.yaml
sed -i 's/YOUR_REGISTRY/'"$DOCKER_REGISTRY"'/g' overlays/production/kustomization.yaml
sed -i 's/YOUR_REGISTRY/'"$DOCKER_REGISTRY"'/g' overlays/development/kustomization.yaml

# Build images (if Docker is installed)
./build-images.sh all

# Deploy
./deploy.sh production
```

---

## Option 2: Work from Your Local Windows Machine

This allows you to manage k3s from your Windows PC while the cluster runs on Proxmox.

### Step 1: Install Required Tools on Windows

**Install kubectl:**
```powershell
# Using Chocolatey
choco install kubernetes-cli

# Or download from: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
```

**Install Docker Desktop (for building images):**
- Download from: https://www.docker.com/products/docker-desktop/

### Step 2: Get kubeconfig from k3s Server

**On your Proxmox server/k3s node:**
```bash
# Copy the k3s config
sudo cat /etc/rancher/k3s/k3s.yaml
```

**On your Windows machine:**

1. Create kubectl config directory:
```powershell
mkdir $env:USERPROFILE\.kube
```

2. Create/Edit config file:
```powershell
notepad $env:USERPROFILE\.kube\config
```

3. Paste the content from k3s.yaml, BUT **change the server IP**:
```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: ...
    server: https://127.0.0.1:6443  # Change this!
  name: default
# Change 127.0.0.1 to your Proxmox server's IP address
# Example: https://192.168.1.100:6443
```

4. Save and test:
```powershell
kubectl get nodes
```

### Step 3: Build Images on Windows

```powershell
# In PowerShell, navigate to your project
cd C:\dms2Project

# Set environment variables
$env:DOCKER_REGISTRY = "docker.io/yourusername"
$env:IMAGE_TAG = "v1.0.0"

# Build images using Docker Desktop
docker-compose build

# Tag and push images
docker tag api-gateway $env:DOCKER_REGISTRY/api-gateway:$env:IMAGE_TAG
docker push $env:DOCKER_REGISTRY/api-gateway:$env:IMAGE_TAG
# Repeat for each service...
```

### Step 4: Deploy from Windows

```powershell
cd C:\dms2Project\k3s

# Update secrets (use any text editor)
notepad base\secrets.yaml

# Update registry references
# (Do this manually in each file or use PowerShell):
(Get-Content base\microservices.yaml) -replace 'YOUR_REGISTRY', $env:DOCKER_REGISTRY | Set-Content base\microservices.yaml

# Deploy using kubectl
kubectl apply -f base/namespace.yaml
kubectl apply -f base/secrets.yaml
kubectl apply -f base/configmap.yaml
kubectl apply -k overlays/production/
```

---

## Recommended Workflow for Your Setup

Since you have:
- Windows development machine
- Separate Proxmox server with k3s

**Best Practice:**

1. **Develop on Windows** (this machine)
2. **Build images on Windows** using Docker Desktop
3. **Push images to Docker Hub** (or your registry)
4. **Deploy to k3s** using kubectl from Windows

### Quick Setup Steps:

#### On Windows (One-time setup):

1. **Install kubectl:**
```powershell
choco install kubernetes-cli
```

2. **Get kubeconfig from Proxmox:**
```bash
# SSH to Proxmox
ssh root@<proxmox-ip>
sudo cat /etc/rancher/k3s/k3s.yaml
```

3. **Configure kubectl on Windows:**
```powershell
mkdir $env:USERPROFILE\.kube
notepad $env:USERPROFILE\.kube\config
# Paste content and change 127.0.0.1 to Proxmox IP
```

4. **Verify connection:**
```powershell
kubectl get nodes
```

#### For Each Deployment:

```powershell
# 1. Build images locally
cd C:\dms2Project
docker-compose build

# 2. Push to registry
docker push yourusername/api-gateway:latest
# ... for each service

# 3. Deploy to k3s
cd k3s
kubectl apply -k overlays/production/

# 4. Check status
kubectl get pods -n document-storage
```

---

## Alternative: Use GitHub Actions / CI/CD

Create a GitHub Actions workflow that:
1. Builds images when you push code
2. Pushes to Docker registry
3. Deploys to your k3s cluster

This is the most automated approach!

---

## Troubleshooting

### Can't connect to k3s cluster

```powershell
# Check if kubectl is configured
kubectl config view

# Test connection
kubectl cluster-info

# Check if k3s is running on Proxmox
ssh root@<proxmox-ip> "sudo systemctl status k3s"
```

### Port 6443 not accessible

```bash
# On Proxmox, ensure k3s API is exposed
sudo systemctl status k3s

# Check firewall
sudo ufw status
sudo ufw allow 6443/tcp
```

### Need to expose k3s API to external network

```bash
# On Proxmox k3s node
sudo nano /etc/systemd/system/k3s.service

# Add to ExecStart line:
--tls-san=<your-proxmox-ip>

# Restart k3s
sudo systemctl daemon-reload
sudo systemctl restart k3s
```

---

## Which Approach Should You Use?

### Use Option 1 (SSH to Proxmox) if:
- You're new to Kubernetes
- You want the simplest setup
- You don't mind working in SSH terminal

### Use Option 2 (Remote kubectl) if:
- You want to work from your Windows machine
- You're comfortable with command line tools
- You want a more professional development workflow

Both approaches work perfectly fine! Choose what's most comfortable for you.
