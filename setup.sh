#!/bin/bash

# WDP Office Data Analytics - Setup Script
echo "🏢 Setting up WDP Office Data Analytics..."
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📚 Installing Python packages..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating environment configuration..."
    cp .env.template .env
    echo "✅ Created .env file - please update with your settings"
fi

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "🤖 Ollama not found. Installing..."
    curl -fsSL https://ollama.ai/install.sh | sh
    echo "📥 Pulling llama3.1 model..."
    ollama pull llama3.1
else
    echo "✅ Ollama already installed"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your database configuration"
echo "2. Run migration script: python migrate_wdp.py"
echo "3. Start the application: chainlit run app.py"
echo ""
echo "Visit http://localhost:8000 to access your WDP analytics dashboard!"
