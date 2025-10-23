# 🐳 Docker Deployment Guide

## Quick Start

### Using Docker Compose (Recommended)

1. **Build and start the application:**
   ```bash
   docker-compose up -d
   ```

2. **Access the application:**
   - Main App: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - TensorBoard: http://localhost:6006 (if enabled)

3. **View logs:**
   ```bash
   docker-compose logs -f animal-classifier
   ```

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

### Using Docker (Manual)

1. **Build the image:**
   ```bash
   docker build -t animal-classifier:latest .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name animal-classifier \
     -p 8000:8000 \
     -v $(pwd)/dataset:/app/dataset:ro \
     -v $(pwd)/outputs:/app/outputs \
     -v $(pwd)/logs:/app/logs \
     animal-classifier:latest
   ```

3. **Stop the container:**
   ```bash
   docker stop animal-classifier
   docker rm animal-classifier
   ```

## Configuration

### Environment Variables

- `PORT`: Server port (default: 8000)
- `PYTHONUNBUFFERED`: Enable Python unbuffered output (default: 1)

### Volumes

- `./dataset:/app/dataset:ro` - Dataset (read-only)
- `./outputs:/app/outputs` - Model weights and feedback data
- `./logs:/app/logs` - TensorBoard logs

## Monitoring

### Enable TensorBoard

```bash
docker-compose --profile monitoring up -d
```

### Health Check

```bash
curl http://localhost:8000/health
```

## Production Deployment

### Using Docker Hub

1. **Tag and push:**
   ```bash
   docker tag animal-classifier:latest yourusername/animal-classifier:latest
   docker push yourusername/animal-classifier:latest
   ```

2. **Pull and run on server:**
   ```bash
   docker pull yourusername/animal-classifier:latest
   docker run -d -p 8000:8000 yourusername/animal-classifier:latest
   ```

## Troubleshooting

### Container won't start
```bash
docker logs animal-classifier
```

### Rebuild without cache
```bash
docker-compose build --no-cache
```

### Clear volumes
```bash
docker-compose down -v
```
