#!/bin/bash

REPO_TAG=$1

# Extract repo name and tag from input (format: reponame-tagversion)
REPO_NAME=$(echo "$REPO_TAG" | sed 's/-[^-]*$//')
TAG_VERSION=$(echo "$REPO_TAG" | sed 's/.*-//')

mkdir -p /opt/jazz/apps/${REPO_NAME}
cd /opt/jazz/apps/${REPO_NAME}

# Stop existing containers if directory exists
if [ -d "$REPO_TAG" ]; then
    cd "$REPO_TAG"
    sudo docker compose down
    cd ..
fi

# Clone the repository with specific tag (add v prefix)
git clone --branch "v${TAG_VERSION}" --depth 1 --single-branch "https://github.com/jaskirat1208/${REPO_NAME}.git" "$REPO_TAG"

# Create symlink
ln -sf "$REPO_TAG" "$REPO_NAME"

# Navigate to the symlink directory
cd "$REPO_NAME" 