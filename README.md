# 🍽️ Food Booking App

Simple food ordering app with Flask backend + MongoDB, ready for Vercel deployment.

## 🚀 Quick Start

### Option 1: Easy Run (Windows)
```bash
run.bat
```
This will install dependencies and start both servers automatically!

### Option 2: Manual Run

**1. Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. Start backend (Terminal 1):**
```bash
python app.py
```
Runs on `http://localhost:5000`

**3. Start frontend (Terminal 2):**
```bash
python -m http.server 8000
```
Runs on `http://localhost:8000`

**4. Open browser:**
Go to `http://localhost:8000`

## 📦 MongoDB Setup

### Option A: MongoDB Atlas (Cloud - Recommended for Vercel)
1. Sign up at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas) (Free)
2. Create cluster → Get connection string
3. Create `.env` file:
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
DB_NAME=foodapp
```

### Option B: Local MongoDB
1. Install MongoDB locally
2. Create `.env` file:
```
MONGODB_URI=mongodb://localhost:27017/
DB_NAME=foodapp
```

**Note:** If no `.env` file, it uses local MongoDB by default.

## 🌐 Deploy to Vercel (Free Hosting)

**Super Simple - Just 3 Steps:**

1. **Push to GitHub** (create repo and push code)

2. **Go to [vercel.com](https://vercel.com)** → Import GitHub repo

3. **Add Environment Variables:**
   - `MONGODB_URI` = Your MongoDB Atlas connection string
   - `DB_NAME` = `foodapp`

4. **Click Deploy** → Done! 🎉

**Get MongoDB Atlas (Free):**
- Sign up at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
- Create free cluster → Get connection string

**See `DEPLOY.md` for detailed instructions!**

## 📁 Project Structure

```
├── app.py              # Flask backend
├── api/index.py        # Vercel serverless function
├── index.html          # Frontend
├── style.css           # Styles
├── script.js           # Frontend + API calls
├── requirements.txt    # Python packages
├── vercel.json         # Vercel config
├── env.example         # Environment template
└── run.bat             # Easy run script (Windows)
```

## 🔌 API Endpoints

- `GET /api/health` - Health check
- `GET /api/menu` - Get menu items
- `POST /api/orders` - Create order
- `GET /api/orders` - Get all orders

## ✨ Features

- 🍕 Menu from MongoDB
- 🛒 Shopping cart
- 📝 Order booking
- 💾 Orders saved to MongoDB
- 📱 Responsive design
- 🚀 Vercel ready

## 📝 Files

- `app.py` - Flask backend with MongoDB
- `script.js` - Frontend with API integration
- `vercel.json` - Vercel deployment config

