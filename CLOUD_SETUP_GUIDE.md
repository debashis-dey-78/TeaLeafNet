# 🌐 TeaLeafNet Cloud Setup Guide

This guide will help you deploy your tea leaf disease detection app to the cloud using **free** services.

## 🎯 Architecture Overview

```
React Native App → Vercel API → Hugging Face → Results
```

## 📋 Prerequisites

- GitHub account
- Hugging Face account
- Vercel account (free)

## 🚀 Step-by-Step Setup

### 1. Hugging Face Setup (FREE)

1. **Create Account**: Go to [huggingface.co](https://huggingface.co) and sign up
2. **Create Model Repository**:
   - Click "New Model"
   - Name: `tea-leaf-detection`
   - Type: "Model"
   - Visibility: Public
3. **Upload Your Models**:
   - Upload `stage1_nonleaf.tflite` as `leaf-detection.tflite`
   - Upload `stage2_Tea_disease.tflite` as `disease-classification.tflite`
4. **Get API Token**:
   - Go to Settings → Access Tokens
   - Create new token with "Read" permissions
   - Copy the token (you'll need it later)

### 2. Vercel Setup (FREE)

1. **Create Account**: Go to [vercel.com](https://vercel.com) and sign up with GitHub
2. **Deploy Your API**:
   - Push this code to GitHub
   - Connect your GitHub repo to Vercel
   - Vercel will automatically deploy your API
3. **Set Environment Variables**:
   - In Vercel dashboard, go to your project
   - Go to Settings → Environment Variables
   - Add: `HUGGINGFACE_TOKEN` = your token from step 1
4. **Get Your API URL**:
   - After deployment, you'll get a URL like `https://your-app.vercel.app`
   - Update `API_BASE_URL` in `ModelService.ts` with this URL

### 3. Update Your App

1. **Install Dependencies**:
   ```bash
   npm install expo-image-manipulator expo-crypto
   ```

2. **Update API URL**:
   - Open `src/services/ModelService.ts`
   - Replace `https://your-vercel-app.vercel.app/api` with your actual Vercel URL

3. **Test the Integration**:
   ```bash
   npm start
   ```

## 🔧 Alternative: Using Hugging Face Inference API Directly

If you prefer to use Hugging Face's hosted models directly:

### Option A: Use Pre-trained Models
1. Find similar models on Hugging Face Hub
2. Use their Inference API directly
3. No need to upload your own models

### Option B: Convert to ONNX/PyTorch
1. Convert your TensorFlow Lite models to ONNX
2. Upload to Hugging Face
3. Use their Inference API

## 💰 Cost Breakdown (All FREE!)

| Service | Free Tier | Your Usage |
|---------|-----------|------------|
| **Hugging Face** | 1,000 requests/month | ✅ Sufficient for testing |
| **Vercel** | 100GB bandwidth/month | ✅ More than enough |
| **GitHub** | Unlimited public repos | ✅ Perfect |
| **Total** | **$0/month** | 🎉 |

## 🚀 Deployment Commands

```bash
# 1. Install dependencies
npm install

# 2. Test locally
npm start

# 3. Deploy to Vercel (automatic with GitHub)
git add .
git commit -m "Add cloud API"
git push origin main
```

## 🔍 Testing Your Setup

1. **Health Check**: Visit `https://your-app.vercel.app/api/health`
2. **Test Analysis**: Use your React Native app to analyze an image
3. **Check Logs**: Monitor Vercel function logs for any issues

## 🛠️ Troubleshooting

### Common Issues:

1. **CORS Errors**: Make sure your API has proper CORS headers
2. **Image Upload Issues**: Check image size limits (Vercel: 4.5MB)
3. **Hugging Face Errors**: Verify your API token and model names
4. **Network Timeouts**: Increase timeout in `vercel.json`

### Debug Steps:

1. Check Vercel function logs
2. Test API endpoints with Postman/curl
3. Verify environment variables are set
4. Check Hugging Face model status

## 📈 Scaling Up (When You Need More)

When you outgrow the free tiers:

1. **Hugging Face Pro**: $9/month for 10,000 requests
2. **Vercel Pro**: $20/month for more bandwidth
3. **Add Database**: Firebase for user data storage
4. **Add CDN**: CloudFlare for faster image delivery

## 🎉 You're Done!

Your app now runs entirely in the cloud with:
- ✅ Real AI model processing
- ✅ No device storage needed
- ✅ Easy model updates
- ✅ Scalable architecture
- ✅ $0 monthly cost

Happy coding! 🚀
