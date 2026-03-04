# RENDER DEPLOYMENT — 10-Minute Execution (Tonight, Mar 3)

**Status:** Regime data updated and pushed to GitHub (just now, 4:26 PM CT)  
**Next:** Deploy to Render (you do this, 10 min)  
**Then:** API goes live at `regime-api.onrender.com`  

---

## WHAT YOU NEED

- Render account (free)
- Your GitHub login
- 10 minutes

---

## THE CHECKLIST

### ✅ Step 1: Render Account (If not already created) — 2 min

1. Go to: https://render.com
2. Click "Get Started for Free"
3. Click "Sign up with GitHub"
4. Authorize Render to access your GitHub repos
5. Verify email

**Status:** ✅ You only do this once ever

---

### ✅ Step 2: Create Web Service — 5 min

1. Go to: https://dashboard.render.com
2. Click **"New +"** in top left
3. Select **"Web Service"**
4. Look for `regime-api` in the list (or search for it)
5. Click on it → Click **"Connect"**

**You'll see a form. Fill it in exactly like this:**

| Field | What to Enter | Notes |
|-------|---------------|-------|
| **Name** | `regime-api` | Must be exactly this (Render uses for subdomain) |
| **Environment** | `Python 3` | Dropdown |
| **Region** | `Oregon (US West)` or `US East` | Doesn't matter much; pick closest to you |
| **Branch** | `main` | Default; leave as-is |
| **Build Command** | `pip install -r requirements.txt` | Copy exactly |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` | Copy exactly |
| **Instance Type** | `Free` | Bottom of form |

**Then click "Advanced" and add Environment Variables:**

| Key | Value | 
|-----|-------|
| `REGIME_DATA_PATH` | `data/regime_data.csv` |
| `ADMIN_KEY` | `sentinel2026` |
| `PYTHON_VERSION` | `3.11.0` |

(For each one: Type the key, press Tab, type the value, click "Add Environment Variable")

**Then click "Create Web Service"**

**Wait 2-3 minutes.** Render will build and deploy. You'll see:
- "Building..." (1-2 min)
- "Running..." (then you're live!)

---

### ✅ Step 3: Verify It's Live — 1 min

Once Render says **"Live"** (green status), test it:

**Open Terminal and run:**
```bash
curl https://regime-api.onrender.com/health
```

**You should see:**
```json
{"status": "ok", "timestamp": "2026-03-03T20:26:00Z"}
```

If you see JSON → **IT'S LIVE** 🎉

---

### ✅ Step 4: Copy Your URL

From the Render dashboard, you'll see your URL at the top:
```
https://regime-api.onrender.com
```

Copy this. You'll use it to:
- DM to @pylonx402 (Pylon x402 integration)
- Share in marketing posts
- Use in your trading bots

---

## THAT'S IT

**Total time:** 10 minutes  
**Total cost:** $0 (free tier, forever fine for this use)  
**Result:** Live API endpoint, production-ready  

---

## NEXT STEPS (I'll Handle)

Once you tell me the deployment is live, I'll:
1. ✅ Update all marketing materials with the live URL
2. ✅ Prepare the Pylon x402 partnership DM (ready to send)
3. ✅ Post marketing posts to X (@Sentinel_Algo)
4. ✅ Update website with API launch announcement

---

## IF SOMETHING GOES WRONG

**Build fails?**
- Check that you're deploying the `regime-api` repo (not a different one)
- Check that all the command fields are typed exactly as shown

**Can't find the regime-api repo?**
- Make sure you're in the right GitHub organization
- The repo name is `regime-api` (shadowfax-mitch/regime-api)

**API returns errors after deploy?**
- First request after deployment sometimes takes 30 sec (Render free tier)
- Wait 5 min and try again

**Still broken?**
- Check logs in Render dashboard (click "Logs" tab)
- DM me and I'll debug

---

## EXPECTED OUTCOMES

✅ **Immediate (tonight):**
- Regime API live and accessible
- Can share URL in marketing

✅ **This week:**
- Pylon x402 partnership launch (DM ready)
- Marketing posts + Website announcement
- First API usage (x402 integration + other integrations)

✅ **This month:**
- $100-500/mo from API usage + subscriptions
- Establishes Sentinel as infrastructure provider (not just content)

---

**Status: READY FOR YOU TO DEPLOY**

Everything is staged. Just follow the 4 steps above.

Message me when it's live and I'll handle the rest. 🚀
