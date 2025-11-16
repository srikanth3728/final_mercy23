# 🔧 Complete Vercel Deployment Fix Guide

## Issues Identified and Fixed

### 1. **Path Handling in Handler**
- **Problem:** Handler was removing `/api` prefix, but Flask routes expect it
- **Fix:** Handler now preserves the full path including `/api` prefix

### 2. **Vercel Configuration**
- **Problem:** Routing might not be prioritizing static files correctly
- **Fix:** Updated `vercel.json` with proper build configuration and route ordering

### 3. **Request Format**
- **Problem:** Handler needed to properly handle Vercel's request format
- **Fix:** Enhanced handler to correctly extract path, method, headers, and body

## Current Configuration

### `vercel.json`
- Uses `builds` to specify Python function
- Routes `/api/*` to Python handler
- Routes static files (HTML, CSS, JS) directly
- Falls back to `index.html` for SPA routing

### `api/index.py`
- Properly extracts request data from Vercel format
- Preserves `/api` prefix for Flask routes
- Converts to WSGI format for Flask
- Returns proper Vercel response format

## Deployment Checklist

### ✅ Before Deploying

1. **Environment Variables** (Set in Vercel Dashboard):
   ```
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
   DB_NAME=foodapp
   ```

2. **Files in Repository**:
   - ✅ `api/index.py` - Serverless function handler
   - ✅ `app.py` - Flask application
   - ✅ `index.html` - Frontend
   - ✅ `style.css` - Styles
   - ✅ `script.js` - Frontend JavaScript
   - ✅ `requirements.txt` - Python dependencies
   - ✅ `vercel.json` - Vercel configuration

3. **MongoDB Atlas Setup**:
   - Network Access: Allow from anywhere (0.0.0.0/0)
   - Database User: Created with read/write permissions
   - Connection string: Valid and tested

### 🚀 Deployment Steps

1. **Commit and Push**:
   ```bash
   git add .
   git commit -m "Fix Vercel deployment - correct path handling"
   git push origin main
   ```

2. **Vercel Auto-Deploy**:
   - Vercel will automatically detect the push and redeploy
   - Monitor the deployment in Vercel dashboard

3. **Verify Deployment**:
   - Check build logs for errors
   - Check function logs for runtime errors

## Testing After Deployment

### Test URLs:

1. **Homepage**: `https://your-project.vercel.app/`
   - Should show the food booking app

2. **API Health**: `https://your-project.vercel.app/api/health`
   - Should return: `{"status": "ok"}`

3. **API Menu**: `https://your-project.vercel.app/api/menu`
   - Should return menu items JSON

4. **Static Files**:
   - `https://your-project.vercel.app/style.css` - Should load CSS
   - `https://your-project.vercel.app/script.js` - Should load JS

## Troubleshooting

### Still Getting 404?

#### Check 1: Vercel Function Logs
1. Go to Vercel Dashboard → Your Project → Functions
2. Click on `api/index.py`
3. Check "Logs" tab for errors
4. Look for: `Handler called: method=GET, path=/api/health`

#### Check 2: Build Logs
1. Go to Vercel Dashboard → Your Project → Deployments
2. Click on latest deployment
3. Check "Build Logs" for any errors
4. Verify Python dependencies installed correctly

#### Check 3: Environment Variables
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Verify `MONGODB_URI` and `DB_NAME` are set
3. Make sure they're set for "Production" environment

#### Check 4: MongoDB Connection
1. Check function logs for MongoDB connection errors
2. Verify MongoDB Atlas network access allows 0.0.0.0/0
3. Test connection string locally

#### Check 5: Static Files
1. Open browser DevTools → Network tab
2. Reload page
3. Check if `index.html`, `style.css`, `script.js` load (status 200)
4. If 404, files might not be in repository

### Common Errors

#### Error: "Module not found"
- **Cause**: Missing dependency in `requirements.txt`
- **Fix**: Add missing package to `requirements.txt`

#### Error: "MongoDB connection failed"
- **Cause**: Invalid connection string or network access
- **Fix**: Verify MongoDB URI and network settings

#### Error: "Handler not found"
- **Cause**: Function file not in correct location
- **Fix**: Ensure `api/index.py` exists and has `handler` function

#### Error: "Path not found" (Flask 404)
- **Cause**: Path mismatch between Vercel routing and Flask routes
- **Fix**: Check handler logs to see what path is being received

## Debug Mode

The handler now includes debug logging. Check Vercel function logs to see:
- What path is being received
- What method is being used
- Any errors during processing

## Next Steps

If still having issues:

1. **Check Function Logs**: Look for the debug message `Handler called: method=..., path=...`
2. **Test API Directly**: Try accessing `/api/health` directly
3. **Check Static Files**: Verify `index.html` loads when accessing root URL
4. **Review Build Output**: Check what files Vercel is deploying

## File Structure

```
/
├── api/
│   └── index.py          # Vercel serverless function (handler)
├── app.py                # Flask application
├── index.html           # Frontend HTML
├── style.css            # Styles
├── script.js            # Frontend JavaScript
├── requirements.txt     # Python dependencies
└── vercel.json          # Vercel configuration
```

## Important Notes

- **Python Version**: Vercel uses Python 3.12 (as shown in build log)
- **Cold Starts**: First request after inactivity may be slow
- **Static Files**: Must be in root directory (not in subdirectory)
- **Environment Variables**: Must be set in Vercel dashboard, not `.env` file

