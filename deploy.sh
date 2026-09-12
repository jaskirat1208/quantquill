#!/bin/bash

REPO_TAG=$1

# Extract repo name and tag from input (format: reponame-tagversion)
REPO_NAME=$(echo "$REPO_TAG" | sed 's/-[^-]*$//')
TAG_VERSION=$(echo "$REPO_TAG" | sed 's/.*-//')

TARGET_DIR="/opt/jazz/apps/${REPO_NAME}"
SERVICE_NAME="quantquill"

echo "Deploying ${REPO_NAME} version ${TAG_VERSION} to ${TARGET_DIR}..."

mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

# Stop and remove any existing containers with conflicting names
echo "Stopping any existing containers..."
docker stop quantquill-api quantquill-frontend 2>/dev/null || true
docker rm quantquill-api quantquill-frontend 2>/dev/null || true

# Stop containers from currently deployed version (if symlink exists)
if [ -L "$REPO_NAME" ]; then
    CURRENT_VERSION=$(readlink "$REPO_NAME")
    echo "Current version symlink points to: $CURRENT_VERSION"
    if [ -d "$CURRENT_VERSION" ]; then
        cd "$CURRENT_VERSION"
        docker compose down || true
        cd ..
    fi
fi

# Clone the repository if it doesn't exist
if [ ! -d "$REPO_TAG" ]; then
    echo "Cloning version ${TAG_VERSION}..."
    git clone --branch "v${TAG_VERSION}" --depth 1 --single-branch "https://github.com/jaskirat1208/${REPO_NAME}.git" "$REPO_TAG"
else
    echo "Version ${TAG_VERSION} already exists, skipping clone"
fi

# Update symlink to point to the target version
echo "Creating symlink: $REPO_NAME -> $REPO_TAG"
# Remove existing symlink if it exists
if [ -L "$REPO_NAME" ]; then
    echo "Removing existing symlink: $REPO_NAME"
    rm "$REPO_NAME"
fi
ln -s "$REPO_TAG" "$REPO_NAME"

# Verify symlink was created
if [ -L "$REPO_NAME" ]; then
    echo "Symlink created successfully: $(readlink $REPO_NAME)"
else
    echo "ERROR: Symlink was not created"
    exit 1
fi

# Navigate to the symlink directory
cd "$REPO_NAME"

# Build and start Docker services
echo "Building Docker images..."
docker compose build

echo "Starting services..."
docker compose up -d

# Setup systemd service
echo "Setting up systemd service..."
if [ -f "systemd/quantquill.service" ]; then
    sudo cp systemd/quantquill.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable $SERVICE_NAME
    sudo systemctl restart $SERVICE_NAME
else
    echo "WARNING: systemd service file not found, skipping systemd setup"
fi

echo "Deployment complete!"
echo "Version: ${TAG_VERSION}"
echo "Services running at:"
echo "  - Frontend: http://localhost:8090"
echo "  - API: http://localhost:8091"
 