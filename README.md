# 🆓 TikTok Stats API - FREE Deployment

## 🎯 What This Does
API gratis untuk scrape statistik TikTok user dari tokcount.com

## 📁 Files (Simple!)
```
├── app.py                           # Main API (siap deploy!)
├── tokcount_scraper_fixed_digits.py # Scraper yang working
├── requirements.txt                 # Dependencies
├── Procfile                        # For Heroku
├── test_api.py                     # Test script
└── README.md                       # This file
```

## 🚀 Deploy GRATIS (Pilih salah satu)

### Option 1: Railway (RECOMMENDED - Paling Gampang)
1. Push code ke GitHub
2. Login ke https://railway.app
3. Connect GitHub repo
4. Deploy otomatis!
5. DONE! ✅

### Option 2: Heroku
```bash
# Install Heroku CLI dulu
git init
git add .
git commit -m "TikTok API"
heroku create your-tiktok-api
git push heroku main
```

### Option 3: Render
1. Connect GitHub di https://render.com
2. Choose "Web Service"
3. Deploy!

## 🧪 Test Local
```bash
# Install dependencies
pip install -r requirements.txt

# Run API
python app.py

# Test
python test_api.py
```

## 📡 API Endpoints

### Get Single User
```bash
GET /api/user/rafiedotid

Response:
{
  "username": "rafiedotid",
  "followers": "12,850",
  "likes": "3,424",
  "following": "13",
  "videos": "18",
  "success": true
}
```

### POST Request
```bash
POST /api/user
Body: {"username": "rafiedotid"}
```

### Batch Users (max 2)
```bash
POST /api/batch
Body: {"usernames": ["user1", "user2"]}
```

## 💰 Cost
**$0** - Completely FREE!

## 🎉 Live Example
After deployment, your API will be available at:
- Railway: `https://your-app.railway.app`
- Heroku: `https://your-app.herokuapp.com`
- Render: `https://your-app.onrender.com`

## 🔧 How It Works
1. Uses Selenium + Chrome (auto-installed on cloud platforms)
2. Scrapes tokcount.com with digit collection method
3. Returns clean JSON response
4. Handles dynamic content loading

## ⚡ Quick Start
1. **Fork this repo**
2. **Deploy to Railway/Heroku/Render**
3. **Test your API**
4. **PROFIT!** 🎉

No VPS needed! No money needed! Just deploy and use!