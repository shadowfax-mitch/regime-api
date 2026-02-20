# 📊 Regime Classifier API Specification

**Version:** 1.0.0  
**Author:** Sentinel Global Enterprises  
**Status:** MVP Design - Ready for Implementation

---

## 🎯 Overview

The **Regime Classifier API** is the world's first commercial API offering **real-time market regime classification** powered by proven Hidden Markov Models (HMM) and fractal analysis. Unlike generic market data providers, this API delivers **actionable trading context** that algo traders and quant researchers actually need.

### Value Proposition

- **Unique Data**: Only API offering regime classification (not just VIX or price feeds)
- **Proven Models**: Same classification logic powering Sentinel's Cleo/Hank/Bobby trading bots
- **Trader-Focused**: Built for algo traders, not generic data resellers
- **Fast & Simple**: RESTful API, no complex integrations

---

## 🔐 Authentication

All API requests require an API key passed via header:

```
X-API-Key: your_api_key_here
```

**API Key Management:**
- Keys generated via dashboard at `api.sentinel-algo.com/dashboard`
- Each key tied to a subscription tier (Free/Basic/Pro/Enterprise)
- Rate limits enforced per key

---

## 📡 Endpoints

### 1. `GET /regime/current`

**Description:** Get the current SPY market regime classification with metrics.

**Response:**
```json
{
  "regime": "STABLE",
  "timestamp": "2026-02-19T13:00:00Z",
  "spy_price": 602.34,
  "metrics": {
    "accel_z": 0.12,
    "div_z": 0.45,
    "signal_strength": 0.45,
    "vix": 15.2,
    "rv20": 11.3
  },
  "trading_implications": [
    "Put credit spreads (PCS) are optimal in this regime",
    "Sell premium — theta decay is your friend",
    "Consider buying cheap options for asymmetric bets"
  ],
  "regime_duration_days": 5
}
```

**Regime Types:**
- `STABLE` - Low volatility, mean-reverting (ideal for premium selling)
- `FRAGILE_ACCEL` - Acceleration instability (momentum shifts)
- `FRAGILE_DIV` - Divergence instability (beware whipsaws)
- `FRAGILE_BOTH` - High chaos (reduce size, widen strikes)

**Rate Limits:**
- Free: 100/day
- Basic: 5,000/day
- Pro: 50,000/day
- Enterprise: Unlimited

---

### 2. `GET /regime/history?days=N`

**Description:** Get historical regime data for the last N days (max 365).

**Query Parameters:**
- `days` (optional, default: 30, max: 365) - Number of days to retrieve

**Response:**
```json
{
  "data": [
    {
      "date": "2026-02-19",
      "regime": "STABLE",
      "accel_z": 0.12,
      "div_z": 0.45,
      "signal_strength": 0.45
    },
    {
      "date": "2026-02-18",
      "regime": "FRAGILE_DIV",
      "accel_z": 0.34,
      "div_z": 2.1,
      "signal_strength": 2.1
    }
  ],
  "total_days": 30,
  "regime_distribution": {
    "STABLE": 18,
    "FRAGILE_DIV": 8,
    "FRAGILE_ACCEL": 3,
    "FRAGILE_BOTH": 1
  }
}
```

**Tier Availability:**
- Free: ❌ Not available
- Basic: ✅ Up to 90 days
- Pro: ✅ Up to 365 days
- Enterprise: ✅ Unlimited history

---

### 3. `GET /regime/transitions?since=YYYY-MM-DD`

**Description:** Get regime transition events (when regime changed).

**Query Parameters:**
- `since` (required) - Start date (YYYY-MM-DD format)

**Response:**
```json
{
  "transitions": [
    {
      "date": "2026-02-15",
      "from_regime": "STABLE",
      "to_regime": "FRAGILE_DIV",
      "trigger": "VIX spike from 14.5 to 18.2",
      "duration_before_change_days": 7
    },
    {
      "date": "2026-02-08",
      "from_regime": "FRAGILE_ACCEL",
      "to_regime": "STABLE",
      "trigger": "Volatility mean reversion",
      "duration_before_change_days": 3
    }
  ],
  "total_transitions": 2,
  "avg_regime_duration_days": 5.0
}
```

**Tier Availability:**
- Free: ❌ Not available
- Basic: ✅ Last 90 days
- Pro: ✅ Last 365 days
- Enterprise: ✅ Unlimited

---

### 4. `POST /regime/classify`

**Description:** Classify custom OHLCV data (bring your own data).

**Request Body:**
```json
{
  "symbol": "QQQ",
  "data": [
    {
      "timestamp": "2026-02-19T09:30:00Z",
      "open": 510.2,
      "high": 512.5,
      "low": 509.8,
      "close": 511.3,
      "volume": 1234567
    }
  ],
  "vix_value": 16.5
}
```

**Response:**
```json
{
  "regime": "STABLE",
  "confidence": 0.87,
  "metrics": {
    "accel_z": 0.23,
    "div_z": 0.67,
    "signal_strength": 0.67,
    "rv20": 12.4
  },
  "warning": null
}
```

**Requirements:**
- Minimum 60 bars (3 hours of 5-min data or 3 months of daily)
- Must include VIX value for volatility context

**Tier Availability:**
- Free: ❌ Not available
- Basic: ❌ Not available
- Pro: ✅ 1,000 classifications/day
- Enterprise: ✅ Unlimited

---

### 5. `GET /regime/websocket` (WebSocket)

**Description:** Real-time regime updates (pushes new classification every 15 minutes during market hours).

**Connection:**
```javascript
const ws = new WebSocket('wss://api.sentinel-algo.com/regime/websocket?api_key=YOUR_KEY');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('New regime:', data.regime);
};
```

**Message Format:**
```json
{
  "event": "regime_update",
  "regime": "STABLE",
  "timestamp": "2026-02-19T13:00:00Z",
  "metrics": {
    "accel_z": 0.12,
    "div_z": 0.45,
    "signal_strength": 0.45
  }
}
```

**Tier Availability:**
- Free: ❌ Not available
- Basic: ❌ Not available
- Pro: ✅ Real-time updates
- Enterprise: ✅ Real-time + priority delivery

---

## 💰 Pricing Tiers

| Feature | Free | Basic ($19/mo) | Pro ($49/mo) | Enterprise ($199/mo) |
|---------|------|---------------|-------------|---------------------|
| **Requests/day** | 100 | 5,000 | 50,000 | Unlimited |
| **Current regime** | ✅ | ✅ | ✅ | ✅ |
| **Historical data** | ❌ | 90 days | 365 days | Unlimited |
| **Regime transitions** | ❌ | ✅ | ✅ | ✅ |
| **Custom classify** | ❌ | ❌ | 1K/day | Unlimited |
| **WebSocket real-time** | ❌ | ❌ | ✅ | ✅ |
| **Support** | Community | Email | Priority | Phone + Custom |
| **SLA uptime** | None | 99% | 99.5% | 99.9% |

**Payment:** Stripe integration, monthly billing, cancel anytime.

---

## 🔧 Technical Stack

### Backend
- **Framework:** FastAPI (Python 3.10+)
- **Authentication:** API key validation middleware
- **Rate Limiting:** Redis-backed sliding window
- **Database:** PostgreSQL (user accounts, usage tracking)
- **Cache:** Redis (15-min TTL for regime data)
- **Background Jobs:** Celery (regime updates every 15 min)

### Data Pipeline
- **Real-time:** Yahoo Finance API (SPY/VIX data)
- **Historical:** Pre-computed `regime_data.csv` (updated nightly)
- **Classification:** PyramidalHMM from `extend_regime_data.py`

### Deployment
- **Hosting:** Render (free tier for MVP, scales to Pro)
- **Domain:** `api.sentinel-algo.com`
- **SSL:** Automatic via Render
- **Monitoring:** Sentry (error tracking), Grafana (metrics)

---

## 🚀 MVP Scope

**Phase 1 (Launch):**
- ✅ `/regime/current` endpoint
- ✅ `/regime/history` endpoint
- ✅ API key authentication
- ✅ Rate limiting (in-memory, simple)
- ✅ Stripe payment integration
- ✅ Basic dashboard (view API key, usage stats)

**Phase 2 (Post-Launch):**
- `/regime/transitions` endpoint
- `/regime/classify` (custom data)
- WebSocket real-time updates
- Multi-asset support (QQQ, IWM, crypto)

---

## 📊 Success Metrics

**Launch Goals (30 days):**
- 100 free tier sign-ups
- 10 paid subscribers (mix of Basic/Pro)
- $190-500/mo MRR (Monthly Recurring Revenue)
- 99% API uptime

**6-Month Goals:**
- 50 paid subscribers
- $1,000-2,500/mo MRR
- Add 2-3 enterprise customers
- Expand to QQQ/IWM regimes

---

## 🛡️ Security & Compliance

- **API Keys:** SHA-256 hashed, stored in Postgres
- **Rate Limiting:** Per-key sliding window (prevents abuse)
- **HTTPS Only:** All traffic encrypted (TLS 1.3)
- **Data Privacy:** No PII collected, usage logs anonymized after 30 days
- **Terms of Service:** No redistribution of raw data, API use only

---

## 🎯 Target Customers

1. **Algo Traders** - Need regime context for strategy filters (like Kalshi bot)
2. **Quant Researchers** - Backtesting regime-aware strategies
3. **Trading Platforms** - Embed regime data into user dashboards
4. **Discord/Telegram Bots** - Alert users on regime changes
5. **Options Sellers** - Optimize PCS timing based on regimes

---

## 📝 Next Steps

1. ✅ Build FastAPI app (`/products/regime-api/app/`)
2. ✅ Deploy to Render free tier
3. ✅ Create documentation site
4. ✅ Set up Stripe billing
5. ✅ Launch marketing (X, Reddit, Discord)

**Timeline:** 1-2 days for MVP deployment.

---

**Questions?** Contact: mitch@sentinel-algo.com | [@Sentinel_Algo](https://x.com/Sentinel_Algo)
