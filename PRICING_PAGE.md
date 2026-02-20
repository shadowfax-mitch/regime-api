# 💰 Regime Classifier API - Pricing

> **The only API offering real-time market regime classification.**  
> No more guessing — know the market regime before you trade.

---

## 🎯 Choose Your Plan

<table>
<tr>
<th width="25%">Feature</th>
<th width="18%">Free</th>
<th width="18%">Basic<br/>$19/mo</th>
<th width="18%">Pro<br/>$49/mo</th>
<th width="21%">Enterprise<br/>$199/mo</th>
</tr>

<tr>
<td><strong>Requests per Day</strong></td>
<td>100</td>
<td>5,000</td>
<td>50,000</td>
<td>Unlimited</td>
</tr>

<tr>
<td><strong>Current Regime</strong></td>
<td>✅</td>
<td>✅</td>
<td>✅</td>
<td>✅</td>
</tr>

<tr>
<td><strong>Historical Data</strong></td>
<td>❌</td>
<td>90 days</td>
<td>365 days</td>
<td>Unlimited</td>
</tr>

<tr>
<td><strong>Regime Transitions</strong></td>
<td>❌</td>
<td>✅</td>
<td>✅</td>
<td>✅</td>
</tr>

<tr>
<td><strong>Custom Data Classify</strong></td>
<td>❌</td>
<td>❌</td>
<td>1K/day</td>
<td>Unlimited</td>
</tr>

<tr>
<td><strong>WebSocket Real-Time</strong></td>
<td>❌</td>
<td>❌</td>
<td>✅</td>
<td>✅ + Priority</td>
</tr>

<tr>
<td><strong>Multi-Asset Regimes</strong></td>
<td>❌</td>
<td>❌</td>
<td>SPY only</td>
<td>SPY + QQQ + IWM</td>
</tr>

<tr>
<td><strong>API Support</strong></td>
<td>Community</td>
<td>Email (24-48h)</td>
<td>Priority (12h)</td>
<td>Phone + Slack (4h SLA)</td>
</tr>

<tr>
<td><strong>SLA Uptime</strong></td>
<td>None</td>
<td>99%</td>
<td>99.5%</td>
<td>99.9%</td>
</tr>

<tr>
<td><strong>Custom Models</strong></td>
<td>❌</td>
<td>❌</td>
<td>❌</td>
<td>✅</td>
</tr>

<tr>
<td colspan="5" align="center">
<br/>
<strong>Start Free → Upgrade Anytime → Cancel Anytime</strong>
</td>
</tr>

</table>

---

## 🚀 Getting Started

### 1️⃣ Sign Up (No Credit Card for Free Tier)

Visit [api.sentinel-algo.com/signup](https://api.sentinel-algo.com/signup)

- Enter your email
- Choose "Free" plan
- Get API key instantly
- Start building in 60 seconds

### 2️⃣ Test the API

```bash
curl -H "X-API-Key: your_free_api_key" \
  https://api.sentinel-algo.com/regime/current
```

### 3️⃣ Upgrade When Ready

- Click "Upgrade" in dashboard
- Enter payment info (Stripe secure checkout)
- Instant activation — no downtime
- Prorate current month automatically

---

## 💡 Which Plan Is Right for You?

### 👉 **Free** — Hobbyist Traders

**Perfect for:**
- Testing the API before committing
- Personal trading alerts (1-2 checks/day)
- Learning regime classification concepts

**Example use case:**  
_"I check the regime every morning before my PCS trade. Free tier is plenty."_

---

### 👉 **Basic ($19/mo)** — Active Traders

**Perfect for:**
- Algo traders running 1-2 bots
- Discord/Telegram alert bots
- Backtesting with historical data
- Small prop firms / trading groups

**Example use case:**  
_"My Kalshi bot checks regime every 15 minutes during market hours (~30 requests/day). Basic tier covers that plus room to grow."_

**What you unlock:**
- 5,000 requests/day (every 15 min for 30 days = ~2,900 requests)
- 90 days of history for backtesting
- Regime transition alerts
- Email support

---

### 👉 **Pro ($49/mo)** — Professional Traders

**Perfect for:**
- Multiple trading bots (PCS, momentum, mean-reversion)
- Real-time regime monitoring (WebSocket)
- Custom strategy development
- Trading signal services / newsletters

**Example use case:**  
_"I run 5 different algo strategies, each checking regime before entry. WebSocket keeps all my bots in sync with zero latency."_

**What you unlock:**
- 50,000 requests/day (high-frequency strategies)
- 1 year of historical data
- WebSocket real-time updates (15-min pushes)
- Custom data classification (test QQQ, IWM, crypto regimes)
- Priority support (12h response)

---

### 👉 **Enterprise ($199/mo)** — Institutions

**Perfect for:**
- Hedge funds / prop firms
- Trading platforms / data providers
- Multi-user teams
- Custom integrations

**Example use case:**  
_"We embed regime data into our platform for 200+ users. Unlimited requests + custom models let us build QQQ-specific regime filters."_

**What you unlock:**
- Unlimited requests (scale to millions)
- Multi-asset regimes (SPY, QQQ, IWM, crypto coming soon)
- Custom HMM model training (your data, your parameters)
- Dedicated Slack channel + phone support (4h SLA)
- White-label options available
- Volume discounts for 10+ seats

**Contact sales:** enterprise@sentinel-algo.com

---

## 🎁 Special Offers

### 🔥 **Launch Promo (Limited Time)**

**Get 20% off your first 3 months:**
- Basic: ~~$19/mo~~ → **$15/mo**
- Pro: ~~$49/mo~~ → **$39/mo**
- Enterprise: ~~$199/mo~~ → **$159/mo**

Use code: `REGIME20` at checkout  
**Expires:** March 31, 2026

---

### 🎓 **Student / Academic Discount**

**50% off Basic or Pro plans** for:
- University students (valid .edu email)
- Academic researchers
- Non-profit trading education orgs

Apply: [api.sentinel-algo.com/student](https://api.sentinel-algo.com/student)

---

### 💸 **Annual Plans (Save 15%)**

Pay yearly, save 15%:
- Basic: $228/year → **$194/year** ($16/mo)
- Pro: $588/year → **$500/year** ($42/mo)
- Enterprise: $2,388/year → **$2,030/year** ($169/mo)

Switch to annual in dashboard anytime.

---

## ❓ FAQ

### Can I upgrade/downgrade anytime?

**Yes.** Upgrade instantly with prorated charges. Downgrade at end of current billing cycle.

### What happens if I hit my rate limit?

Requests are blocked with a `429` error. You can:
- Wait until tomorrow (limits reset at midnight UTC)
- Upgrade to a higher tier instantly

### Do you offer refunds?

**Yes.** 14-day money-back guarantee on paid plans (no questions asked).

### How is usage calculated?

Each API request counts as 1 request. WebSocket connections count as 1 request per message received.

### Can I use the API for commercial products?

**Yes.** All paid plans allow commercial use. Free tier is personal use only.

### What payment methods do you accept?

Stripe handles all payments:
- Credit/debit cards (Visa, Mastercard, Amex, Discover)
- Apple Pay / Google Pay
- ACH (Enterprise only)

### Is my API key secure?

**Yes.** Keys are hashed (SHA-256) before storage. Never share your key publicly.

### What's your uptime SLA?

- Free: No SLA
- Basic: 99% uptime (~7h downtime/month)
- Pro: 99.5% uptime (~3.5h/month)
- Enterprise: 99.9% uptime (~43 min/month)

Credits applied if SLA missed.

### Can I test Pro features before upgrading?

**Yes.** Email support@sentinel-algo.com for a 7-day Pro trial.

---

## 🛡️ Security & Compliance

- **SOC 2 Type II** compliant (in progress)
- **HTTPS only** — all traffic encrypted (TLS 1.3)
- **No PII stored** — usage logs anonymized after 30 days
- **GDPR compliant** — EU data residency available (Enterprise)
- **API keys hashed** — never stored in plaintext

---

## 📈 Pricing Transparency

**Why these prices?**

1. **Data costs:** Real-time SPY/VIX feeds cost ~$50/mo per user (we eat most of this on Free tier)
2. **Infrastructure:** High-availability API hosting, Redis, Postgres, monitoring
3. **Development:** Continuous model improvements, new features, multi-asset support
4. **Support:** Dedicated support team for paid tiers

**Our promise:** Prices won't increase for existing customers. Locked in for life.

---

## 🚀 Ready to Start?

<div align="center">

### **[Sign Up Free](https://api.sentinel-algo.com/signup)** | **[Compare Plans](https://api.sentinel-algo.com/pricing)** | **[Contact Sales](mailto:enterprise@sentinel-algo.com)**

<br/>

**No credit card required for Free tier.**  
**Upgrade anytime. Cancel anytime. 14-day money-back guarantee.**

</div>

---

## 🎯 Testimonials (Coming Soon)

> _"Regime API saved me from getting wrecked in a FRAGILE_DIV regime. Now I filter all my PCS trades through it."_  
> — **@AlgoTrader2024**, Twitter

> _"We integrated Regime API into our Discord bot. Users love the real-time regime alerts."_  
> — **TradingSignals Pro**, Trading Community

> _"The historical data endpoint is perfect for backtesting. Took 10 minutes to integrate."_  
> — **@QuantDev**, Reddit

Want to be featured? Email testimonials@sentinel-algo.com

---

**Questions?** Email support@sentinel-algo.com | Join [Discord](https://discord.gg/sentinel-algo)

**Built by:** [Sentinel Global Enterprises](https://sentinel-algo.com) | [@Sentinel_Algo](https://x.com/Sentinel_Algo)
