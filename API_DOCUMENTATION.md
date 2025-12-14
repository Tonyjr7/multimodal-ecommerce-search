# API Documentation

## Overview

The AI E-commerce Search API provides three intelligent search methods for product discovery.

**Base URL**: `http://localhost:5000`

**Content-Type**: `application/json` (for JSON endpoints) or `multipart/form-data` (for file uploads)

---

## Endpoints

### 1. Health Check

Check the service health and model availability.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "service": "AI E-commerce Search",
  "models": {
    "pinecone": "connected",
    "embeddings": "loaded",
    "cnn": "loaded"
  }
}
```

**Status Codes**:
- `200 OK` - Service is healthy
- `503 Service Unavailable` - Service or models unavailable

---

### 2. Text Search

Semantic search using natural language queries.

**Endpoint**: `POST /api/text`

**Request Body**:
```json
{
  "query": "red alarm clock"
}
```

**Response**:
```json
{
  "message": "Showing results for: 'red alarm clock'",
  "products": [
    {
      "StockCode": "22727",
      "Description": "ALARM CLOCK BAKELIKE RED",
      "score": 0.85
    },
    {
      "StockCode": "22112",
      "Description": "CHOCOLATE HOT WATER BOTTLE",
      "score": 0.72
    }
  ]
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/text \
  -H "Content-Type: application/json" \
  -d '{"query": "red alarm clock"}'
```

---

### 3. OCR Search

Search using handwritten text recognition.

**Endpoint**: `POST /api/ocr`

**Request**: `multipart/form-data`
- `file`: Image file containing handwritten text

**Response**:
```json
{
  "detected_text": "alarm clock",
  "products": [
    {
      "StockCode": "22727",
      "Description": "ALARM CLOCK BAKELIKE RED",
      "score": 0.88
    }
  ]
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/ocr \
  -F "file=@handwriting.jpg"
```

**Error Response**:
```json
{
  "error": "No text detected. Try writing clearer."
}
```

---

### 4. Vision Search

Search using product images.

**Endpoint**: `POST /api/vision`

**Request**: `multipart/form-data`
- `file`: Product image file

**Response**:
```json
{
  "detected_product": "ALARM CLOCK BAKELIKE RED",
  "detected_stock_code": "22727",
  "confidence": "94.5%",
  "similar_products": [
    {
      "StockCode": "22423",
      "Description": "REGENCY CAKESTAND 3 TIER",
      "score": 0.76
    }
  ]
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/api/vision \
  -F "file=@product.jpg"
```

**Error Response**:
```json
{
  "error": "Invalid image format"
}
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

| Status Code | Meaning |
|-------------|---------|
| 200 | Success |
| 400 | Bad Request (invalid input) |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

**Error Response Format**:
```json
{
  "error": "Description of the error"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing rate limiting based on your requirements.

---

## Authentication

Currently, the API is open. For production deployment, implement authentication using:
- API Keys
- JWT tokens
- OAuth 2.0

---

## Best Practices

1. **Image Uploads**:
   - Supported formats: JPG, PNG, JPEG
   - Recommended size: < 5MB
   - For OCR: Clear, high-contrast handwriting
   - For Vision: Well-lit product images

2. **Text Queries**:
   - Use descriptive terms
   - Natural language works best
   - 2-50 words recommended

3. **Error Handling**:
   - Always check status codes
   - Handle errors gracefully
   - Retry on 500 errors

---

## Examples

### JavaScript (Fetch API)

```javascript
// Text Search
async function searchByText(query) {
  const response = await fetch('http://localhost:5000/api/text', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });
  return await response.json();
}

// Vision Search
async function searchByImage(imageFile) {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await fetch('http://localhost:5000/api/vision', {
    method: 'POST',
    body: formData,
  });
  return await response.json();
}
```

### Python (Requests)

```python
import requests

# Text Search
def search_by_text(query):
    response = requests.post(
        'http://localhost:5000/api/text',
        json={'query': query}
    )
    return response.json()

# Vision Search
def search_by_image(image_path):
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            'http://localhost:5000/api/vision',
            files=files
        )
    return response.json()
```

---

## Support

For issues or questions, please open an issue on GitHub.
