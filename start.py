#!/usr/bin/env python3
"""
Startup script for Animal Classification API
Optimized for local development
"""

import os
import uvicorn
import signal
import sys

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print("\n🔄 Shutting down gracefully...")
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Configuration for local development
    port = 8000
    host = "127.0.0.1"  # Local development
    
    print(f"🚀 Starting Animal Classification API")
    print(f"📍 Server: http://{host}:{port}")
    print(f"📊 API Docs: http://{host}:{port}/docs")
    print(f"💚 Health Check: http://{host}:{port}/health")
    print(f"\n⌨️  Press CTRL+C to stop\n")
    
    try:
        from main_api import app
        
        uvicorn.run(
            app, 
            host=host, 
            port=port,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print(f"💡 Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
