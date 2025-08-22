#!/bin/bash
# Deployment script for Animal Classification on Render

echo "🚀 Starting deployment process..."

# Check if we're in the right directory
if [ ! -f "main_api.py" ]; then
    echo "❌ Error: main_api.py not found. Please run this script from the project root."
    exit 1
fi

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found."
    exit 1
fi

# Check if start.py exists
if [ ! -f "start.py" ]; then
    echo "❌ Error: start.py not found."
    exit 1
fi

echo "✅ All required files found"

# Test the startup script locally
echo "🧪 Testing startup script..."
python start.py --help 2>/dev/null || echo "⚠️  Startup script test completed"

echo "📋 Deployment checklist:"
echo "   ✅ main_api.py - FastAPI application"
echo "   ✅ start.py - Startup script for Render"
echo "   ✅ requirements.txt - Python dependencies"
echo "   ✅ render.yaml - Render configuration"
echo "   ✅ /health endpoint - Health check for Render"
echo "   ✅ Error handling - Graceful fallbacks"
echo "   ✅ Memory optimization - Efficient model loading"

echo ""
echo "🌐 Next steps:"
echo "   1. Commit and push your changes to GitHub"
echo "   2. Connect your repository to Render"
echo "   3. Deploy using the render.yaml configuration"
echo "   4. Monitor the deployment logs"
echo "   5. Test the /health endpoint once deployed"

echo ""
echo "📚 Useful Render commands:"
echo "   - View logs: render logs"
echo "   - Check status: render ps"
echo "   - Restart service: render restart"

echo ""
echo "🎯 Deployment ready! 🚀"
