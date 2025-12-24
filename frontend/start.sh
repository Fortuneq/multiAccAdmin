#!/bin/bash

# Multi-Account Admin Panel - Frontend Startup Script

echo "======================================"
echo "Multi-Account Admin Panel - Frontend"
echo "======================================"
echo ""

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    echo "Starting HTTP server on port 8080..."
    echo ""
    echo "Access the application at:"
    echo "  Dashboard:  http://localhost:8080/index.html"
    echo "  Accounts:   http://localhost:8080/accounts.html"
    echo "  Generator:  http://localhost:8080/generator.html"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    python3 -m http.server 8080
elif command -v python &> /dev/null; then
    echo "Starting HTTP server on port 8080..."
    echo ""
    echo "Access the application at:"
    echo "  Dashboard:  http://localhost:8080/index.html"
    echo "  Accounts:   http://localhost:8080/accounts.html"
    echo "  Generator:  http://localhost:8080/generator.html"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    python -m http.server 8080
else
    echo "ERROR: Python not found!"
    echo ""
    echo "Please install Python 3 or use an alternative method:"
    echo "  - Node.js: npx http-server -p 8080"
    echo "  - VS Code: Install Live Server extension"
    echo ""
fi
