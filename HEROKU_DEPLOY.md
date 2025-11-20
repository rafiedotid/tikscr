# 🚀 Deploy ke Heroku (GRATIS & RELIABLE)

## 🎯 Kenapa Heroku?
- ✅ Support Selenium out of the box
- ✅ Chrome buildpacks tersedia
- ✅ Lebih stable dari Railway untuk Selenium
- ✅ GRATIS (dengan limits)

## 📋 Step-by-Step Deploy

### 1. Install Heroku CLI
Download dari: https://devcenter.heroku.com/articles/heroku-cli

### 2. Login Heroku
```bash
heroku login
```

### 3. Create App
```bash
heroku create nama-api-lu
```

### 4. Add Buildpacks (PENTING!)
```bash
heroku buildpacks:add --index 1 heroku/python
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-google-chrome
heroku buildpacks:add --index 3 https://github.com/heroku/heroku-buildpack-chromedriver
```

### 5. Set Environment Variables
```bash
heroku config:set GOOGLE_CHROME_BIN=/app/.chromedriver/bin/chromedriver
heroku config:set CHROMEDRIVER_PATH=/app/.chromedriver/bin/chromedriver
```

### 6. Deploy
```bash
git add .
git commit -m "Deploy TikTok API"
git push heroku main
```

### 7. Test
```bash
curl https://nama-api-lu.herokuapp.com/health
curl https://nama-api-lu.herokuapp.com/api/user/rafiedotid
```

## 🎉 DONE!
API lu live di: `https://nama-api-lu.herokuapp.com`

## 🔧 Troubleshooting

### Jika masih error Chrome:
```bash
heroku logs --tail
```

### Check buildpacks:
```bash
heroku buildpacks
```

### Restart app:
```bash
heroku restart
```

## 💡 Pro Tips
- Heroku free tier: 550 hours/month
- App sleep setelah 30 menit idle
- First request setelah sleep agak lama (cold start)
- Untuk production, upgrade ke paid plan

## 🆚 Heroku vs Railway
| Feature | Heroku | Railway |
|---------|--------|---------|
| Selenium Support | ✅ Excellent | ❌ Problematic |
| Setup Complexity | Medium | Easy |
| Free Hours | 550/month | 500/month |
| Cold Start | Slow | Fast |
| Reliability | High | Medium |

**Recommendation: Pakai Heroku untuk Selenium apps!**