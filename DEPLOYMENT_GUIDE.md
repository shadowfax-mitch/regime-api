# 🚀 Regime API Deployment Guide

**Goal:** Get the Regime Classifier API from localhost to production in under 30 minutes.

---

## 📋 Pre-Deployment Checklist

### ✅ Requirements
- [ ] Python 3.10+ installed locally
- [ ] Git repository created (GitHub/GitLab)
- [ ] Render.com account (or Railway/Fly.io)
- [ ] `regime_data.csv` accessible (or mock data for testing)
- [ ] Domain name ready (optional, Render provides free subdomain)

### ✅ Files Ready
- [ ] `app/main.py` (FastAPI app)
- [ ] `requirements.txt` (dependencies)
- [ ] `Dockerfile` (optional, for Docker deployment)
- [ ] `render.yaml` (Render config)
- [ ] `.env.example` (environment variables template)

---

## 🧪 Step 1: Test Locally

### 1.1 Install Dependencies

```bash
cd /home/shado/.openclaw/workspace/products/regime-api

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 1.2 Set Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env
nano .env
```

**Minimal .env for local testing:**
```bash
REGIME_DATA_PATH=/mnt/c/NinjaTrader/data/regime_data.csv
ADMIN_KEY=test_admin_key_123
```

If `regime_data.csv` doesn't exist, create mock data:

```bash
cat > /tmp/regime_data.csv << 'EOF'
Date,Regime,AccelZ,DivZ,SignalStrength
2026-02-15,STABLE,0.12,0.45,0.45
2026-02-16,STABLE,0.08,0.32,0.32
2026-02-17,FRAGILE_DIV,0.45,2.1,2.1
2026-02-18,STABLE,0.23,0.67,0.67
2026-02-19,STABLE,0.11,0.39,0.39
EOF

export REGIME_DATA_PATH=/tmp/regime_data.csv
```

### 1.3 Run Locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 1.4 Test Endpoints

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Expected:** `{"status":"healthy",...}`

**Current Regime (with demo API key):**
```bash
curl -H "X-API-Key: demo_free_key" http://localhost:8000/regime/current
```

**Expected:** JSON response with regime data

**Swagger Docs:**
Open browser: http://localhost:8000/docs

✅ **If all tests pass, proceed to deployment!**

---

## 🚢 Step 2: Deploy to Render

### 2.1 Push to GitHub

```bash
# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit - Regime API"

# Create repo on GitHub, then:
git remote add origin https://github.com/your-username/regime-api.git
git push -u origin main
```

### 2.2 Connect to Render

1. Go to [render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your `regime-api` repository

### 2.3 Configure Web Service

**Settings:**
- **Name:** `regime-api`
- **Region:** Oregon (US West) or closest to you
- **Branch:** `main`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Instance Type:**
- **Free** (for MVP — 512 MB RAM, sleeps after 15 min inactivity)
- Upgrade to **Starter ($7/mo)** for always-on

### 2.4 Set Environment Variables

Click **"Environment"** tab, add:

| Key | Value |
|-----|-------|
| `REGIME_DATA_PATH` | `/opt/render/project/data/regime_data.csv` |
| `ADMIN_KEY` | `[generate secure random string]` |
| `PYTHON_VERSION` | `3.11.0` |

**⚠️ Important:** You'll need to upload `regime_data.csv` to Render. Two options:

**Option A: Include in Git (if data is not too large)**
```bash
mkdir -p data
cp /mnt/c/NinjaTrader/data/regime_data.csv data/
git add data/regime_data.csv
git commit -m "Add regime data"
git push
```

Then set: `REGIME_DATA_PATH=/opt/render/project/src/data/regime_data.csv`

**Option B: Use Render Disk (persistent storage, $1/GB/mo)**
1. Click "Disks" → "Add Disk"
2. Name: `regime-data`, Size: 1 GB, Mount Path: `/data`
3. SSH into Render shell: `render shell regime-api`
4. Upload file: `scp regime_data.csv user@render:/data/`
5. Set: `REGIME_DATA_PATH=/data/regime_data.csv`

### 2.5 Deploy

Click **"Create Web Service"**

Render will:
1. Clone your repo
2. Install dependencies
3. Start the app
4. Assign a URL: `https://regime-api-xxxx.onrender.com`

**Deployment takes ~2-5 minutes.**

### 2.6 Verify Deployment

```bash
# Test health endpoint
curl https://regime-api-xxxx.onrender.com/health

# Test current regime
curl -H "X-API-Key: demo_free_key" \
  https://regime-api-xxxx.onrender.com/regime/current
```

✅ **If both return 200 OK, you're live!**

---

## 🌐 Step 3: Custom Domain (Optional)

### 3.1 Add Custom Domain in Render

1. Go to your service → "Settings" → "Custom Domains"
2. Click "Add Custom Domain"
3. Enter: `api.sentinel-algo.com`

### 3.2 Configure DNS

Add a CNAME record in your DNS provider (Namecheap, Cloudflare, etc.):

| Type | Name | Value |
|------|------|-------|
| CNAME | api | regime-api-xxxx.onrender.com |

**Propagation:** Takes 5-60 minutes

### 3.3 Enable SSL

Render auto-provisions SSL certificates (Let's Encrypt) — no action needed!

**Verify:**
```bash
curl https://api.sentinel-algo.com/health
```

---

## 🔥 Step 4: Set Up Monitoring

### 4.1 Enable Render Notifications

1. Go to "Settings" → "Notifications"
2. Enable "Deploy Notifications" → Add your email
3. Enable "Health Check Failures" → Add your email

### 4.2 Set Up Uptime Monitoring (Free)

Use [UptimeRobot](https://uptimerobot.com) (free for 50 monitors):

1. Create account
2. Add monitor:
   - **Type:** HTTP(s)
   - **URL:** `https://api.sentinel-algo.com/health`
   - **Name:** Regime API Health
   - **Interval:** 5 minutes
3. Add alert contact (email, Slack, Discord webhook)

### 4.3 Set Up Error Tracking (Optional)

**Sentry (free for 5K errors/month):**

```bash
pip install sentry-sdk[fastapi]
```

Add to `app/main.py` (before `app = FastAPI(...)`):

```python
import sentry_sdk
sentry_sdk.init(
    dsn="https://your-sentry-dsn@sentry.io/project-id",
    traces_sample_rate=0.1,
)
```

Redeploy to enable Sentry.

---

## 📊 Step 5: Integrate Stripe (for Payments)

### 5.1 Create Stripe Account

1. Go to [stripe.com](https://stripe.com)
2. Create account (or use existing)
3. Get API keys: Dashboard → Developers → API Keys

### 5.2 Add Stripe Dependency

```bash
echo "stripe==11.2.0" >> requirements.txt
```

### 5.3 Create Pricing Plans in Stripe

1. Go to "Products" → "Add Product"
2. Create 3 products:
   - **Basic:** $19/mo, recurring
   - **Pro:** $49/mo, recurring
   - **Enterprise:** $199/mo, recurring

Copy the **Price IDs** (e.g., `price_1ABC123...`)

### 5.4 Add Stripe Key to Render

Environment Variables:

| Key | Value |
|-----|-------|
| `STRIPE_SECRET_KEY` | `sk_live_...` (from Stripe dashboard) |

### 5.5 Build Payment Flow (Future Phase)

You'll need:
- Stripe Checkout session endpoint (`POST /billing/create-checkout`)
- Webhook endpoint (`POST /billing/webhook`) to handle subscription events
- Database to store user subscriptions

**For MVP:** Skip this, manually create test API keys for early users.

---

## 🧪 Step 6: Production Testing

### 6.1 Load Test (Optional)

```bash
# Install Apache Bench
sudo apt install apache2-utils  # Ubuntu/Debian
# or: brew install httpd (macOS)

# Test 1000 requests, 10 concurrent
ab -n 1000 -c 10 -H "X-API-Key: demo_free_key" \
  https://api.sentinel-algo.com/regime/current
```

**Goal:** 
- Average response time < 500ms
- 0% failed requests

If fails, upgrade Render instance to Starter ($7/mo).

### 6.2 Security Audit

```bash
# Test without API key (should return 401)
curl https://api.sentinel-algo.com/regime/current

# Test with invalid API key (should return 401)
curl -H "X-API-Key: invalid_key_123" \
  https://api.sentinel-algo.com/regime/current

# Test rate limiting (make 101 requests rapidly)
for i in {1..101}; do
  curl -H "X-API-Key: demo_free_key" \
    https://api.sentinel-algo.com/regime/current
done
# Should see 429 error on request #101
```

---

## 🚨 Troubleshooting

### Issue: "Module not found" error on Render

**Fix:** Make sure `requirements.txt` includes all dependencies.

```bash
# Regenerate requirements
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Issue: "regime_data.csv not found"

**Fix:** Check `REGIME_DATA_PATH` environment variable matches actual file location.

```bash
# SSH into Render
render shell regime-api

# Check file exists
ls -la /opt/render/project/data/regime_data.csv
```

### Issue: API returns 503 "Service Unavailable"

**Fix:** Check Render logs:

1. Go to Render dashboard → your service
2. Click "Logs" tab
3. Look for Python errors

Common causes:
- Missing environment variable
- File path issue
- Out of memory (upgrade instance)

### Issue: Free tier sleeps after 15 minutes

**Expected behavior** on Render free tier. Two options:
1. **Upgrade to Starter ($7/mo)** for always-on
2. **Use cron job** to ping API every 10 minutes (keeps it awake)

```bash
# Add to your server's crontab
*/10 * * * * curl https://api.sentinel-algo.com/health > /dev/null 2>&1
```

---

## 📈 Post-Deployment

### ✅ Launch Checklist

- [ ] API live at `https://api.sentinel-algo.com`
- [ ] All endpoints tested (current, history, transitions)
- [ ] Rate limiting working
- [ ] Uptime monitoring configured
- [ ] Domain + SSL working
- [ ] Documentation published
- [ ] Landing page live
- [ ] Twitter announcement drafted
- [ ] Reddit post drafted

### 🚀 Launch!

1. Announce on Twitter/X (see MARKETING_PLAN.md)
2. Post on Reddit (r/algotrading)
3. Email early access list
4. Monitor logs for first 24 hours

---

**Need help?** Email support@sentinel-algo.com or ping Mitch on Telegram.

**You did it! 🎉 Now go make some money with this API.**
