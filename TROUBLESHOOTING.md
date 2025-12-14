# 🔧 Troubleshooting Guide

Common issues and their solutions for the AI E-commerce Search application.

---

## 🐳 Docker Issues

### Issue: "Cannot connect to Docker daemon"

**Symptoms:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solutions:**
1. **Start Docker Desktop** (Windows/Mac)
2. **Linux**: Start Docker service
   ```bash
   sudo systemctl start docker
   ```
3. **Check Docker status**
   ```bash
   docker version
   ```

---

### Issue: "Port 5000 already in use"

**Symptoms:**
```
Error starting userland proxy: listen tcp4 0.0.0.0:5000: bind: address already in use
```

**Solutions:**

**Option 1: Stop the conflicting process**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

**Option 2: Change the port**
Edit `docker-compose.yml`:
```yaml
ports:
  - "5001:5000"  # Change 5001 to any available port
```

---

### Issue: "No such file or directory: ecommerce_cnn_model.h5"

**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'ecommerce_cnn_model.h5'
```

**Solutions:**
1. **Ensure model files exist**
   ```bash
   ls -la *.h5 *.pkl
   ```

2. **Check volume mounts in docker-compose.yml**
   ```yaml
   volumes:
     - ./ecommerce_cnn_model.h5:/app/ecommerce_cnn_model.h5:ro
     - ./class_names.pkl:/app/class_names.pkl:ro
   ```

3. **Verify file paths are correct**

---

### Issue: Container keeps restarting

**Symptoms:**
```bash
docker ps -a
# Shows container constantly restarting
```

**Solutions:**

1. **Check logs**
   ```bash
   docker logs ai-ecommerce
   # or
   docker-compose logs
   ```

2. **Common causes:**
   - Missing environment variables
   - Model files not found
   - Pinecone API key invalid
   - Insufficient memory

3. **Increase memory limit**
   ```yaml
   # docker-compose.yml
   deploy:
     resources:
       limits:
         memory: 6G  # Increase from 4G
   ```

---

## 🔑 Environment & Configuration Issues

### Issue: "PINECONE_API_KEY environment variable is required"

**Symptoms:**
```
ValueError: PINECONE_API_KEY environment variable is required
```

**Solutions:**

1. **Create .env file**
   ```bash
   cp .env.example .env
   ```

2. **Add your API key**
   ```bash
   # .env
   PINECONE_API_KEY=your_actual_api_key_here
   ```

3. **Verify .env is loaded**
   ```bash
   # Docker Compose automatically loads .env
   docker-compose config
   ```

---

### Issue: "Index 'ecommerce-products' not found"

**Symptoms:**
```
pinecone.exceptions.NotFoundException: Index not found
```

**Solutions:**

1. **Create the index in Pinecone**
   - Log into Pinecone console
   - Create index named "ecommerce-products"
   - Set dimensions to 384 (for all-MiniLM-L6-v2)

2. **Or change index name**
   ```bash
   # .env
   INDEX_NAME=your_index_name
   ```

---

## 🖼️ OCR Issues

### Issue: "Tesseract not found"

**Symptoms:**
```
TesseractNotFoundError: tesseract is not installed
```

**Solutions:**

**Docker**: Already included in Dockerfile ✅

**Local Development:**

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-eng
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
1. Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install and add to PATH
3. Restart terminal

---

### Issue: "No text detected" from OCR

**Symptoms:**
```json
{"error": "No text detected. Try writing clearer."}
```

**Solutions:**

1. **Improve image quality**
   - Use high-contrast images
   - Ensure text is clear and legible
   - Avoid blurry or low-resolution images

2. **Check image format**
   - Supported: JPG, PNG, JPEG
   - Max size: 5MB recommended

3. **Test with sample image**
   ```bash
   curl -X POST http://localhost:5000/api/ocr \
     -F "file=@test_image.jpg"
   ```

---

## 🧠 Model & AI Issues

### Issue: "Model prediction fails"

**Symptoms:**
```
Error: Invalid image format or model prediction failed
```

**Solutions:**

1. **Verify model files**
   ```bash
   # Check file sizes
   ls -lh ecommerce_cnn_model.h5 class_names.pkl
   ```

2. **Test model loading**
   ```python
   import tensorflow as tf
   model = tf.keras.models.load_model('ecommerce_cnn_model.h5')
   print(model.summary())
   ```

3. **Check TensorFlow version**
   ```bash
   pip show tensorflow
   # Should be 2.15.0
   ```

---

### Issue: High memory usage

**Symptoms:**
- Container using 4GB+ RAM
- System slowdown
- OOM (Out of Memory) errors

**Solutions:**

1. **Increase Docker memory limit**
   - Docker Desktop → Settings → Resources
   - Increase memory to 6-8GB

2. **Optimize model loading**
   - Load models lazily
   - Use model quantization
   - Consider using smaller models

3. **Monitor memory**
   ```bash
   docker stats ai-ecommerce
   ```

---

## 🌐 Network & API Issues

### Issue: "Connection refused" when accessing API

**Symptoms:**
```
curl: (7) Failed to connect to localhost port 5000: Connection refused
```

**Solutions:**

1. **Check if container is running**
   ```bash
   docker ps
   ```

2. **Check health endpoint**
   ```bash
   curl http://localhost:5000/health
   ```

3. **Verify port mapping**
   ```bash
   docker port ai-ecommerce
   ```

4. **Check firewall**
   - Windows: Allow port 5000 in Windows Firewall
   - Linux: `sudo ufw allow 5000`

---

### Issue: CORS errors in browser

**Symptoms:**
```
Access to fetch at 'http://localhost:5000/api/text' has been blocked by CORS policy
```

**Solutions:**

1. **Add CORS support** (for development)
   ```python
   # main.py
   from flask_cors import CORS
   
   app = Flask(__name__)
   CORS(app)  # Enable CORS for all routes
   ```

2. **Install flask-cors**
   ```bash
   pip install flask-cors
   # Add to requirements.txt
   ```

---

## 📦 Dependency Issues

### Issue: "No module named 'X'"

**Symptoms:**
```
ModuleNotFoundError: No module named 'sentence_transformers'
```

**Solutions:**

1. **Reinstall dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Clear pip cache**
   ```bash
   pip cache purge
   pip install --no-cache-dir -r requirements.txt
   ```

3. **Use virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

---

### Issue: Version conflicts

**Symptoms:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed
```

**Solutions:**

1. **Use pinned versions**
   - Already done in requirements.txt ✅

2. **Create fresh environment**
   ```bash
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

---

## 🚀 Performance Issues

### Issue: Slow API responses

**Symptoms:**
- Requests taking >5 seconds
- Timeouts

**Solutions:**

1. **Check resource usage**
   ```bash
   docker stats
   ```

2. **Increase workers**
   ```bash
   # .env
   WORKERS=4  # Increase from 2
   ```

3. **Add caching** (future enhancement)
   - Implement Redis caching
   - Cache frequent queries

4. **Optimize model**
   - Use model quantization
   - Consider GPU acceleration

---

### Issue: Slow startup time

**Symptoms:**
- Container takes >30 seconds to start
- Health check fails initially

**Solutions:**

1. **Normal behavior**
   - Model loading takes 10-15 seconds
   - Health check has 40s start period

2. **Optimize if needed**
   - Use smaller models
   - Lazy load models
   - Pre-warm models

---

## 🔍 Debugging Tips

### Enable Debug Logging

```python
# main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Container Logs

```bash
# Real-time logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service
docker logs ai-ecommerce
```

### Interactive Container Shell

```bash
# Access running container
docker exec -it ai-ecommerce /bin/bash

# Check files
ls -la
cat .env

# Test Python imports
python -c "import tensorflow; print(tensorflow.__version__)"
```

### Test Individual Components

```bash
# Test Pinecone connection
python -c "from pinecone import Pinecone; pc = Pinecone(api_key='your_key'); print(pc.list_indexes())"

# Test model loading
python -c "import tensorflow as tf; model = tf.keras.models.load_model('ecommerce_cnn_model.h5'); print('Model loaded')"

# Test OCR
tesseract --version
```

---

## 📞 Getting Help

If you're still stuck:

1. **Check Documentation**
   - README.md
   - API_DOCUMENTATION.md
   - DEPLOYMENT.md

2. **Review Logs**
   - Application logs
   - Docker logs
   - System logs

3. **Search Issues**
   - GitHub Issues (if published)
   - Stack Overflow
   - Docker forums

4. **Create an Issue**
   - Include error messages
   - Provide system info
   - Share relevant logs
   - Describe steps to reproduce

---

## 🛠️ Useful Commands

```bash
# Health check
curl http://localhost:5000/health

# Test text search
curl -X POST http://localhost:5000/api/text \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'

# Restart containers
docker-compose restart

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Clean up Docker
docker system prune -a

# View resource usage
docker stats

# Check environment
docker-compose config
```

---

**Still having issues? Check the logs first, then consult the documentation!** 📚
