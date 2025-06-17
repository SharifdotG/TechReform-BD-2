#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Navigate to Tailwind CSS directory and install Node.js dependencies
cd theme/static_src
npm install

# Build Tailwind CSS for production
npm run build

# Return to project root
cd ../..

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate
