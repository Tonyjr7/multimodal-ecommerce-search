# Deployment Guide

This guide covers various deployment options for the AI E-commerce Search application.

## Table of Contents
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Production Checklist](#production-checklist)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

---

## Docker Deployment

### Local Docker

1. **Build the image**:
   ```bash
   docker build -t ai-ecommerce:latest .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     --name ai-ecommerce \
     -p 5000:5000 \
     -e PINECONE_API_KEY=your_key_here \
     -v $(pwd)/ecommerce_cnn_model.h5:/app/ecommerce_cnn_model.h5:ro \
     -v $(pwd)/class_names.pkl:/app/class_names.pkl:ro \
     -v $(pwd)/datasets:/app/datasets:ro \
     ai-ecommerce:latest
   ```

3. **Check logs**:
   ```bash
   docker logs -f ai-ecommerce
   ```

### Docker Compose

1. **Start services**:
   ```bash
   docker-compose up -d
   ```

2. **View logs**:
   ```bash
   docker-compose logs -f
   ```

3. **Stop services**:
   ```bash
   docker-compose down
   ```

4. **Rebuild after changes**:
   ```bash
   docker-compose up --build -d
   ```

---

## Cloud Deployment

### AWS ECS (Elastic Container Service)

1. **Push to ECR**:
   ```bash
   # Authenticate
   aws ecr get-login-password --region us-east-1 | \
     docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   
   # Tag and push
   docker tag ai-ecommerce:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-ecommerce:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-ecommerce:latest
   ```

2. **Create ECS Task Definition**:
   - Use the pushed image
   - Set environment variables
   - Configure health checks
   - Allocate 2 vCPU, 4GB RAM

3. **Create ECS Service**:
   - Use Application Load Balancer
   - Enable auto-scaling
   - Set desired count: 2+

### Google Cloud Run

1. **Build and push**:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/ai-ecommerce
   ```

2. **Deploy**:
   ```bash
   gcloud run deploy ai-ecommerce \
     --image gcr.io/PROJECT_ID/ai-ecommerce \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars PINECONE_API_KEY=your_key \
     --memory 4Gi \
     --cpu 2
   ```

### Azure Container Instances

1. **Create resource group**:
   ```bash
   az group create --name ai-ecommerce-rg --location eastus
   ```

2. **Deploy container**:
   ```bash
   az container create \
     --resource-group ai-ecommerce-rg \
     --name ai-ecommerce \
     --image your-registry/ai-ecommerce:latest \
     --cpu 2 \
     --memory 4 \
     --ports 5000 \
     --environment-variables PINECONE_API_KEY=your_key
   ```

### Heroku

1. **Login and create app**:
   ```bash
   heroku login
   heroku create ai-ecommerce-app
   ```

2. **Set environment variables**:
   ```bash
   heroku config:set PINECONE_API_KEY=your_key
   ```

3. **Deploy**:
   ```bash
   heroku container:push web
   heroku container:release web
   ```

### DigitalOcean App Platform

1. **Create app.yaml**:
   ```yaml
   name: ai-ecommerce
   services:
   - name: web
     dockerfile_path: Dockerfile
     github:
       repo: your-username/ai-ecommerce
       branch: main
     envs:
     - key: PINECONE_API_KEY
       value: ${PINECONE_API_KEY}
     instance_size_slug: professional-s
     http_port: 5000
   ```

2. **Deploy via CLI or web interface**

---

## Production Checklist

### Security
- [ ] Use HTTPS/TLS certificates
- [ ] Implement API authentication
- [ ] Enable CORS properly
- [ ] Use secrets management (AWS Secrets Manager, etc.)
- [ ] Regular security updates
- [ ] Rate limiting
- [ ] Input validation

### Performance
- [ ] Enable caching (Redis)
- [ ] Use CDN for static assets
- [ ] Optimize model loading
- [ ] Database connection pooling
- [ ] Horizontal scaling
- [ ] Load balancing

### Monitoring
- [ ] Application logs (CloudWatch, Stackdriver)
- [ ] Error tracking (Sentry)
- [ ] Performance monitoring (New Relic, Datadog)
- [ ] Health check endpoints
- [ ] Uptime monitoring
- [ ] Cost monitoring

### Reliability
- [ ] Auto-scaling configuration
- [ ] Backup strategy
- [ ] Disaster recovery plan
- [ ] Multi-region deployment
- [ ] Database replication
- [ ] Graceful shutdown

### Configuration
- [ ] Environment-specific configs
- [ ] Proper logging levels
- [ ] Resource limits
- [ ] Timeout configurations
- [ ] Worker/thread tuning

---

## Monitoring

### Health Checks

Monitor the `/health` endpoint:
```bash
curl http://your-domain.com/health
```

Expected response:
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

### Logging

Application logs include:
- Request/response logs
- Error traces
- Model loading status
- Performance metrics

**View logs**:
```bash
# Docker
docker logs -f ai-ecommerce

# Docker Compose
docker-compose logs -f

# Kubernetes
kubectl logs -f deployment/ai-ecommerce
```

### Metrics to Monitor

1. **Application Metrics**:
   - Request rate
   - Response time
   - Error rate
   - Success rate by endpoint

2. **System Metrics**:
   - CPU usage
   - Memory usage
   - Disk I/O
   - Network traffic

3. **Business Metrics**:
   - Search queries per day
   - Popular search methods
   - Average confidence scores
   - User engagement

---

## Troubleshooting

### Container Won't Start

**Check logs**:
```bash
docker logs ai-ecommerce
```

**Common issues**:
- Missing environment variables
- Model files not found
- Port already in use
- Insufficient memory

### High Memory Usage

**Solutions**:
- Increase container memory limit
- Optimize model loading
- Implement model caching
- Use smaller batch sizes

### Slow Response Times

**Diagnose**:
- Check network latency
- Monitor database queries
- Profile model inference time
- Check resource utilization

**Solutions**:
- Add caching layer
- Optimize model
- Scale horizontally
- Use GPU acceleration

### Connection to Pinecone Fails

**Check**:
- API key is correct
- Network connectivity
- Pinecone service status
- Index exists and is ready

### OCR Not Working

**Verify**:
- Tesseract is installed
- Image format is supported
- Image quality is sufficient
- Proper permissions

---

## Scaling Strategies

### Vertical Scaling
- Increase CPU/memory
- Use GPU instances
- Optimize code

### Horizontal Scaling
- Multiple container instances
- Load balancer
- Session management
- Stateless design

### Database Scaling
- Read replicas
- Caching layer
- Connection pooling
- Query optimization

---

## Backup and Recovery

### Model Files
- Store in S3/Cloud Storage
- Version control
- Regular backups
- Disaster recovery plan

### Configuration
- Infrastructure as Code (Terraform)
- Version control
- Environment parity
- Rollback procedures

---

## Cost Optimization

1. **Right-sizing**: Match resources to actual usage
2. **Auto-scaling**: Scale down during low traffic
3. **Reserved instances**: For predictable workloads
4. **Spot instances**: For non-critical workloads
5. **Caching**: Reduce API calls and compute
6. **Monitoring**: Track and optimize costs

---

## Support

For deployment issues:
1. Check logs first
2. Review this guide
3. Check GitHub issues
4. Open a new issue with details

---

**Happy Deploying! 🚀**
