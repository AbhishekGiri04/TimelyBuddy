#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p database
mkdir -p uploads/profiles
mkdir -p uploads/assignments
mkdir -p uploads/submissions
mkdir -p exports

# Initialize database
python init_db.py

echo "Build completed successfully!"