#!/bin/bash
apt-get update -y
apt-get install -y docker.io

# Run Docker container
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  --name ${app_name} \
  ghcr.io/yourusername/qrgenx:latest
