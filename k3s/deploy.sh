#!/bin/bash

# Document Storage System - K3s Deployment Script
# This script deploys the DMS to k3s cluster

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-development}
NAMESPACE="document-storage"

# Functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    print_info "Checking prerequisites..."
    
    # Check if kubectl is installed
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl is not installed. Please install kubectl first."
        exit 1
    fi
    
    # Check if kustomize is installed
    if ! command -v kustomize &> /dev/null; then
        print_warning "kustomize is not installed. Using kubectl kustomize instead."
    fi
    
    # Check if k3s cluster is accessible
    if ! kubectl cluster-info &> /dev/null; then
        print_error "Cannot connect to k3s cluster. Please check your kubeconfig."
        exit 1
    fi
    
    print_info "Prerequisites check passed!"
}

deploy_namespace() {
    print_info "Creating namespace if it doesn't exist..."
    kubectl apply -f base/namespace.yaml
}

update_secrets() {
    print_info "Updating secrets..."
    print_warning "Remember to update the secrets in k3s/base/secrets.yaml with production values!"
    read -p "Have you updated the secrets? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Please update secrets before deploying to production."
        exit 1
    fi
}

deploy_infrastructure() {
    print_info "Deploying infrastructure components (databases, message queue, etc.)..."
    kubectl apply -f base/persistent-volumes.yaml
    kubectl apply -f base/postgres.yaml
    kubectl apply -f base/mongodb.yaml
    kubectl apply -f base/rabbitmq.yaml
    kubectl apply -f base/minio.yaml
    kubectl apply -f base/elasticsearch.yaml
    
    print_info "Waiting for infrastructure to be ready..."
    kubectl wait --for=condition=ready pod -l app=postgres -n $NAMESPACE --timeout=300s || true
    kubectl wait --for=condition=ready pod -l app=mongo -n $NAMESPACE --timeout=300s || true
    kubectl wait --for=condition=ready pod -l app=rabbitmq -n $NAMESPACE --timeout=300s || true
    kubectl wait --for=condition=ready pod -l app=elasticsearch -n $NAMESPACE --timeout=300s || true
}

deploy_services() {
    print_info "Deploying microservices..."
    
    if [ "$ENVIRONMENT" = "production" ]; then
        kubectl apply -k overlays/production/
    else
        kubectl apply -k overlays/development/
    fi
    
    print_info "Waiting for services to be ready..."
    sleep 10
}

deploy_ingress() {
    print_info "Deploying ingress..."
    print_warning "Make sure to update domain names in k3s/base/ingress.yaml"
    kubectl apply -f base/ingress.yaml
}

initialize_minio() {
    print_info "Initializing MinIO bucket..."
    print_warning "You may need to manually create the 'documents' bucket in MinIO console"
}

show_status() {
    print_info "Deployment Status:"
    echo ""
    kubectl get pods -n $NAMESPACE
    echo ""
    kubectl get services -n $NAMESPACE
    echo ""
    kubectl get ingress -n $NAMESPACE
}

main() {
    echo "=========================================="
    echo "Document Storage System - K3s Deployment"
    echo "Environment: $ENVIRONMENT"
    echo "=========================================="
    echo ""
    
    check_prerequisites
    
    if [ "$ENVIRONMENT" = "production" ]; then
        update_secrets
    fi
    
    deploy_namespace
    deploy_infrastructure
    deploy_services
    deploy_ingress
    initialize_minio
    
    echo ""
    print_info "Deployment completed!"
    echo ""
    
    show_status
    
    echo ""
    print_info "Access your services:"
    print_info "1. Update /etc/hosts with your k3s node IP and domain names"
    print_info "2. Access the web UI at: http://dms.yourdomain.com"
    print_info "3. Access the API at: http://api.dms.yourdomain.com"
    print_info "4. Access MinIO console at: http://minio.dms.yourdomain.com"
    print_info "5. Access RabbitMQ management at: http://rabbitmq.dms.yourdomain.com"
    echo ""
}

# Run main function
main
