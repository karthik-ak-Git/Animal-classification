# Vercel Deployment Guide for Animal Classification Project

## Project Overview
This is a PyTorch-based animal classification web application with:
- **Backend**: FastAPI with PyTorch ResNet18 model
- **Frontend**: HTML/CSS/JS with Bootstrap 5
- **Features**: Image classification, feedback system, breed suggestions

## Files Prepared for Vercel Deployment

### 1. `vercel.json` - Vercel Configuration
```json
{
  "functions": {
    "api/index.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ],
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ]
}
```

### 2. `requirements-vercel.txt` - Python Dependencies
Optimized for Vercel with reduced PyTorch version to avoid size limits.

### 3. `api/index.py` - Main API Entry Point
Serverless function that handles all API routes and serves the frontend.

### 4. `.vercelignore` - Files to Exclude
Excludes large dataset, logs, and cache files from deployment.

## Deployment Steps

### 1. Prerequisites
- Install Vercel CLI: `npm install -g vercel`
- Create Vercel account at https://vercel.com

### 2. Prepare Model File
**Important**: The model file (`outputs/best_model.pth`) needs to be included in deployment:

```bash
# Ensure model exists and is not too large (Vercel has 50MB limit per function)
ls -la outputs/best_model.pth
```

If model is too large, consider:
- Model quantization
- Using a smaller architecture
- Hosting model externally (S3, Hugging Face, etc.)

### 3. Deploy to Vercel

#### Option A: CLI Deployment
```bash
# Navigate to project directory
cd d:\Animal-classification

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Link to existing project or create new
# - Confirm settings
```

#### Option B: GitHub Integration
1. Push code to GitHub repository
2. Connect GitHub repo to Vercel dashboard
3. Auto-deploy on push

### 4. Environment Configuration
If needed, set environment variables in Vercel dashboard:
- Go to Project Settings → Environment Variables
- Add any required variables

## API Endpoints

Once deployed, your app will have these endpoints:

- `GET /` - Main web interface
- `POST /predict` - Image classification
- `POST /feedback` - Submit corrections
- `GET /classes` - Get available animal classes
- `GET /health` - Health check

## Potential Issues & Solutions

### 1. Model File Size
**Problem**: Model file too large for Vercel
**Solutions**:
- Use model quantization
- Host model externally
- Use a smaller model architecture

### 2. Cold Start Performance
**Problem**: First request is slow
**Solutions**:
- Use Vercel Pro for better performance
- Implement model caching
- Consider warming functions

### 3. Missing Dependencies
**Problem**: Import errors during deployment
**Solutions**:
- Check `requirements-vercel.txt`
- Ensure all custom modules are included
- Test locally with minimal environment

### 4. File Path Issues
**Problem**: File not found errors
**Solutions**:
- Use absolute paths with `os.path.join()`
- Check file structure in deployed environment
- Use environment-specific paths

## Testing Deployment

After deployment:

1. **Test main page**: Visit the deployed URL
2. **Test image upload**: Try uploading an animal image
3. **Test API endpoints**: Use curl or Postman
4. **Check logs**: Monitor Vercel function logs for errors

## Performance Optimization

1. **Model Optimization**:
   - Use TorchScript for faster inference
   - Consider ONNX conversion
   - Implement model caching

2. **Frontend Optimization**:
   - Compress images and assets
   - Use CDN for static files
   - Implement lazy loading

3. **API Optimization**:
   - Add response caching
   - Optimize image preprocessing
   - Use async operations

## Monitoring & Maintenance

1. **Monitor Function Performance**:
   - Check Vercel dashboard for metrics
   - Monitor function execution time
   - Watch for errors and timeouts

2. **Update Model**:
   - Retrain model periodically
   - Deploy updated model files
   - Version control model updates

## Alternative Deployment Options

If Vercel doesn't work well:

1. **Heroku**: Better for larger applications
2. **Google Cloud Run**: Good for containerized apps
3. **AWS Lambda**: Similar serverless approach
4. **Railway**: Simple deployment platform
5. **Render**: Alternative to Heroku

## Next Steps

1. Deploy and test
2. Monitor performance
3. Optimize based on usage
4. Consider scaling solutions if needed
5. Implement CI/CD pipeline for updates
