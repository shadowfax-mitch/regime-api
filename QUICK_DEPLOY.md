# 🚀 Regime API — 10-Minute Deploy Guide

**Goal:** Get regime-api.onrender.com live so we can DM the URL to Pylon

---

## Step 1: Create Render Account (2 min)

1. Go to **https://render.com**
2. Click "Get Started for Free"
3. Sign up with **GitHub** (easiest — auto-connects your repos)
4. Verify email

---

## Step 2: Include Regime Data in Repo (2 min)

Open WSL terminal:
```bash
cd /home/shado/.openclaw/workspace/products/regime-api
mkdir -p data
cp /mnt/c/NinjaTrader/data/regime_data.csv data/
git add data/regime_data.csv
git commit -m "Add regime data for deployment"
git push
```

---

## Step 3: Deploy on Render (5 min)

1. Go to **https://dashboard.render.com**
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub → select **`regime-api`** repo
4. Fill in:

| Field | Value |
|-------|-------|
| Name | `regime-api` |
| Region | Oregon (US West) |
| Branch | `main` |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Instance Type | **Free** (upgrade later if needed) |

5. Click **"Advanced"** → **"Add Environment Variable"**:

| Key | Value |
|-----|-------|
| `REGIME_DATA_PATH` | `data/regime_data.csv` |
| `ADMIN_KEY` | `sentinel2026` |
| `PYTHON_VERSION` | `3.11.0` |

6. Click **"Create Web Service"**
7. Wait 2-3 minutes for build...

---

## Step 4: Test It (1 min)

Once it says "Live" in the Render dashboard:

```bash
# Health check
curl https://regime-api.onrender.com/health

# Get current regime
curl https://regime-api.onrender.com/regime/current
```

If you see JSON with regime data → **IT'S LIVE** 🎉

---

## Step 5: DM Pylon (30 sec)

Send to @pylonx402:
> "Endpoint is live: https://regime-api.onrender.com — 3-state HMM regime classifier (STABLE/TRENDING/HIGH_VOL). Returns JSON with regime, confidence, sub-regime metadata. Ready to wire up."

---

## ⚠️ Notes

- **Free tier sleeps after 15 min of inactivity** (first request after sleep takes ~30 sec to wake). This is fine for testing. Upgrade to $7/mo Starter for always-on when Pylon is connected.
- **Regime data updates:** Run the copy command (Step 2) daily to keep data fresh, then `git push`.
- **Custom domain:** Can add `api.sentinel-algo.com` later in Render settings.

---

## That's It!

Total time: ~10 minutes
Total cost: $0 (free tier)
Result: Live API endpoint ready for Pylon x402 integration

**After deploy, tell Sentinel and I'll update all docs + marketing materials with the live URL.**
