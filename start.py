#!/usr/bin/env python3
"""
Startup script for Render deployment
Optimized for memory usage and proper port binding
"""

import os
import uvicorn
import signal
import sys
import gc

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print("🔄 Received shutdown signal, shutting down gracefully...")
    # Force garbage collection before exit
    gc.collect()
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Force garbage collection at startup
    gc.collect()
    
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get("PORT", 8000))
    
    # Set environment variables for better performance and memory management
    os.environ.setdefault("PYTHONUNBUFFERED", "1")
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "max_split_size_mb:128")
    
    print(f"🚀 Starting Animal Classification API on port {port}")
    print(f"🌍 Environment: {os.environ.get('RENDER_ENVIRONMENT', 'local')}")
    
    try:
        # Import app after setting environment variables
        from main_api import app
        
        # Bind to 0.0.0.0 to allow external connections
        # Use workers=1 to reduce memory usage
        # Add timeout and keep-alive settings
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=port,
            workers=1,  # Single worker to save memory
            log_level="info",
            timeout_keep_alive=30,
            timeout_graceful_shutdown=60,  # Increased for memory cleanup
            access_log=True,
            loop="asyncio"  # Use asyncio for better memory management
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)
