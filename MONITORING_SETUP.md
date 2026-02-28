# 📊 Regime API — Monitoring Setup Guide

**Goal:** Set up alerts so you know immediately when the API goes down or has issues.

---

## Why Monitor?

Your Regime API is a **revenue-generating service**. If it goes down:
- ❌ Customers can't use it
- ❌ x402 micropayments stop flowing
- ❌ Your reputation takes a hit

**With monitoring, you get alerted within 1 minute of any outage.**

---

## Monitoring Layers

We'll set up 3 layers:

1. **Render Built-In Monitoring** (Free, 5 min setup)
2. **UptimeRobot** (Free, external monitoring, 10 min setup)
3. **Simple Python Watchdog** (Free, Telegram alerts, 15 min setup)

---

## Layer 1: Render Built-In Monitoring (5 minutes)

Render automatically monitors your service. Here's how to use it:

### Step 1: Enable Email Alerts

- [ ] Go to https://dashboard.render.com → regime-api
- [ ] Click **"Settings"** tab
- [ ] Scroll to **"Notifications"**
- [ ] Enable **"Deploy Failed"** email notifications
- [ ] Enable **"Service Unhealthy"** email notifications
- [ ] Save

**What this does:** Emails you when deployment fails or health check fails.

### Step 2: Check Built-In Logs

- [ ] Click **"Logs"** tab in Render dashboard
- [ ] Bookmark this page: https://dashboard.render.com/web/regime-api/logs

**Use logs to:**
- See requests in real-time
- Debug errors
- Check startup issues

### Step 3: Enable Health Checks (Already Done!)

Your API already has `/health` endpoint. Render checks it automatically.

**How it works:**
- Render pings `/health` every 30 seconds
- If it gets a non-200 response, it marks service as unhealthy
- After 3 failures, you get an email

✅ **Layer 1 complete!** You now get alerts for deployment and health failures.

---

## Layer 2: UptimeRobot (10 minutes)

**Why?** External monitoring from outside Render. Catches issues that Render's internal checks might miss (DNS, SSL, network).

### Step 1: Create UptimeRobot Account

- [ ] Go to https://uptimerobot.com
- [ ] Click **"Register for FREE"**
- [ ] Sign up with email (free tier = 50 monitors!)
- [ ] Verify email

### Step 2: Add Monitor

- [ ] Login to UptimeRobot dashboard
- [ ] Click **"+ Add New Monitor"**

Fill in:

| Field | Value |
|-------|-------|
| **Monitor Type** | HTTP(s) |
| **Friendly Name** | Regime API - Health |
| **URL** | `https://regime-api.onrender.com/health` |
| **Monitoring Interval** | 5 minutes (free tier) |

- [ ] Click **"Create Monitor"**

### Step 3: Add Second Monitor (Current Regime Endpoint)

- [ ] Click **"+ Add New Monitor"** again

Fill in:

| Field | Value |
|-------|-------|
| **Monitor Type** | HTTP(s) |
| **Friendly Name** | Regime API - Current Regime |
| **URL** | `https://regime-api.onrender.com/regime/current` |
| **Monitoring Interval** | 5 minutes |
| **Custom HTTP Headers** | `X-API-Key: demo_free_key` |
| **Keyword Exists** | `regime` |

- [ ] Click **"Create Monitor"**

**What this does:** Checks that the actual regime endpoint works (not just health check).

### Step 4: Set Up Alerts

- [ ] Click **"My Settings"** → **"Alert Contacts"**
- [ ] Your email is already added (verified)
- [ ] Optional: Add Telegram alerts:
  - Click **"Add Alert Contact"**
  - Select **"Telegram"**
  - Follow instructions to add UptimeRobot bot to your Telegram
  - Set alert threshold: **"Notify when down"**

- [ ] Save

✅ **Layer 2 complete!** You now get external monitoring + alerts every 5 minutes.

---

## Layer 3: Python Watchdog Script (15 minutes)

**Why?** Custom monitoring that checks YOUR specific metrics and sends Telegram alerts.

### Step 1: Create Watchdog Script

Create this file: `~/regime-api-watchdog.py`

```python
#!/usr/bin/env python3
"""
Regime API Watchdog
===================
Monitors the Regime API and sends Telegram alerts on failures.
Run as cron job: */5 * * * * python3 ~/regime-api-watchdog.py
"""

import requests
import time
from datetime import datetime

# ───────────────────────────────────────────────────────────────────
# CONFIG
# ───────────────────────────────────────────────────────────────────

API_URL = "https://regime-api.onrender.com"
DEMO_KEY = "demo_free_key"
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Get from @BotFather
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"      # Your Telegram chat ID

# ───────────────────────────────────────────────────────────────────
# TELEGRAM ALERT FUNCTION
# ───────────────────────────────────────────────────────────────────

def send_telegram_alert(message):
    """Send alert to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": f"🚨 Regime API Alert\n\n{message}",
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Failed to send Telegram alert: {e}")

# ───────────────────────────────────────────────────────────────────
# HEALTH CHECKS
# ───────────────────────────────────────────────────────────────────

def check_health():
    """Check /health endpoint."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        if response.status_code == 200:
            return True, "OK"
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "Timeout (>10s)"
    except requests.exceptions.ConnectionError:
        return False, "Connection failed"
    except Exception as e:
        return False, str(e)

def check_regime_endpoint():
    """Check /regime/current endpoint."""
    try:
        headers = {"X-API-Key": DEMO_KEY}
        response = requests.get(f"{API_URL}/regime/current", headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "regime" in data:
                return True, f"OK (regime: {data['regime']})"
            else:
                return False, "Missing 'regime' key in response"
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)

# ───────────────────────────────────────────────────────────────────
# MAIN
# ───────────────────────────────────────────────────────────────────

def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Running Regime API watchdog...")
    
    # Check health endpoint
    health_ok, health_msg = check_health()
    if not health_ok:
        alert = f"⚠️ Health check FAILED: {health_msg}"
        print(alert)
        send_telegram_alert(alert)
        return
    
    # Check regime endpoint
    regime_ok, regime_msg = check_regime_endpoint()
    if not regime_ok:
        alert = f"⚠️ Regime endpoint FAILED: {regime_msg}"
        print(alert)
        send_telegram_alert(alert)
        return
    
    print(f"✅ All checks passed")

if __name__ == "__main__":
    main()
```

- [ ] Save this file to `~/regime-api-watchdog.py`

### Step 2: Get Telegram Bot Token (5 min)

- [ ] Open Telegram
- [ ] Search for **@BotFather**
- [ ] Send `/newbot`
- [ ] Follow prompts (name: "Regime API Watchdog")
- [ ] Copy the bot token (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
- [ ] Paste it into the script: `TELEGRAM_BOT_TOKEN = "..."`

### Step 3: Get Your Chat ID (2 min)

- [ ] Search for **@userinfobot** in Telegram
- [ ] Send `/start`
- [ ] Copy your ID (a number like `123456789`)
- [ ] Paste it into the script: `TELEGRAM_CHAT_ID = "..."`

### Step 4: Test the Script (1 min)

```bash
chmod +x ~/regime-api-watchdog.py
python3 ~/regime-api-watchdog.py
```

You should get:
- Console output: `✅ All checks passed`
- **If it fails**, you'll get a Telegram message!

- [ ] Script runs successfully

### Step 5: Set Up Cron Job (2 min)

Run this to edit your crontab:

```bash
crontab -e
```

Add this line (runs every 5 minutes):

```bash
*/5 * * * * python3 ~/regime-api-watchdog.py >> ~/regime-api-watchdog.log 2>&1
```

Save and exit.

- [ ] Cron job added

✅ **Layer 3 complete!** You now have custom monitoring with Telegram alerts every 5 minutes.

---

## What You Have Now

✅ **Render Built-In** — Email alerts for deployment failures  
✅ **UptimeRobot** — External monitoring + email/Telegram alerts every 5 min  
✅ **Python Watchdog** — Custom checks + Telegram alerts every 5 min  

**Total alert time:** ~1 minute after any failure (UptimeRobot or Watchdog will catch it)

---

## Testing Your Monitoring

Want to make sure it works? Break the API on purpose:

1. **Simulate downtime:**
   - Go to Render dashboard → regime-api
   - Click **"Manual Deploy"** → **"Clear build cache & deploy"**
   - During the ~2 min rebuild, your monitors should alert you

2. **Check your alerts:**
   - UptimeRobot should email you: "Monitor is DOWN"
   - Watchdog should Telegram you: "🚨 Health check FAILED"

3. **After it's back up:**
   - UptimeRobot emails: "Monitor is UP"
   - Watchdog stops alerting

---

## Monitoring Dashboard URLs

Bookmark these:

| Service | URL |
|---------|-----|
| **Render Logs** | https://dashboard.render.com/web/regime-api/logs |
| **UptimeRobot** | https://uptimerobot.com/dashboard |
| **Watchdog Logs** | `~/regime-api-watchdog.log` on your machine |

---

## Quick Troubleshooting

### UptimeRobot shows DOWN but API works
- Free tier has 5-min intervals — might just be catching a Render sleep/wake
- Wait 10 minutes to see if it resolves
- If persistent, check Render logs

### Watchdog not running
- Check cron: `crontab -l` (should show the job)
- Check logs: `cat ~/regime-api-watchdog.log`
- Test manually: `python3 ~/regime-api-watchdog.py`

### Telegram alerts not coming
- Verify bot token and chat ID are correct
- Send a test message to your bot in Telegram
- Check the bot is not blocked

---

## Maintenance

**Weekly:**
- [ ] Check UptimeRobot dashboard for uptime %
  - Target: >99% uptime
  - Render free tier might dip to ~95% (sleep/wake)

**Monthly:**
- [ ] Review Render logs for errors
- [ ] Check watchdog logs: `tail -100 ~/regime-api-watchdog.log`

---

## Next Steps

✅ **Monitoring is live!** Now you can:

1. **Relax** — You'll know immediately if anything breaks
2. **Enable x402** — Follow x402_INTEGRATION_GUIDE.md
3. **Start marketing** — API is production-ready

---

**Total setup time:** ~30 minutes  
**Total cost:** $0  
**Peace of mind:** Priceless 😊
