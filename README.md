# 📊 Regime Classifier API

**The world's first commercial API for real-time market regime classification.**

Built by [Sentinel Global Enterprises](https://sentinel-algo.com) | [@Sentinel_Algo](https://x.com/Sentinel_Algo)

---

## 🎯 What Is This?

A FastAPI-powered REST API that classifies the current stock market regime using proven Hidden Markov Models (HMM) and fractal analysis. 

Unlike generic market data APIs, this tells you **actionable trading context**:
- Is today a **STABLE** regime? (Safe for premium selling / PCS strategies)
- Or a **FRAGILE** regime? (Volatile, high-risk, avoid counter-trend trades)

**Use it to:**
- Filter trading signals (only trade PCS in STABLE regimes)
- Build smarter algo trading bots
- Add regime alerts to Discord/Telegram bots
- Backtest regime-aware strategies

---

## 🚀 Features

✅ **Real-Time Classification** — Updates every 15 minutes during market hours  
✅ **Proven Models** — Same HMM logic powering Sentinel's profitable trading bots (Cleo, Hank, Bobby)  
✅ **Historical Data** — Access up to 365 days of regime history for backtesting  
✅ **Custom Classification** — Bring your own OHLCV data (QQQ, IWM, crypto)  
✅ **WebSocket Real-Time** — Get pushed updates (Pro/Enterprise tiers)  
✅ **Free Tier** — 100 requests/day, no credit card required  

---

## 📚 Documentation

- **[API Spec](./REGIME_API_SPEC.md)** — Full API design document
- **[API Docs](./API_DOCUMENTATION.md)** — Endpoint reference + code examples
- **[Pricing](./PRICING_PAGE.md)** — Plans and pricing
- **[Marketing Plan](./MARKETING_PLAN.md)** — Launch strategy

---

## ⚡ Quick Start

### 1. Sign Up (Free)

Visit [api.sentinel-algo.com/signup](https://api.sentinel-algo.com/signup) to get your API key.

### 2. Test the API

```bash
curl -H "X-API-Key: demo_free_key" \
  https://api.sentinel-algo.com/regime/current
```

**Response:**
```json
{
  "regime": "STABLE",
  "timestamp": "2026-02-19T13:00:00Z",
  "metrics": {
    "accel_z": 0.12,
    "div_z": 0.45,
    "signal_strength": 0.45
  },
  "trading_implications": [
    "Put credit spreads (PCS) are optimal in this regime"
  ]
}
```

### 3. Integrate

**Python:**
```python
import requests

response = requests.get(
    "https://api.sentinel-algo.com/regime/current",
    headers={"X-API-Key": "your_api_key_here"}
)

regime = response.json()
print(f"Current regime: {regime['regime']}")

if regime['regime'] == 'STABLE':
    print("✅ Safe to trade PCS")
else:
    print("⚠️ Fragile regime — be cautious")
```

**JavaScript:**
```javascript
const response = await fetch("https://api.sentinel-algo.com/regime/current", {
  headers: { "X-API-Key": "your_api_key_here" }
});

const regime = await response.json();
console.log(`Current regime: ${regime.regime}`);
```

---

## 🛠️ Local Development

### Prerequisites

- Python 3.10+
- `/mnt/c/NinjaTrader/data/regime_data.csv` (or set `REGIME_DATA_PATH` env var)

### Setup

```bash
# Clone repo
git clone https://github.com/sentinel-algo/regime-api
cd regime-api

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your paths

# Run locally
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs (Swagger UI)

---

## 🚢 Deployment

### Deploy to Render (Recommended)

1. **Connect GitHub Repo**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo

2. **Configure Service**
   - Name: `regime-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**
   - `REGIME_DATA_PATH`: Path to your regime_data.csv
   - `ADMIN_KEY`: Secret key for admin endpoints

4. **Deploy**
   - Click "Create Web Service"
   - Auto-deploys on every git push

**Free Tier Limits:**
- 512 MB RAM
- Sleeps after 15 min inactivity
- 750 hours/month (plenty for MVP)

### Deploy with Docker

```bash
# Build image
docker build -t regime-api .

# Run container
docker run -p 8000:8000 \
  -e REGIME_DATA_PATH=/path/to/regime_data.csv \
  regime-api
```

---

## 📊 Tech Stack

- **Framework:** FastAPI (Python 3.10+)
- **Authentication:** API key validation (SHA-256 hashed)
- **Rate Limiting:** In-memory (Redis for production)
- **Data:** CSV-based (PostgreSQL for production)
- **Hosting:** Render (Railway, Fly.io also supported)
- **Monitoring:** Sentry (error tracking), Grafana (metrics)

---

## 📁 Project Structure

```
regime-api/
├── app/
│   └── main.py              # FastAPI application
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker build config
├── render.yaml               # Render deployment config
├── .env.example              # Environment variables template
├── REGIME_API_SPEC.md        # API design specification
├── API_DOCUMENTATION.md      # Endpoint reference + examples
├── PRICING_PAGE.md           # Pricing tiers + features
├── MARKETING_PLAN.md         # Launch strategy
└── README.md                 # This file
```

---

## 🔐 Security

- **API Keys:** SHA-256 hashed before storage
- **HTTPS Only:** TLS 1.3 encryption
- **Rate Limiting:** Per-key sliding window (prevents abuse)
- **No PII:** Usage logs anonymized after 30 days
- **GDPR Compliant:** EU data residency available (Enterprise tier)

---

## 🎯 Roadmap

### ✅ MVP (Phase 1) — COMPLETE
- [x] Core API endpoints (current, history, transitions)
- [x] API key authentication
- [x] Rate limiting
- [x] Documentation
- [x] Render deployment

### 🚧 Post-Launch (Phase 2) — IN PROGRESS
- [ ] Stripe billing integration
- [ ] User dashboard (view usage, manage keys)
- [ ] WebSocket real-time updates
- [ ] Custom data classification endpoint

### 🔮 Future (Phase 3)
- [ ] Multi-asset regimes (QQQ, IWM, crypto)
- [ ] Python SDK (`pip install regime-api-sdk`)
- [ ] Slack/Discord webhook integrations
- [ ] Custom HMM model training (Enterprise)

---

## 💰 Pricing

| Tier | Price | Requests/Day | History | WebSocket |
|------|-------|-------------|---------|-----------|
| **Free** | $0 | 100 | ❌ | ❌ |
| **Basic** | $19/mo | 5,000 | 90 days | ❌ |
| **Pro** | $49/mo | 50,000 | 365 days | ✅ |
| **Enterprise** | $199/mo | Unlimited | Unlimited | ✅ |

**Launch offer:** Use code `REGIME20` for 20% off first 3 months!

[View Full Pricing](./PRICING_PAGE.md)

---

## 🤝 Contributing

We're not open-sourcing the core classification models (proprietary), but we welcome:

- Bug reports / feature requests (open an issue)
- Documentation improvements (PRs welcome)
- Integration examples (bots, backtesting frameworks)

---

## 📧 Support

- **Docs:** [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- **Email:** support@sentinel-algo.com
- **Discord:** [discord.gg/sentinel-algo](https://discord.gg/sentinel-algo)
- **Twitter:** [@Sentinel_Algo](https://x.com/Sentinel_Algo)

**Response times:**
- Free: Community (Discord)
- Basic: Email (24-48h)
- Pro: Priority (12h)
- Enterprise: Phone + Slack (4h SLA)

---

## 📜 License

Proprietary — Copyright © 2026 Sentinel Global Enterprises

**Commercial use allowed** with paid subscription. Free tier for personal use only.

---

## 🎉 Built By

**Sentinel Global Enterprises** — AI-powered algorithmic trading systems.

Our bots (Cleo, Hank, Bobby) use the same regime classification models powering this API.

**Follow our journey:**
- Twitter: [@Sentinel_Algo](https://x.com/Sentinel_Algo)
- Website: [sentinel-algo.com](https://sentinel-algo.com)
- Blog: [blog.sentinel-algo.com](https://blog.sentinel-algo.com)

---

**Ready to build smarter trading systems? [Get your API key →](https://api.sentinel-algo.com/signup)**
