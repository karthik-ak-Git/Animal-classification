# 🚀 Vercel Deployment Guide for Animal Classification API

## 📋 **Prerequisites**

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install with `npm i -g vercel`
3. **Git Repository**: Your code should be in a Git repo

## 🔧 **Setup Steps**

### **Step 1: Install Vercel CLI**
```bash
npm i -g vercel
```

### **Step 2: Login to Vercel**
```bash
vercel login
```

### **Step 3: Deploy to Vercel**
```bash
vercel
```

### **Step 4: Follow the Prompts**
- **Set up and deploy**: Choose `Y`
- **Which scope**: Select your account
- **Link to existing project**: Choose `N`
- **Project name**: `animal-classification-api`
- **Directory**: Press Enter (current directory)
- **Override settings**: Choose `N`

## 🌐 **Deployment Configuration**

### **vercel.json**
- **Max Duration**: 30 seconds
- **Memory**: 3008 MB
- **Routes**: All requests go to `/api/index.py`

### **API Structure**
- **Entry Point**: `api/index.py`
- **Framework**: FastAPI
- **Handler**: Vercel serverless function

## ⚠️ **Important Notes**

### **Model Limitations**
- **Current Setup**: Uses placeholder predictions (no actual model loading)
- **Reason**: Vercel has 50MB function size limit
- **Your Model**: 43MB (too close to limit)

### **Solutions for Full Model Deployment**

#### **Option 1: Model Quantization**
```python
# Reduce model size by 50-70%
torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
```

#### **Option 2: External Model Hosting**
- **Hugging Face**: Host model separately
- **AWS S3**: Store model in cloud storage
- **Google Cloud**: Use Cloud Storage

#### **Option 3: Lightweight Model**
- Use MobileNet or EfficientNet
- Smaller architecture
- Faster inference

## 🔄 **Update Frontend for Vercel**

### **Update API URLs**
```javascript
// In frontend/scripts.js, change:
const API_BASE = 'https://your-app.vercel.app';

// Update fetch calls:
fetch(`${API_BASE}/classes`)
fetch(`${API_BASE}/predict`)
fetch(`${API_BASE}/feedback`)
```

## 📊 **Deployment Commands**

### **Deploy to Production**
```bash
vercel --prod
```

### **Deploy to Preview**
```bash
vercel
```

### **List Deployments**
```bash
vercel ls
```

### **Remove Project**
```bash
vercel remove animal-classification-api
```

## 🧪 **Testing After Deployment**

### **Health Check**
```bash
curl https://your-app.vercel.app/health
```

### **Classes Endpoint**
```bash
curl https://your-app.vercel.app/classes
```

### **Frontend**
Visit: `https://your-app.vercel.app/`

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Build Failures**
   - Check `requirements.txt` compatibility
   - Ensure all imports are available

2. **Function Timeout**
   - Increase `maxDuration` in `vercel.json`
   - Optimize code for faster execution

3. **Memory Issues**
   - Reduce model size
   - Use lazy loading
   - Optimize imports

### **Performance Tips**

1. **Cold Start Optimization**
   - Keep dependencies minimal
   - Use lightweight frameworks

2. **Memory Management**
   - Load models on demand
   - Clear variables after use

3. **Caching**
   - Use Vercel's edge caching
   - Implement response caching

## 🎯 **Next Steps**

1. **Deploy current version** (with placeholder predictions)
2. **Test all endpoints**
3. **Implement actual model loading** (choose one of the solutions above)
4. **Optimize for production**

## 📞 **Support**

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **FastAPI Docs**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Community**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)

---

**🎉 Your Animal Classification API is now ready for Vercel deployment!**
