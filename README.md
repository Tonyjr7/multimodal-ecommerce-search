# 🛍️ AI-Powered E-commerce Product Search

An intelligent product search system that combines **text search**, **handwriting recognition (OCR)**, and **computer vision** to help users find products in innovative ways.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### 1. **Text-Based Search** 🔍
- Semantic search using sentence embeddings
- Powered by Pinecone vector database
- Natural language understanding

### 2. **Handwriting Recognition (OCR)** ✍️
- Upload handwritten product queries
- EasyOCR OCR for text extraction
- Intelligent product matching

### 3. **Visual Product Search** 📸
- Upload product images
- CNN-based image classification
- Find similar products automatically

## 🏗️ Architecture

```
┌─────────────────┐
│   User Input    │
│ (Text/Image/OCR)│
└────────┬────────┘
         │
    ┌────▼────┐
    │  Flask  │
    │   API   │
    └────┬────┘
         │
    ┌────┴────────────────────┐
    │                         │
┌───▼────┐              ┌────▼─────┐
│Pinecone│              │TensorFlow│
│ Vector │              │   CNN    │
│   DB   │              │  Model   │
└────────┘              └──────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Docker & Docker Compose (for containerized deployment)
- Pinecone API Key ([Get one here](https://www.pinecone.io/))
- EasyOCR OCR (for local development)

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd AI-FRONTEND
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your PINECONE_API_KEY
   ```

3. **Ensure model files are present**
   - `ecommerce_cnn_model.h5`
   - `class_names.pkl`
   - `datasets/Cleaned_Dataset.csv`

4. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

5. **Access the application**
   - Open your browser: `http://localhost:5000`
   - Health check: `http://localhost:5000/health`

### Option 2: Local Development

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
   - **macOS**: `brew install tesseract`
   - **Windows**: [Download installer](https://github.com/UB-Mannheim/tesseract/wiki)

4. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
AI-FRONTEND/
├── main.py                      # Main Flask application
├── settings.py                  # Configuration management
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose setup
├── .env.example                 # Environment template
├── .gitignore                   # Git exclusions
├── .dockerignore               # Docker exclusions
│
├── utils/
│   ├── ocr.py                  # OCR processing logic
│   └── image_processor.py      # Image preprocessing
│
├── templates/
│   ├── base.html               # Base template
│   ├── text.html               # Text search UI
│   ├── ocr.html                # OCR search UI
│   └── vision.html             # Vision search UI
│
├── datasets/
│   └── Cleaned_Dataset.csv     # Product database
│
├── model/
│   ├── ecommerce_cnn_model.h5  # Trained CNN model
│   └── class_names.pkl         # Product class mappings
│
└── classname/                  # Additional resources
```

## 🔌 API Endpoints

### Health Check
```http
GET /health
```
Returns service health status and model availability.

### Text Search
```http
POST /api/text
Content-Type: application/json

{
  "query": "red alarm clock"
}
```

### OCR Search
```http
POST /api/ocr
Content-Type: multipart/form-data

file: <image-file>
```

### Vision Search
```http
POST /api/vision
Content-Type: multipart/form-data

file: <image-file>
```

## 🛠️ Technology Stack

| Category | Technology |
|----------|-----------|
| **Backend** | Flask 3.0 |
| **ML Framework** | TensorFlow 2.15 |
| **Vector DB** | Pinecone |
| **Embeddings** | Sentence Transformers |
| **OCR** | EasyOCR |
| **Server** | Gunicorn (Production) |
| **Containerization** | Docker + Docker Compose |

## 🔐 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `PINECONE_API_KEY` | Your Pinecone API key | ✅ Yes |
| `FLASK_ENV` | Environment (development/production) | No |
| `INDEX_NAME` | Pinecone index name | No |
| `DATA_PATH` | Path to product CSV | No |

## 🧪 Testing

Test the health endpoint:
```bash
curl http://localhost:5000/health
```

Test text search:
```bash
curl -X POST http://localhost:5000/api/text \
  -H "Content-Type: application/json" \
  -d '{"query": "alarm clock"}'
```

## 📊 Model Information

### CNN Model
- **Architecture**: Custom CNN for product classification
- **Input**: 224x224 RGB images
- **Output**: Product stock codes
- **Training Dataset**: E-commerce product images

### Embedding Model
- **Model**: `all-MiniLM-L6-v2`
- **Dimension**: 384
- **Use Case**: Semantic text search

## 🚢 Deployment

### Docker Production Deployment

The Dockerfile uses multi-stage builds for optimization:
- **Builder stage**: Compiles dependencies
- **Production stage**: Minimal runtime image
- **Security**: Non-root user execution
- **Health checks**: Automatic container monitoring

### Resource Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **CPU** | 1 core | 2+ cores |
| **RAM** | 2 GB | 4 GB |
| **Storage** | 5 GB | 10 GB |

### Scaling Considerations

- Increase Gunicorn workers for higher traffic
- Use load balancer for multiple instances
- Consider GPU support for faster inference
- Implement caching for frequent queries

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Pinecone](https://www.pinecone.io/) for vector database
- [Sentence Transformers](https://www.sbert.net/) for embeddings
- [TensorFlow](https://www.tensorflow.org/) for ML framework
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for text recognition

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ for intelligent product discovery**
