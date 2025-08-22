# Animal Classification API - Deployment Guide

## 🚀 Deployment on Render

This guide covers deploying the Animal Classification API on Render with memory optimization.

## 📋 Prerequisites

- Render account
- Git repository with your code
- Trained model file (`outputs/best_model.pth`)

## 🔧 Memory Optimization Changes

The API has been optimized to prevent memory overflow during deployment:

### Key Changes Made:

1. **Removed Dataset Loading at Startup**: The app no longer loads the entire dataset during startup
2. **Directory Scanning Only**: Only scans folder names to get class information
3. **Lazy Loading**: Images are only loaded when needed for predictions
4. **Reduced Dependencies**: Removed heavy packages not needed for deployment
5. **Memory Monitoring**: Added memory usage tracking in health endpoint

### Files Modified:

- `main_api.py` - Optimized model loading
- `requirements.txt` - Reduced dependencies
- `start.py` - Memory management improvements
- `render.yaml` - Memory optimization settings

## 🚀 Deployment Steps

### 1. Test Locally First

```bash
# Test memory optimization
python test_memory.py

# Test the API locally
python start.py
```

### 2. Deploy to Render

1. **Connect Repository**: Link your Git repository to Render
2. **Create Web Service**: Use the `render.yaml` configuration
3. **Environment**: Python 3.11
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `python start.py`

### 3. Monitor Deployment

- Check the deployment logs for memory usage
- Use the `/health` endpoint to monitor memory consumption
- Watch for any memory-related errors

## 🔍 Troubleshooting

### Memory Issues

If you still encounter memory problems:

1. **Check Health Endpoint**: `/health` shows memory usage
2. **Reduce Model Size**: Consider using a smaller model
3. **Increase Render Plan**: Upgrade from free to paid plan for more memory
4. **Check Dependencies**: Ensure no unnecessary packages are installed

### Common Errors

```
==> Out of memory (used over 512Mi)
```

**Solutions:**
- Verify `test_memory.py` passes locally
- Check that all optimization changes are deployed
- Monitor memory usage via health endpoint
- Consider reducing model complexity

### Port Binding Issues

```
==> No open ports detected, continuing to scan...
```

**Solutions:**
- Ensure `start.py` binds to `0.0.0.0`
- Check that `PORT` environment variable is set
- Verify uvicorn configuration in `start.py`

## 📊 Memory Monitoring

The `/health` endpoint now provides memory information:

```json
{
  "status": "healthy",
  "model_loaded": true,
  "classes_available": 75,
  "device": "cpu",
  "memory_usage_mb": 245.67,
  "memory_available_mb": 1024.33,
  "memory_percent": 19.35
}
```

## 🧪 Testing Deployment

### 1. Health Check
```bash
curl https://your-app.onrender.com/health
```

### 2. Class Information
```bash
curl https://your-app.onrender.com/classes
```

### 3. Prediction Test
```bash
curl -X POST "https://your-app.onrender.com/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg"
```

## 🔄 Continuous Deployment

- Enable auto-deploy in Render
- Monitor deployment logs for memory issues
- Use health checks to verify deployment success

## 📈 Performance Tips

1. **Model Optimization**: Use model quantization if possible
2. **Image Processing**: Optimize image transformations
3. **Caching**: Consider adding response caching for repeated requests
4. **Monitoring**: Regularly check memory usage patterns

## 🆘 Support

If you continue to experience issues:

1. Check the deployment logs thoroughly
2. Verify all optimization changes are applied
3. Test locally with `test_memory.py`
4. Consider upgrading Render plan for more resources

---

**Note**: The free Render plan has limited memory (512MB). For production use, consider upgrading to a paid plan with more resources.
