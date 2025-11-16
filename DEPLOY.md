# 🚀 Deploy to Vercel - Simple Guide

## Step 1: Push to GitHub

1. Create a new repository on GitHub
2. Push your code:
```bash
git init
git add .
git commit -m "Food app with Flask + MongoDB"
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

## Step 2: Deploy to Vercel

### Option A: Via Vercel Dashboard (Easiest)

1. Go to [vercel.com](https://vercel.com) and sign up/login
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Vercel will auto-detect Python
5. **Add Environment Variables:**
   - `MONGODB_URI` = Your MongoDB Atlas connection string
   - `DB_NAME` = `foodapp`
6. Click **"Deploy"**
7. Done! Your app is live! 🎉

### Option B: Via Vercel CLI

```bash
npm install -g vercel
vercel login
vercel
```

Follow prompts and add environment variables when asked.

## Step 3: Set MongoDB Atlas (Free)

1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up (Free tier available)
3. Create a cluster (Free M0)
4. Get connection string: `mongodb+srv://username:password@cluster.mongodb.net/`
5. Add to Vercel environment variables as `MONGODB_URI`

## ✅ That's It!

Your app will be live at: `https://your-project.vercel.app`

The frontend automatically uses `/api` when deployed (no code changes needed!)

