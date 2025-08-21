import json

def handler(request):
    """Vercel serverless function handler - absolutely bulletproof"""
    
    # Get request details
    method = request.get('method', 'GET')
    path = request.get('path', '/')
    
    # Set CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    try:
        # Handle different endpoints
        if path == "/" or path == "":
            # Root endpoint - return HTML
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Animal Classification API</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; text-align: center; background: #f5f5f5; }
                    .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    .endpoint { background: #f0f8ff; padding: 15px; margin: 15px 0; border-radius: 8px; border-left: 4px solid #007bff; }
                    .success { color: #28a745; font-weight: bold; }
                    .btn { display: inline-block; padding: 10px 20px; margin: 5px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
                    .btn:hover { background: #0056b3; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🐾 Animal Classification API</h1>
                    <p class="success">✅ API is running successfully on Vercel!</p>
                    
                    <h2>Available Endpoints:</h2>
                    <div class="endpoint">
                        <strong>/health</strong> - API health check
                    </div>
                    <div class="endpoint">
                        <strong>/classes</strong> - List of animal classes
                    </div>
                    <div class="endpoint">
                        <strong>/predict</strong> - Image prediction (placeholder)
                    </div>
                    
                    <h2>Test Links:</h2>
                    <a href="/health" class="btn">Health Check</a>
                    <a href="/classes" class="btn">Animal Classes</a>
                    <a href="/predict" class="btn">Test Prediction</a>
                    
                    <p><small>Deployed on Vercel - Serverless Function</small></p>
                </div>
            </body>
            </html>
            """
            
            return {
                "statusCode": 200,
                "body": html_content,
                "headers": {**headers, "Content-Type": "text/html"}
            }
            
        elif path == "/health":
            # Health check endpoint
            response = {
                "status": "healthy",
                "message": "API is working correctly",
                "deployment": "vercel",
                "version": "1.0.0",
                "handler": "simple_function"
            }
            
            return {
                "statusCode": 200,
                "body": json.dumps(response),
                "headers": {**headers, "Content-Type": "application/json"}
            }
            
        elif path == "/classes":
            # Animal classes endpoint
            animal_classes = ["Cat", "Dog", "Bird", "Bear", "Lion", "Tiger", "Elephant", "Giraffe", "Horse", "Cow"]
            
            response = {
                "classes": animal_classes,
                "count": len(animal_classes),
                "status": "success"
            }
            
            return {
                "statusCode": 200,
                "body": json.dumps(response),
                "headers": {**headers, "Content-Type": "application/json"}
            }
            
        elif path == "/predict":
            # Prediction endpoint
            response = {
                "prediction": "Cat",
                "confidence": 0.85,
                "message": "Placeholder prediction - API is working!",
                "status": "success"
            }
            
            return {
                "statusCode": 200,
                "body": json.dumps(response),
                "headers": {**headers, "Content-Type": "application/json"}
            }
            
        else:
            # Handle any other path
            response = {
                "error": "Endpoint not found",
                "available_endpoints": ["/", "/health", "/classes", "/predict"],
                "status": "error"
            }
            
            return {
                "statusCode": 404,
                "body": json.dumps(response),
                "headers": {**headers, "Content-Type": "application/json"}
            }
            
    except Exception as e:
        # If anything fails, return a basic response
        response = {
            "error": "Internal server error",
            "message": "API encountered an error but is still responding",
            "status": "error",
            "details": str(e)
        }
        
        return {
            "statusCode": 500,
            "body": json.dumps(response),
            "headers": {**headers, "Content-Type": "application/json"}
        }

# For local development
if __name__ == "__main__":
    # Test the handler locally
    test_request = {"method": "GET", "path": "/"}
    result = handler(test_request)
    print("Local test result:")
    print(f"Status: {result['statusCode']}")
    print(f"Body: {result['body'][:100]}...")
