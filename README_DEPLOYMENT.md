# 🚀 Daily Deployment Guide for DappLooker Script

## 📋 **Overview**
Your `enhanced_dapplooker.py` script can be deployed to run automatically once daily on various platforms. Here are the best options:

---

## 🎯 **Option 1: Render (Recommended)**

### ✅ **Why Render?**
- Native cron job support
- Free tier available
- Easy environment variable management
- Automatic scaling

### 📝 **Setup Steps:**

1. **Create Account**: Sign up at [render.com](https://render.com)

2. **Connect Repository**: 
   - Connect your GitHub repository
   - Render will auto-detect the `render.yaml` file

3. **Set Environment Variables** in Render Dashboard:
   ```bash
   WALLET_PRIVATE_KEY=your_wallet_private_key_here
   IRYS_TOKEN=ethereum
   IRYS_NODE=https://uploader.irys.xyz
   UPLOAD_ENABLED=true
   ```

4. **Deploy**: Render will automatically set up the cron job

### ⏰ **Schedule Options:**
```yaml
# Daily at 6 AM UTC
schedule: "0 6 * * *"

# Daily at midnight UTC  
schedule: "0 0 * * *"

# Daily at 2 PM UTC
schedule: "0 14 * * *"

# Every 12 hours
schedule: "0 */12 * * *"
```

---

## 🎯 **Option 2: GitHub Actions (Free)**

### 📝 **Setup Steps:**

1. **Create Workflow File**: `.github/workflows/daily-fetch.yml`
   ```yaml
   name: Daily DappLooker Fetch
   
   on:
     schedule:
       - cron: '0 6 * * *'  # Daily at 6 AM UTC
     workflow_dispatch:  # Manual trigger
   
   jobs:
     fetch-data:
       runs-on: ubuntu-latest
       
       steps:
       - uses: actions/checkout@v3
       
       - name: Set up Python
         uses: actions/setup-python@v4
         with:
           python-version: '3.9'
           
       - name: Install dependencies
         run: |
           pip install -r requirements.txt
           
       - name: Install Irys CLI
         run: |
           npm install -g @irys/cli
           
       - name: Run DappLooker Script
         env:
           WALLET_PRIVATE_KEY: ${{ secrets.WALLET_PRIVATE_KEY }}
           IRYS_TOKEN: ethereum
           IRYS_NODE: https://uploader.irys.xyz
           UPLOAD_ENABLED: true
         run: python enhanced_dapplooker.py
   ```

2. **Set Repository Secrets**:
   - Go to Settings → Secrets and Variables → Actions
   - Add `WALLET_PRIVATE_KEY` secret

---

## 🎯 **Option 3: Railway**

### 📝 **Setup Steps:**

1. **Create `railway.json`**:
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "python enhanced_dapplooker.py",
       "cronSchedule": "0 6 * * *"
     }
   }
   ```

2. **Deploy**: Connect GitHub repo to Railway

---

## 🎯 **Option 4: Heroku with Scheduler**

### 📝 **Setup Steps:**

1. **Create `Procfile`**:
   ```
   worker: python enhanced_dapplooker.py
   ```

2. **Install Heroku Scheduler Add-on**:
   ```bash
   heroku addons:create scheduler:standard
   ```

3. **Configure Schedule**:
   ```bash
   heroku addons:open scheduler
   # Add job: python enhanced_dapplooker.py
   # Set frequency: Daily at 6:00 AM UTC
   ```

---

## 🎯 **Option 5: AWS Lambda (Advanced)**

### 📝 **Setup Steps:**

1. **Create Lambda Function** with Python runtime
2. **Set up EventBridge Rule** for daily trigger
3. **Package dependencies** in deployment zip
4. **Configure environment variables**

---

## ⚙️ **Environment Variables Required**

All platforms need these environment variables:

```bash
WALLET_PRIVATE_KEY=your_ethereum_private_key
IRYS_TOKEN=ethereum
IRYS_NODE=https://uploader.irys.xyz
UPLOAD_ENABLED=true
```

---

## 📊 **Monitoring & Logs**

### ✅ **What to Monitor:**
- Daily execution success/failure
- File upload to Irys
- Data collection metrics
- Error rates

### 📝 **Log Locations:**
- **Render**: Dashboard → Service → Logs
- **GitHub Actions**: Actions tab → Workflow runs
- **Railway**: Dashboard → Deployments → Logs
- **Heroku**: `heroku logs --tail`

---

## 🔧 **Troubleshooting**

### ❌ **Common Issues:**

1. **Missing Dependencies**:
   ```bash
   # Add to requirements.txt
   requests>=2.31.0
   python-dotenv>=1.0.0
   ```

2. **Irys CLI Not Found**:
   ```bash
   # Install in build step
   npm install -g @irys/cli
   ```

3. **Environment Variables**:
   - Ensure all required vars are set
   - Check secret/variable names match exactly

4. **Timezone Issues**:
   - All cron schedules use UTC
   - Convert your local time to UTC

---

## 🎯 **Recommended: Render Setup**

**Why Render is best for your use case:**
- ✅ Native cron job support
- ✅ Free tier sufficient for daily runs
- ✅ Easy environment variable management
- ✅ Automatic dependency installation
- ✅ Built-in logging and monitoring

**Quick Start:**
1. Push code to GitHub
2. Connect to Render
3. Set environment variables
4. Deploy - it runs automatically daily!

---

## 📅 **Schedule Examples**

```bash
# Every day at 6 AM UTC
"0 6 * * *"

# Every day at midnight UTC
"0 0 * * *"

# Twice daily (6 AM and 6 PM UTC)
"0 6,18 * * *"

# Every weekday at 9 AM UTC
"0 9 * * 1-5"

# Every Sunday at 3 AM UTC
"0 3 * * 0"
```

Your script is ready for daily automated execution! 🚀 