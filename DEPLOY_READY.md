# ✅ DEPLOY READY - Regime API

**Status:** Git repo initialized, ready for GitHub + Render deployment  
**Prepared:** 2026-02-20 5:10 AM CT  
**Next Step:** Push to GitHub, then deploy to Render

---

## What's Ready

✅ Git repository initialized (`.git/`)  
✅ `.gitignore` configured (excludes venv, .env, data files)  
✅ Initial commit made (16 files, 4,485 lines)  
✅ Branch renamed to `main`  
✅ All documentation complete  
✅ Render deployment config ready (`render.yaml`)  
✅ Test suite included (`test_api.py`)  

---

## GitHub Setup (5 minutes)

### Option A: Via GitHub CLI (fastest)

```bash
cd /home/shado/.openclaw/workspace/products/regime-api

# Create GitHub repo
gh repo create sentinel-algo/regime-api --public --description "Real-time market regime classification API for AI trading agents" --source=. --remote=origin --push

# Done! Repo created and pushed
```

### Option B: Via GitHub Web (manual)

1. Go to https://github.com/new
2. Repository name: `regime-api`
3. Description: "Real-time market regime classification API for AI trading agents"
4. Public repository
5. Do NOT initialize with README (we have one)
6. Click "Create repository"

7. Push local repo:
```bash
cd /home/shado/.openclaw/workspace/products/regime-api

git remote add origin https://github.com/shadowfax-mitch/regime-api.git
# OR for org: https://github.com/sentinel-algo/regime-api.git

git push -u origin main
```

---

## Render Deployment (10 minutes)

### Prerequisites
- GitHub repo created and pushed (above)
- Render account: https://render.com (free tier OK for MVP)
- regime_data.csv file (already generated at `/mnt/c/NinjaTrader/data/regime_data.csv`)

### Steps

1. **Go to Render Dashboard:** https://dashboard.render.com

2. **New Web Service:**
   - Click "New +" → "Web Service"
   - Connect GitHub account (if not already)
   - Select repository: `regime-api`

3. **Configure:**
   - Name: `regime-api`
   - Region: Oregon (US West) or closest
   - Branch: `main`
   - Root Directory: (leave blank)
   - Environment: `Python 3`
   - Python Version: `3.11.0`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Instance Type:**
   - Free (512 MB RAM, sleeps after 15 min inactivity) — OK for MVP
   - Upgrade to Starter ($7/mo) for always-on when needed

5. **Environment Variables:**
   Click "Environment" tab, add:
   
   | Key | Value |
   |-----|-------|
   | `REGIME_DATA_PATH` | `/opt/render/project/src/data/regime_data.csv` |
   | `ADMIN_KEY` | `[generate random 32-char string]` |
   | `PYTHON_VERSION` | `3.11.0` |

6. **Upload Regime Data:**
   
   **Option A: Include in git (if <100 MB)**
   ```bash
   cd /home/shado/.openclaw/workspace/products/regime-api
   mkdir -p data
   cp /mnt/c/NinjaTrader/data/regime_data.csv data/
   git add data/regime_data.csv
   git commit -m "Add regime data CSV"
   git push
   ```
   
   **Option B: Use Render Disk (persistent storage)**
   - In Render dashboard → "Disks" → "Add Disk"
   - Name: `regime-data`, Size: 1 GB, Mount: `/data`
   - SSH into Render: `render shell regime-api`
   - Upload: `scp /mnt/c/NinjaTrader/data/regime_data.csv user@render:/data/`
   - Update env var: `REGIME_DATA_PATH=/data/regime_data.csv`

7. **Deploy:**
   - Click "Create Web Service"
   - Wait 2-3 minutes for build + deploy
   - Check logs for "Uvicorn running"

8. **Test:**
   ```bash
   # Health check
   curl https://regime-api.onrender.com/health
   
   # Demo query
   curl -H "X-API-Key: demo_free_key" \
     https://regime-api.onrender.com/regime/current
   ```

9. **Custom Domain (optional):**
   - Render → "Settings" → "Custom Domain"
   - Add: `api.sentinel-algo.com`
   - Update DNS CNAME record as instructed

---

## Post-Deployment

### Update Documentation

Once deployed, update these files with live URL:

- `README.md` — Replace localhost examples with `https://regime-api.onrender.com`
- `API_DOCUMENTATION.md` — Update all curl examples
- `MARKETING_PLAN.md` — Add live URL to launch posts

### Marketing Launch

Follow `MARKETING_PLAN.md`:
- Announce on X/Twitter (thread ready in MARKETING_PLAN.md)
- Post on Reddit (r/algotrading, r/quantfinance, r/Python)
- Submit to API directories (RapidAPI, ProgrammableWeb)
- Email Kit subscribers (if list exists)

### Monitoring

- Check Render logs daily: https://dashboard.render.com/web/regime-api/logs
- Monitor usage in Render metrics dashboard
- Track API key requests (add analytics later)

---

## Estimated Timeline

| Task | Time | Status |
|------|------|--------|
| GitHub setup | 5 min | ⏳ Ready |
| Render configuration | 10 min | ⏳ Ready |
| Regime data upload | 5 min | ⏳ Ready |
| First deploy + test | 5 min | ⏳ Pending |
| Documentation updates | 10 min | ⏳ Pending |
| Marketing launch | 30 min | ⏳ Pending |
| **Total** | **65 min** | |

---

## Revenue Activation

Once live, set up Stripe billing (see `PRICING_PAGE.md`):

1. Create Stripe account
2. Generate API keys
3. Add `/billing/subscribe` endpoint
4. Implement API key → tier mapping
5. Add usage tracking

**Conservative Month 1 revenue:** $50-100  
**Target Month 3 revenue:** $300-500

---

## Support & Maintenance

**Daily:**
- Check Render logs for errors
- Monitor regime data freshness (update daily)

**Weekly:**
- Review usage analytics
- Respond to support emails

**Monthly:**
- Update regime data with latest months
- Review pricing tier performance
- A/B test pricing ($19 vs $29 for Basic tier)

---

**Status:** 🚀 FULLY PREPARED — Ready for Mitch to deploy when convenient

**Recommendation:** Deploy during low-traffic hours (evening/weekend) to test thoroughly before marketing launch.
