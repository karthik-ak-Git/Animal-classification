# 📚 API Documentation

## Base URL

```
Local: http://localhost:8000
Production: https://your-domain.com
```

## Authentication

### Public Endpoints

Most endpoints are publicly accessible. For production use, implement API key authentication.

### Rate Limiting

- **Default**: 100 requests per 60 seconds per IP
- **Headers**: 
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Reset timestamp

## Endpoints

### 1. Health Check

**GET** `/health`

Check API health and status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "num_classes": 75,
  "memory_usage": "45.2%",
  "timestamp": "2025-01-20T10:30:00Z"
}
```

---

### 2. Get Classes

**GET** `/classes`

Retrieve list of supported animal classes.

**Response:**
```json
{
  "status": "success",
  "num_classes": 75,
  "classes": [
    "African Elephant",
    "Asian Elephant",
    "Bengal Tiger",
    ...
  ]
}
```

---

### 3. Predict Animal

**POST** `/predict`

Classify an animal from an uploaded image.

**Request:**
- Content-Type: `multipart/form-data`
- Body Parameter: `file` (image file)

**File Requirements:**
- Type: JPEG, PNG, JPG
- Max Size: 10MB
- Min Dimensions: 224x224 recommended

**Example Request (cURL):**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/image.jpg"
```

**Response:**
```json
{
  "prediction": "Bengal Tiger",
  "base_class": "Tiger",
  "confidence": 0.9542,
  "breeds": [
    "Bengal Tiger",
    "Siberian Tiger",
    "Tiger"
  ],
  "scores": [0.9542, 0.0321, 0.0089]
}
```

**Error Responses:**
- `400`: Invalid file type or size
- `503`: Model not loaded
- `500`: Prediction failed

---

### 4. Visualize Prediction (Grad-CAM)

**POST** `/visualize`

Generate a Grad-CAM heatmap visualization showing what the model focuses on.

**Request:**
- Content-Type: `multipart/form-data`
- Body Parameter: `file` (image file)

**Example Request (cURL):**
```bash
curl -X POST "http://localhost:8000/visualize" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/image.jpg"
```

**Response:**
```json
{
  "predicted_class": "Golden Retriever",
  "confidence": 0.9123,
  "visualization": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA...",
  "success": true
}
```

**Note:** The `visualization` field contains a base64-encoded image that can be directly used in `<img>` tags.

---

### 5. Submit Feedback

**POST** `/feedback`

Submit a correction when the model makes an incorrect prediction.

**Request:**
- Content-Type: `application/json`

**Body:**
```json
{
  "predicted_class": "Labrador",
  "correct_class": "Golden Retriever",
  "confidence": 0.8534,
  "comments": "The dog has longer fur, clearly a Golden Retriever",
  "timestamp": "2025-01-20T10:30:00",
  "image_data": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Example Request (cURL):**
```bash
curl -X POST "http://localhost:8000/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "predicted_class": "Labrador",
    "correct_class": "Golden Retriever",
    "confidence": 0.85,
    "comments": "Incorrect breed identification"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Feedback submitted - Model retraining initiated",
  "feedback_id": 42,
  "image_saved": true,
  "retraining_triggered": true
}
```

**Notes:**
- Triggers automatic incremental learning
- Image is optional but recommended
- Model updates asynchronously

---

### 6. Get Analytics

**GET** `/analytics`

Retrieve model performance metrics and analytics.

**Response:**
```json
{
  "status": "success",
  "metrics": {
    "timestamp": "2025-01-20T10:30:00Z",
    "accuracy_metrics": {
      "total_feedback": 150,
      "reported_errors": 150,
      "feedback_over_time": [
        {"date": "2025-01-18", "count": 45},
        {"date": "2025-01-19", "count": 62},
        {"date": "2025-01-20", "count": 43}
      ]
    },
    "confusion_analysis": {
      "most_confused_pairs": [
        {
          "predicted": "Labrador",
          "actual": "Golden Retriever",
          "count": 12
        }
      ],
      "most_mispredicted_classes": {
        "Labrador": 15,
        "German Shepherd": 10
      }
    },
    "confidence_analysis": {
      "avg_confidence": 0.7842,
      "min_confidence": 0.3421,
      "max_confidence": 0.9987
    }
  }
}
```

---

### 7. Get Analytics Dashboard

**GET** `/analytics/dashboard`

Generate a visual analytics dashboard with charts and graphs.

**Response:**
```json
{
  "status": "success",
  "dashboard": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUg..."
}
```

**Note:** Returns a base64-encoded PNG image containing:
- Feedback timeline graph
- Most confused classes chart
- Confidence distribution histogram
- Misprediction frequency bar chart

---

## Error Handling

All endpoints return consistent error responses:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes

- `200`: Success
- `400`: Bad Request (invalid input)
- `401`: Unauthorized (invalid API key)
- `413`: Payload Too Large (file size exceeded)
- `415`: Unsupported Media Type (invalid file type)
- `422`: Validation Error (missing required fields)
- `429`: Too Many Requests (rate limit exceeded)
- `500`: Internal Server Error
- `503`: Service Unavailable (model not loaded)

---

## Code Examples

### Python

```python
import requests

# Predict
with open('dog.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/predict',
        files={'file': f}
    )
    print(response.json())

# Submit feedback
feedback = {
    'predicted_class': 'Labrador',
    'correct_class': 'Golden Retriever',
    'confidence': 0.85
}
response = requests.post(
    'http://localhost:8000/feedback',
    json=feedback
)
print(response.json())
```

### JavaScript

```javascript
// Predict
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/predict', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));

// Submit feedback
fetch('http://localhost:8000/feedback', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        predicted_class: 'Labrador',
        correct_class: 'Golden Retriever',
        confidence: 0.85
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

### cURL

```bash
# Predict
curl -X POST "http://localhost:8000/predict" \
  -F "file=@dog.jpg"

# Get analytics
curl "http://localhost:8000/analytics"

# Health check
curl "http://localhost:8000/health"
```

---

## Interactive Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Test endpoints directly in the browser
- See request/response schemas
- View example requests
- Download OpenAPI specification

---

## WebSocket Support

*Coming soon: Real-time prediction updates and training progress*

---

## Versioning

Current API version: **v2.0.0**

Breaking changes will increment major version number. Monitor the `/health` endpoint for version information.

---

## Support

- GitHub Issues: [Report bugs](https://github.com/yourusername/animal-classification/issues)
- Email: support@example.com
- Documentation: [Full docs](https://your-docs-site.com)
