#!/bin/bash

REPO_TAG=$1

# Extract repo name and tag from input (format: reponame-tagversion)
REPO_NAME=$(echo "$REPO_TAG" | sed 's/-[^-]*$//')
TAG_VERSION=$(echo "$REPO_TAG" | sed 's/.*-//')

mkdir -p /opt/jazz/apps/${REPO_NAME}
cd /opt/jazz/apps/${REPO_NAME}

# Stop containers from currently deployed version (if symlink exists)
if [ -L "$REPO_NAME" ]; then
    CURRENT_VERSION=$(readlink "$REPO_NAME")
    if [ -d "$CURRENT_VERSION" ]; then
        cd "$CURRENT_VERSION"
        sudo docker compose down
        cd ..
    fi
fi

# Clone the repository if it doesn't exist
if [ ! -d "$REPO_TAG" ]; then
    git clone --branch "v${TAG_VERSION}" --depth 1 --single-branch "https://github.com/jaskirat1208/${REPO_NAME}.git" "$REPO_TAG"
fi

# Update symlink to point to the target version
ln -sf "$REPO_TAG" "$REPO_NAME"

# Navigate to the symlink directory
cd "$REPO_NAME" 