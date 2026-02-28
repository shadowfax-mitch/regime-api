# 🚀 Regime API — Deployment Checklist for Mitch

**Goal:** Deploy regime-api to Render in 10 minutes. Just follow the checkboxes.

---

## Pre-Flight ✅

Before you start:

- [ ] You have a GitHub account (shadowfax-mitch)
- [ ] The regime-api repo is pushed to GitHub
- [ ] You're on your Windows machine with WSL/Ubuntu

**Total time estimate:** 10-12 minutes  
**Total cost:** $0 (free tier)

---

## Step 1: Create Render Account (2 minutes)

- [ ] Go to https://render.com
- [ ] Click **"Get Started for Free"**
- [ ] Click **"Sign up with GitHub"** (easiest — auto-connects repos)
- [ ] Authorize Render to access your GitHub account
- [ ] Check your email and verify your account

**You should now see the Render dashboard.**

---

## Step 2: Create Web Service (5 minutes)

- [ ] In Render dashboard, click **"New +"** (top right)
- [ ] Select **"Web Service"**
- [ ] Click **"Connect a repository"** → find `regime-api` in the list
- [ ] Click **"Connect"** next to regime-api

### Configuration Form

Fill in EXACTLY as shown:

| Field | Value |
|-------|-------|
| **Name** | `regime-api` |
| **Region** | `Oregon (US West)` |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

- [ ] All fields filled correctly

### Environment Variables

- [ ] Click **"Advanced"** to expand advanced options
- [ ] Click **"Add Environment Variable"** (do this 3 times)

Add these 3 variables:

| Key | Value |
|-----|-------|
| `REGIME_DATA_PATH` | `/opt/render/project/data/regime_data.csv` |
| `ADMIN_KEY` | `sentinel2026` |
| `PYTHON_VERSION` | `3.11.0` |

- [ ] All 3 environment variables added

### Deploy!

- [ ] Click **"Create Web Service"** (bottom of page)
- [ ] Wait 2-3 minutes while Render builds and deploys
  - You'll see: "Build started" → "Building..." → "Deploy live"
- [ ] When it says **"Live"** in green — you're done! 🎉

---

## Step 3: Test the Deployment (2 minutes)

- [ ] Copy your Render URL from the dashboard (top of the page)
  - It should be: `https://regime-api.onrender.com`

### Run Test Commands

Open WSL terminal and run these:

```bash
# Test 1: Health check (should return JSON with "status": "healthy")
curl https://regime-api.onrender.com/health

# Test 2: Current regime (should return regime data)
curl -H "X-API-Key: demo_free_key" https://regime-api.onrender.com/regime/current

# Test 3: x402 info (should show x402 is ready)
curl https://regime-api.onrender.com/x402/info
```

- [ ] Health check works (returns JSON)
- [ ] Regime endpoint works (returns regime: STABLE/TRENDING/HIGH_VOL)
- [ ] x402 info shows config

**If all 3 tests pass → API is LIVE and working!**

---

## Step 4: Save Your Info (1 minute)

- [ ] Copy your Render URL: `https://regime-api.onrender.com`
- [ ] Save it in a note (you'll need it for marketing/integration)
- [ ] Bookmark the Render dashboard: https://dashboard.render.com

**Your admin key is:** `sentinel2026` (save this too)

---

## Troubleshooting

### Build Failed
- Check the **"Logs"** tab in Render dashboard
- Most common issue: Missing Python dependencies
- Fix: Make sure `requirements.txt` is committed to GitHub
- Then click **"Manual Deploy"** → **"Deploy latest commit"**

### Endpoint Returns 404
- Wait 30 seconds after "Live" appears (sometimes takes a moment)
- Verify the URL is correct (should be `https://regime-api.onrender.com`)
- Check **"Logs"** tab for startup errors

### Can't Find Repo
- Go to Render → Settings → Connected Accounts
- Make sure GitHub is connected
- Try disconnecting and reconnecting GitHub

### Free Tier Sleeps After 15 Minutes
- **This is normal!** Free tier sleeps after inactivity
- First request after sleep takes ~30 seconds to wake up
- If you need always-on, upgrade to Starter ($7/mo) later

---

## What's Next?

✅ **API is live!** Now you can:

1. **Test it more** — Run the TEST_SCRIPT.sh (see next file)
2. **Set up monitoring** — Follow MONITORING_SETUP.md
3. **Enable x402 payments** — Follow x402_INTEGRATION_GUIDE.md (optional)
4. **Start marketing** — Tweet the URL, add to website, etc.

---

## Quick Reference

| What | Where |
|------|-------|
| **Live URL** | https://regime-api.onrender.com |
| **Dashboard** | https://dashboard.render.com |
| **Logs** | Dashboard → regime-api → Logs tab |
| **Settings** | Dashboard → regime-api → Settings |
| **Admin Key** | `sentinel2026` |

---

**Total time:** ~10 minutes  
**Total cost:** $0  
**Status:** ✅ LIVE

**You did it! The API is deployed. 🎉**

Next: Run `bash TEST_SCRIPT.sh` to validate everything works.
