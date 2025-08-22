#!/usr/bin/env python3
"""
Startup script for Render deployment
Optimized for memory usage and proper port binding
"""

import os
import uvicorn
from main_api import app

if __name__ == "__main__":
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get("PORT", 8000))
    
    # Bind to 0.0.0.0 to allow external connections
    # Use workers=1 to reduce memory usage
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        workers=1,  # Single worker to save memory
        log_level="info"
    )
