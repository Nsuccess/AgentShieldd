#!/bin/bash

echo "🚀 Starting AgentShield API..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Start server
echo ""
echo "✅ Starting server on http://localhost:8000"
echo "📚 API docs: http://localhost:8000/docs"
echo ""

python main.py
