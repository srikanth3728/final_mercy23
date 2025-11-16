# ⚡ Quick Start Guide

## 🏃 Run Locally (2 Commands)

**Terminal 1:**
```bash
python app.py
```

**Terminal 2:**
```bash
python -m http.server 8000
```

Open: `http://localhost:8000`

## 🚀 Deploy to Vercel (3 Steps)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Food app"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repo
   - Add environment variables:
     - `MONGODB_URI` = Your MongoDB Atlas connection string
     - `DB_NAME` = `foodapp`
   - Click "Deploy"

3. **Done!** Your app is live! 🎉

## 📝 Get MongoDB Atlas (Free)

1. Sign up: [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create free cluster
3. Get connection string
4. Add to Vercel environment variables

That's it! Super simple! ✨

