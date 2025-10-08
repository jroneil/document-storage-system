#!/bin/bash

# Document Storage System - Docker Image Build Script
# This script builds and pushes all Docker images to a registry

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
REGISTRY=${DOCKER_REGISTRY:-"YOUR_REGISTRY"}
TAG=${IMAGE_TAG:-"latest"}
PROJECT_ROOT=$(dirname "$(dirname "$(readlink -f "$0")")")

# Services to build
SERVICES=(
    "api-gateway"
    "ingestion-service"
    "metadata-service"
    "storage-service"
    "processing-service"
    "search-service"
    "ai-service"
    "notification-service"
    "bulk-upload-service"
    "saga-orchestrator"
    "admin-service"
)

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

check_prerequisites() {
    print_info "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    
    if [ "$REGISTRY" = "YOUR_REGISTRY" ]; then
        print_error "Please set DOCKER_REGISTRY environment variable"
        print_info "Example: export DOCKER_REGISTRY=docker.io/yourusername"
        exit 1
    fi
    
    print_info "Prerequisites check passed!"
}

build_service() {
    local service=$1
    local image_name="${REGISTRY}/${service}:${TAG}"
    
    print_info "Building $service..."
    
    if [ ! -d "$PROJECT_ROOT/$service" ]; then
        print_warning "Directory $service not found, skipping..."
        return
    fi
    
    cd "$PROJECT_ROOT/$service"
    
    if [ ! -f "Dockerfile" ] && [ ! -f "DockerFile" ] && [ ! -f "DOCKERFILE" ]; then
        print_warning "No Dockerfile found for $service, skipping..."
        return
    fi
    
    # Find the correct Dockerfile name
    DOCKERFILE="Dockerfile"
    [ -f "DockerFile" ] && DOCKERFILE="DockerFile"
    [ -f "DOCKERFILE" ] && DOCKERFILE="DOCKERFILE"
    
    docker build -t "$image_name" -f "$DOCKERFILE" .
    
    print_info "Successfully built $image_name"
}

push_service() {
    local service=$1
    local image_name="${REGISTRY}/${service}:${TAG}"
    
    print_info "Pushing $service to registry..."
    docker push "$image_name"
    print_info "Successfully pushed $image_name"
}

build_all() {
    print_info "Building all services with tag: $TAG"
    
    for service in "${SERVICES[@]}"; do
        build_service "$service"
    done
    
    print_info "All images built successfully!"
}

push_all() {
    print_info "Pushing all images to registry: $REGISTRY"
    
    read -p "Do you want to push images to $REGISTRY? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Push cancelled"
        exit 0
    fi
    
    # Login to registry
    print_info "Logging in to registry..."
    docker login "$REGISTRY" || {
        print_error "Failed to login to registry"
        exit 1
    }
    
    for service in "${SERVICES[@]}"; do
        push_service "$service"
    done
    
    print_info "All images pushed successfully!"
}

show_images() {
    print_info "Built images:"
    for service in "${SERVICES[@]}"; do
        echo "  - ${REGISTRY}/${service}:${TAG}"
    done
}

main() {
    echo "=========================================="
    echo "Document Storage System - Image Builder"
    echo "Registry: $REGISTRY"
    echo "Tag: $TAG"
    echo "=========================================="
    echo ""
    
    check_prerequisites
    
    case "${1:-build}" in
        build)
            build_all
            show_images
            ;;
        push)
            push_all
            ;;
        all)
            build_all
            push_all
            show_images
            ;;
        *)
            print_error "Unknown command: $1"
            echo "Usage: $0 [build|push|all]"
            exit 1
            ;;
    esac
    
    echo ""
    print_info "Done!"
}

main "$@"
