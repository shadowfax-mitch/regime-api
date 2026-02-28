# 🚀 Regime Classifier API — Render Deployment (5-10 Minutes)

**Status:** Code ready ✅ | API tested locally ✅ | Ready to deploy 🎯

---

## What's Ready

- ✅ **API Code:** FastAPI app with full regime classification, history, transitions, and custom classification endpoints
- ✅ **x402 Integration:** Micropayment module ready (needs wallet address to activate)
- ✅ **Docker Ready:** Dockerfile configured for Render
- ✅ **Render Config:** render.yaml with all settings pre-configured
- ✅ **Data:** regime_data.csv committed to repo

---

## Local Testing Results (Verified Feb 27, 7:36 AM CT)

### Health Endpoint
```bash
curl http://localhost:8000/health
```
**Response:** ✅ `{"status":"healthy","timestamp":"2026-02-27T07:36:19.687542"}`

### Regime Endpoint (with demo key)
```bash
curl -H "X-API-Key: demo_free_key" http://localhost:8000/regime/current
```
**Response:** ✅
```json
{
  "regime": "STABLE",
  "timestamp": "2026-02-27T07:36:19.687542",
  "metrics": {
    "accel_z": 0.0,
    "div_z": 0.0,
    "signal_strength": 0.0,
    "vix": null,
    "rv20": null
  },
  "trading_implications": [
    "Put credit spreads (PCS) are optimal in this regime",
    "Sell premium — theta decay is your friend",
    "Consider buying cheap options for asymmetric bets"
  ],
  "regime_duration_days": 8
}
```

### x402 Info Endpoint
```bash
curl http://localhost:8000/x402/info
```
**Response:** ✅ x402 integration ready (currently disabled — waiting for wallet address)

### Available Endpoints
- `/` — Root (welcome)
- `/health` — Health check
- `/regime/current` — Current regime (requires API key)
- `/regime/history` — Historical regimes (requires API key)
- `/regime/transitions` — Regime transitions (requires API key)
- `/regime/classify` — Custom classification (requires API key)
- `/x402/info` — x402 micropayment info (public)
- `/admin/stats` — Admin stats (requires admin key)

---

## Deploy to Render (Step-by-Step)

### Step 1: Create Render Account (2 minutes)

1. Go to **https://render.com**
2. Click **"Get Started for Free"**
3. Click **"Sign up with GitHub"** (easiest)
4. Authorize Render to access your GitHub account
5. Verify your email

---

### Step 2: Deploy Service (5 minutes)

1. Log in to **https://dashboard.render.com**
2. Click **"New +"** in top right
3. Select **"Web Service"**
4. Connect GitHub:
   - If not already connected: Click "Connect account"
   - Select `shadowfax-mitch/regime-api` from the repo list
   - Click "Connect"

5. Fill in the deployment form:

| Field | Value |
|-------|-------|
| **Name** | `regime-api` |
| **Region** | `Oregon (US West)` |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

6. Click **"Advanced"** to expand advanced options
7. Add environment variables:

| Key | Value |
|-----|-------|
| `REGIME_DATA_PATH` | `/opt/render/project/data/regime_data.csv` |
| `ADMIN_KEY` | `sentinel2026` |
| `PYTHON_VERSION` | `3.11.0` |

8. Leave **x402-related vars blank for now** (we'll add after wallet setup):
   - `X402_PAY_TO_ADDRESS` — *add later when wallet is ready*
   - `X402_CHAIN` — *optional, defaults to Base (eip155:8453)*

9. Click **"Create Web Service"**

10. **Wait 2-3 minutes** for build and deployment
    - Watch the logs in the Render dashboard
    - You'll see: "Build started" → "Building…" → "Build succeeded" → "Deploy started" → "Live"

---

### Step 3: Verify Deployment (1 minute)

Once Render shows "Live" in the dashboard:

```bash
# Test health endpoint
curl https://regime-api.onrender.com/health

# Test regime endpoint
curl -H "X-API-Key: demo_free_key" https://regime-api.onrender.com/regime/current

# Test x402 info
curl https://regime-api.onrender.com/x402/info
```

**Expected responses:** Same JSON as local testing above ✅

---

## After Deployment: Enable x402 Micropayments (Optional but Recommended)

If you want to enable x402 micropayments (AI agents paying per query):

### Step 1: Set Up Base Wallet (~5 min)

1. Create a **Base network wallet** (if you don't have one):
   - **Option A (Recommended):** Use Coinbase Wallet
     - Download from https://www.coinbase.com/wallet
     - Create wallet with test USDC on Base
   - **Option B:** Use MetaMask
     - Download from https://metamask.io
     - Add Base network
     - Add test USDC

2. **Get your wallet address** (copy to clipboard)
   - Example: `0x1234567890abcdef...`

3. **Fund with test USDC** (on Base tesnet for testing):
   - Use faucet: https://base.org/faucet
   - Request test USDC

### Step 2: Enable x402 in Render

1. Go to **https://dashboard.render.com** → **regime-api** service
2. Click **"Environment"**
3. Add new variable:
   - **Key:** `X402_PAY_TO_ADDRESS`
   - **Value:** `0x1234567890abcdef...` (your wallet address)
4. Save and Render will auto-redeploy (~30 sec)
5. Verify with:
   ```bash
   curl https://regime-api.onrender.com/x402/info
   ```
   Should show `"x402_enabled": true`

---

## API Rate Limits & Tiers

### Demo API Keys (for testing)
```
demo_free_key   → Free tier (100 req/day)
demo_basic_key  → Basic tier (5,000 req/day)
demo_pro_key    → Pro tier (50,000 req/day)
```

### Free Tier Features
- `/regime/current` ✅
- No history, transitions, or custom classification
- 100 requests/day

### Pro Tier Features (for x402 payments)
- All endpoints ✅
- Custom regime classification ✅
- Historical data (365 days) ✅
- Unlimited requests (pay per query)

---

## Important Notes

1. **Free Tier Sleeps:** Render's free tier sleeps after 15 min of inactivity. First request after sleep takes ~30 sec. Upgrade to Starter ($7/mo) for always-on if Pylon/x402 needs it.

2. **Regime Data Updates:** To keep regime data fresh:
   ```bash
   cd /path/to/regime-api
   cp /mnt/c/NinjaTrader/data/regime_data.csv data/
   git add data/regime_data.csv
   git commit -m "Update regime data"
   git push
   ```
   Render will auto-redeploy.

3. **Custom Domain:** After deployment, you can add a custom domain (`api.sentinel-algo.com`) in Render settings.

4. **Monitoring:** Monitor logs in Render dashboard under **"Logs"** tab.

---

## Troubleshooting

### Build fails
- Check build log in Render dashboard
- Verify all Python dependencies are in `requirements.txt`
- Ensure `Dockerfile` exists

### Endpoint returns 404
- Verify service is "Live" (not "Building" or "Failed")
- Check endpoint URL spelling
- Ensure you're using the correct Render URL (`https://regime-api.onrender.com`)

### Can't connect GitHub
- Authorize Render in GitHub settings → Applications → Render
- Verify you're the repo owner or have push access

### x402 not enabling
- Verify `X402_PAY_TO_ADDRESS` is set correctly
- Wallet address must start with `0x` and be 42 characters
- Restart the service in Render after setting the env var

---

## Next Steps (After Live)

1. ✅ **Copy the live URL:** `https://regime-api.onrender.com`
2. ✅ **Run test queries** (see "Verify Deployment" above)
3. 📧 **Notify the x402 partner** (@pylonx402 or Pylon):
   > "Regime Classifier API is live at https://regime-api.onrender.com
   > 
   > - Current regime: STABLE/TRENDING/HIGH_VOL (3-state HMM)
   > - Endpoints: /regime/current, /regime/history, /regime/transitions, /regime/classify
   > - x402 ready: Pay per query in USDC on Base
   > - API keys: Free/Basic/Pro tiers available
   > 
   > Ready to integrate!"

4. 🔄 **Set up auto-updates:** Configure cron to push fresh regime data daily
5. 📊 **Monitor usage** in Render dashboard

---

## Support

- **Render docs:** https://render.com/docs
- **FastAPI docs:** https://fastapi.tiangolo.com
- **x402 protocol:** https://x402.sh

---

**Total time: ~10 minutes**  
**Total cost: $0 (free tier, upgrade to $7/mo later if needed)**  
**Result: Live API + x402 micropayment support 🎉**
