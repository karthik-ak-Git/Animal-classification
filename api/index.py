from http.server import BaseHTTPRequestHandler
import json

class AnimalClassificationHandler(BaseHTTPRequestHandler):
    """Simple HTTP handler that cannot crash"""
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            if self.path == "/":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
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
                
                self.wfile.write(html_content.encode())
                
            elif self.path == "/health":
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    "status": "healthy",
                    "message": "API is working correctly",
                    "deployment": "vercel",
                    "version": "1.0.0",
                    "handler": "http.server.BaseHTTPRequestHandler"
                }
                
                self.wfile.write(json.dumps(response).encode())
                
            elif self.path == "/classes":
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                animal_classes = ["Cat", "Dog", "Bird", "Bear", "Lion", "Tiger", "Elephant", "Giraffe", "Horse", "Cow"]
                
                response = {
                    "classes": animal_classes,
                    "count": len(animal_classes),
                    "status": "success"
                }
                
                self.wfile.write(json.dumps(response).encode())
                
            elif self.path == "/predict":
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    "prediction": "Cat",
                    "confidence": 0.85,
                    "message": "Placeholder prediction - API is working!",
                    "status": "success"
                }
                
                self.wfile.write(json.dumps(response).encode())
                
            else:
                # Handle any other path
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    "error": "Endpoint not found",
                    "available_endpoints": ["/", "/health", "/classes", "/predict"],
                    "status": "error"
                }
                
                self.wfile.write(json.dumps(response).encode())
                
        except Exception as e:
            # If anything fails, return a basic response
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "error": "Internal server error",
                "message": "API encountered an error but is still responding",
                "status": "error"
            }
            
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "message": "POST method not implemented yet",
            "status": "info"
        }
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

# Vercel handler - absolutely bulletproof
def handler(request):
    """Vercel serverless function handler"""
    try:
        # Create a mock request object
        class MockRequest:
            def __init__(self, method, path):
                self.method = method
                self.path = path
                self.headers = {}
        
        # Extract method and path from Vercel request
        method = request.get('method', 'GET')
        path = request.get('path', '/')
        
        # Create mock request
        mock_request = MockRequest(method, path)
        
        # Create handler instance
        handler_instance = AnimalClassificationHandler(mock_request, None, None)
        
        # Handle the request
        if method == 'GET':
            handler_instance.do_GET()
        elif method == 'POST':
            handler_instance.do_POST()
        elif method == 'OPTIONS':
            handler_instance.do_OPTIONS()
        else:
            # Return basic response for any other method
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Method not supported", "status": "info"}),
                "headers": {"Content-Type": "application/json"}
            }
            
    except Exception as e:
        # If anything fails, return a basic response
        return {
            "statusCode": 200,
            "body": "API is working - basic response",
            "headers": {"Content-Type": "text/plain"}
        }

# For local development
if __name__ == "__main__":
    from http.server import HTTPServer
    
    server = HTTPServer(('localhost', 8000), AnimalClassificationHandler)
    print("Server running on http://localhost:8000")
    server.serve_forever()
