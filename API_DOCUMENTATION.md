# 📚 Regime Classifier API Documentation

**Base URL:** `https://api.sentinel-algo.com`  
**Version:** 1.0.0  
**Last Updated:** February 19, 2026

---

## 🚀 Quick Start

### 1. Get Your API Key

Sign up at [api.sentinel-algo.com/signup](https://api.sentinel-algo.com/signup) to get your API key.

**Free tier includes:**
- 100 requests/day
- Current regime access
- No credit card required

### 2. Make Your First Request

```bash
curl -H "X-API-Key: your_api_key_here" \
  https://api.sentinel-algo.com/regime/current
```

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
    "Sell premium — theta decay is your friend"
  ],
  "regime_duration_days": 5
}
```

---

## 🔐 Authentication

All API requests require an API key passed via the `X-API-Key` header:

```
X-API-Key: your_api_key_here
```

### Python Example

```python
import requests

API_KEY = "your_api_key_here"
BASE_URL = "https://api.sentinel-algo.com"

headers = {"X-API-Key": API_KEY}
response = requests.get(f"{BASE_URL}/regime/current", headers=headers)
data = response.json()

print(f"Current regime: {data['regime']}")
```

### JavaScript Example

```javascript
const API_KEY = "your_api_key_here";
const BASE_URL = "https://api.sentinel-algo.com";

async function getCurrentRegime() {
  const response = await fetch(`${BASE_URL}/regime/current`, {
    headers: {
      "X-API-Key": API_KEY
    }
  });
  
  const data = await response.json();
  console.log(`Current regime: ${data.regime}`);
  return data;
}

getCurrentRegime();
```

---

## 📡 Endpoints

### `GET /regime/current`

Get the current SPY market regime classification with real-time metrics.

**Headers:**
- `X-API-Key` (required): Your API key

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
    "Sell premium — theta decay is your friend"
  ],
  "regime_duration_days": 5
}
```

**Regime Types:**
- `STABLE` - Low volatility, mean-reverting (ideal for premium selling)
- `FRAGILE_ACCEL` - Acceleration instability (watch for momentum shifts)
- `FRAGILE_DIV` - Divergence instability (beware whipsaws)
- `FRAGILE_BOTH` - High chaos (reduce size, widen strikes)

**Metrics Explained:**
- `accel_z` - Acceleration instability Z-score (> 1.0 = unstable)
- `div_z` - Divergence instability Z-score (> 1.0 = unstable)
- `signal_strength` - Overall regime signal strength (max of accel_z and div_z)
- `vix` - Current VIX level (market fear gauge)
- `rv20` - 20-day realized volatility (annualized %)

**Python Example:**
```python
import requests

response = requests.get(
    "https://api.sentinel-algo.com/regime/current",
    headers={"X-API-Key": "your_api_key_here"}
)

regime_data = response.json()

if regime_data['regime'] == 'STABLE':
    print("✅ STABLE regime - PCS strategies optimal")
else:
    print(f"⚠️ {regime_data['regime']} regime - adjust strategy")

print(f"Signal strength: {regime_data['metrics']['signal_strength']}")
```

---

### `GET /regime/history?days=N`

Get historical regime classifications for the last N trading days.

**Headers:**
- `X-API-Key` (required): Your API key

**Query Parameters:**
- `days` (optional, default: 30, max: 365): Number of trading days to retrieve

**Tier Restrictions:**
- Free: ❌ Not available
- Basic: ✅ Up to 90 days
- Pro: ✅ Up to 365 days
- Enterprise: ✅ Unlimited

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

**Python Example:**
```python
import pandas as pd
import requests

response = requests.get(
    "https://api.sentinel-algo.com/regime/history?days=60",
    headers={"X-API-Key": "your_api_key_here"}
)

data = response.json()

# Convert to DataFrame for analysis
df = pd.DataFrame(data['data'])
df['date'] = pd.to_datetime(df['date'])

# Analyze regime distribution
print(f"Total days: {data['total_days']}")
print(f"Regime distribution: {data['regime_distribution']}")

# Find regime changes
df['regime_change'] = df['regime'] != df['regime'].shift(1)
changes = df[df['regime_change']]
print(f"\nRegime changes: {len(changes)}")
```

---

### `GET /regime/transitions?since=YYYY-MM-DD`

Get regime transition events (when regime changed) since a specific date.

**Headers:**
- `X-API-Key` (required): Your API key

**Query Parameters:**
- `since` (required): Start date in YYYY-MM-DD format

**Tier Restrictions:**
- Free: ❌ Not available
- Basic: ✅ Last 90 days
- Pro: ✅ Last 365 days
- Enterprise: ✅ Unlimited

**Response:**
```json
{
  "transitions": [
    {
      "date": "2026-02-15",
      "from_regime": "STABLE",
      "to_regime": "FRAGILE_DIV",
      "trigger": "Divergence instability detected",
      "duration_before_change_days": 7
    },
    {
      "date": "2026-02-08",
      "from_regime": "FRAGILE_ACCEL",
      "to_regime": "STABLE",
      "trigger": "Signal strength: 0.45",
      "duration_before_change_days": 3
    }
  ],
  "total_transitions": 2,
  "avg_regime_duration_days": 5.0
}
```

**Python Example:**
```python
from datetime import datetime, timedelta

# Get transitions from last 30 days
since_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

response = requests.get(
    f"https://api.sentinel-algo.com/regime/transitions?since={since_date}",
    headers={"X-API-Key": "your_api_key_here"}
)

data = response.json()

print(f"Regime transitions in last 30 days: {data['total_transitions']}")
print(f"Average regime duration: {data['avg_regime_duration_days']} days")

# Alert on recent transition to FRAGILE regime
for t in data['transitions']:
    if 'FRAGILE' in t['to_regime']:
        print(f"⚠️ {t['date']}: Transitioned to {t['to_regime']} - {t['trigger']}")
```

---

### `POST /regime/classify`

Classify custom OHLCV data (bring your own data).

**Headers:**
- `X-API-Key` (required): Your API key
- `Content-Type: application/json`

**Tier Restrictions:**
- Free: ❌ Not available
- Basic: ❌ Not available
- Pro: ✅ 1,000 classifications/day
- Enterprise: ✅ Unlimited

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

**Requirements:**
- Minimum 60 bars (3 hours of 5-min data or 3 months of daily)
- Must include VIX value for volatility context

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

**Python Example:**
```python
import yfinance as yf

# Fetch QQQ data
qqq = yf.Ticker("QQQ")
hist = qqq.history(period="3mo")

# Format for API
bars = []
for timestamp, row in hist.iterrows():
    bars.append({
        "timestamp": timestamp.isoformat(),
        "open": row['Open'],
        "high": row['High'],
        "low": row['Low'],
        "close": row['Close'],
        "volume": int(row['Volume'])
    })

# Get VIX
vix = yf.Ticker("^VIX")
vix_current = vix.history(period="1d")['Close'].iloc[-1]

# Classify
response = requests.post(
    "https://api.sentinel-algo.com/regime/classify",
    headers={"X-API-Key": "your_api_key_here"},
    json={
        "symbol": "QQQ",
        "data": bars,
        "vix_value": vix_current
    }
)

result = response.json()
print(f"QQQ Regime: {result['regime']} (confidence: {result['confidence']:.2%})")
```

---

## ⚡ Rate Limits

Rate limits are enforced per API key based on subscription tier:

| Tier | Requests/Day | Requests/Minute |
|------|-------------|-----------------|
| Free | 100 | 10 |
| Basic | 5,000 | 100 |
| Pro | 50,000 | 500 |
| Enterprise | Unlimited | 1,000+ |

**Rate Limit Headers:**

All responses include rate limit info in headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1708372800
```

**Handling Rate Limits:**

```python
response = requests.get(
    "https://api.sentinel-algo.com/regime/current",
    headers={"X-API-Key": "your_api_key_here"}
)

if response.status_code == 429:
    reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
    print(f"Rate limit exceeded. Resets at {reset_time}")
else:
    data = response.json()
```

---

## 🛡️ Error Handling

### HTTP Status Codes

- `200 OK` - Request successful
- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Invalid API key
- `403 Forbidden` - Feature not available in your tier
- `429 Too Many Requests` - Rate limit exceeded
- `503 Service Unavailable` - Service temporarily down

### Error Response Format

```json
{
  "detail": "Invalid API key"
}
```

**Python Error Handling:**

```python
try:
    response = requests.get(
        "https://api.sentinel-algo.com/regime/current",
        headers={"X-API-Key": "your_api_key_here"}
    )
    response.raise_for_status()
    data = response.json()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Invalid API key")
    elif e.response.status_code == 429:
        print("Rate limit exceeded - upgrade tier or wait")
    elif e.response.status_code == 403:
        print("Feature not available in your tier - upgrade to access")
    else:
        print(f"API error: {e}")
```

---

## 🔔 WebSocket (Pro/Enterprise Only)

Real-time regime updates pushed every 15 minutes during market hours (9:30 AM - 4:00 PM ET).

**Connection:**

```javascript
const ws = new WebSocket(
  'wss://api.sentinel-algo.com/regime/websocket?api_key=your_api_key_here'
);

ws.onopen = () => {
  console.log('Connected to regime stream');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.event === 'regime_update') {
    console.log(`Regime: ${data.regime}`);
    console.log(`Signal strength: ${data.metrics.signal_strength}`);
    
    // Alert on regime change
    if (data.regime !== currentRegime) {
      alert(`Regime changed to ${data.regime}!`);
    }
  }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected from regime stream');
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

---

## 🐍 Python SDK (Coming Soon)

```python
from regime_api import RegimeClient

client = RegimeClient(api_key="your_api_key_here")

# Get current regime
regime = client.get_current()
print(f"Current: {regime.regime} (strength: {regime.metrics.signal_strength})")

# Get history as DataFrame
df = client.get_history(days=60)
print(df.head())

# Stream real-time updates
for update in client.stream():
    print(f"Regime update: {update.regime}")
```

Install: `pip install regime-api-sdk` (coming Q2 2026)

---

## 📊 Use Cases

### 1. Trading Bot Integration

```python
def should_trade_pcs(regime_data):
    """Check if regime is favorable for put credit spreads."""
    if regime_data['regime'] == 'STABLE':
        if regime_data['metrics']['signal_strength'] < 0.5:
            return True, "Strong STABLE regime - PCS optimal"
    elif regime_data['regime'] in ['FRAGILE_ACCEL', 'FRAGILE_DIV']:
        return False, f"{regime_data['regime']} regime - skip PCS"
    
    return False, "Neutral regime"

# In your trading loop
regime = requests.get(
    "https://api.sentinel-algo.com/regime/current",
    headers={"X-API-Key": "your_api_key_here"}
).json()

should_trade, reason = should_trade_pcs(regime)
if should_trade:
    print(f"✅ Trading signal: {reason}")
    # Execute trade logic
else:
    print(f"⏸️  Skipping trade: {reason}")
```

### 2. Discord/Telegram Alert Bot

```python
import discord
import asyncio

client = discord.Client()

async def regime_monitor():
    """Send alerts on regime changes."""
    last_regime = None
    
    while True:
        response = requests.get(
            "https://api.sentinel-algo.com/regime/current",
            headers={"X-API-Key": "your_api_key_here"}
        )
        regime_data = response.json()
        current_regime = regime_data['regime']
        
        if last_regime and current_regime != last_regime:
            channel = client.get_channel(YOUR_CHANNEL_ID)
            await channel.send(
                f"🚨 **REGIME CHANGE ALERT** 🚨\n"
                f"{last_regime} → {current_regime}\n"
                f"Signal strength: {regime_data['metrics']['signal_strength']}"
            )
        
        last_regime = current_regime
        await asyncio.sleep(900)  # Check every 15 minutes

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    client.loop.create_task(regime_monitor())

client.run('your_discord_bot_token')
```

### 3. Backtesting Framework

```python
import pandas as pd
import backtrader as bt

class RegimeFilter(bt.Strategy):
    def __init__(self):
        # Load historical regime data
        self.regime_df = pd.read_csv('regime_history.csv')
        self.regime_df['Date'] = pd.to_datetime(self.regime_df['Date'])
        self.regime_df = self.regime_df.set_index('Date')
    
    def next(self):
        current_date = self.datas[0].datetime.date(0)
        
        # Look up regime for this date
        if current_date in self.regime_df.index:
            regime = self.regime_df.loc[current_date, 'Regime']
            
            if regime == 'STABLE':
                # Execute PCS strategy
                if not self.position:
                    self.sell()  # Sell put spread
            elif regime in ['FRAGILE_BOTH', 'FRAGILE_DIV']:
                # Close positions in fragile regimes
                if self.position:
                    self.close()
```

---

## 💡 Best Practices

1. **Cache Results**: Cache regime data for 15 minutes (it updates every 15 min)
2. **Handle Errors Gracefully**: Always wrap API calls in try/except blocks
3. **Monitor Rate Limits**: Track usage to avoid hitting limits unexpectedly
4. **Use WebSocket for Real-Time**: If you need updates immediately, use WebSocket (Pro+ tier)
5. **Combine with Other Signals**: Regime data is powerful but use it as one input in multi-signal strategies

---

## 🆘 Support

- **Documentation:** [docs.sentinel-algo.com/regime-api](https://docs.sentinel-algo.com/regime-api)
- **Email:** support@sentinel-algo.com
- **Discord:** [discord.gg/sentinel-algo](https://discord.gg/sentinel-algo)
- **Twitter/X:** [@Sentinel_Algo](https://x.com/Sentinel_Algo)

**Response Times:**
- Free: Community support (Discord)
- Basic: Email support (24-48h)
- Pro: Priority email (12-24h)
- Enterprise: Phone + Slack channel (4h SLA)

---

**Happy trading! 📈**
