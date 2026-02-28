# 💰 x402 Micropayment Integration Guide

**Goal:** Enable AI agents to pay per query in USDC (on Base network) instead of using API keys.

**Why do this?**
- 🤖 AI agents can use your API without signup/API keys
- 💰 Get paid instantly per query (USDC on Base)
- 🚀 First-mover advantage (very few trading APIs support x402)
- 🔗 Agent-to-agent commerce (the future of AI)

**Time estimate:** 15-20 minutes  
**Cost:** $0 to set up (only pay Coinbase facilitator fees after 1,000 transactions/month — first 1,000 are FREE)

---

## What is x402?

**x402** is the HTTP 402 "Payment Required" protocol for micropayments.

**How it works:**
1. AI agent requests: `GET /regime/current` (no API key)
2. Your API responds: `402 Payment Required` + payment details
3. Agent signs payment with its USDC wallet (Base network)
4. Agent resends request with `PAYMENT-SIGNATURE` header
5. Coinbase facilitator verifies + settles payment
6. Your API returns data ✅
7. USDC deposited to your wallet on Base

**No accounts. No API keys. Just pay and get data.**

---

## Prerequisites

Before you start:

- [ ] Your Regime API is deployed to Render and working
- [ ] You have a way to receive crypto (exchange account or wallet)
- [ ] 10-15 minutes of time

---

## Step 1: Create a Base Wallet (10 minutes)

You need a **USDC-receiving wallet on Base network** to get paid.

### Option A: Coinbase Wallet (Recommended — Easiest)

1. **Download Coinbase Wallet:**
   - Go to https://www.coinbase.com/wallet
   - Download for your phone (iOS/Android)
   - Or use browser extension (Chrome)

2. **Create wallet:**
   - Open app → "Create new wallet"
   - Follow setup (save recovery phrase!)
   - Set a PIN

3. **Get your wallet address:**
   - Open wallet
   - Click **"Receive"**
   - Copy your wallet address (starts with `0x...`)
   - **Save this!** You'll need it in Step 2.

4. **Add Base network:**
   - In wallet, click network dropdown (top left)
   - Select **"Base"**
   - Confirm

5. **Optional: Get test USDC (for testing):**
   - Go to https://base.org/faucet
   - Paste your wallet address
   - Request test USDC (for testing payments)

### Option B: MetaMask (Alternative)

1. **Install MetaMask:**
   - Go to https://metamask.io
   - Install browser extension

2. **Create wallet:**
   - Follow setup prompts
   - Save recovery phrase

3. **Add Base network:**
   - Click network dropdown → "Add network"
   - Search "Base" → Add
   - Switch to Base network

4. **Copy wallet address:**
   - Click account name (top)
   - Click copy icon
   - **Save this!** You'll need it in Step 2.

### Option C: Use Your Exchange Deposit Address (Easiest but Limited)

**⚠️ Warning:** This only works if your exchange supports **Base network USDC deposits.**

Check if your exchange (Coinbase, Kraken, etc.) supports:
- **Asset:** USDC
- **Network:** Base (or "Base Mainnet")

If yes:
1. Log in to your exchange
2. Go to deposit USDC
3. Select **Base network**
4. Copy the deposit address
5. **Use this as your wallet address**

**Pros:** No new wallet needed, USDC goes straight to your exchange  
**Cons:** If exchange doesn't support Base, this won't work

---

✅ **You now have a wallet address that can receive USDC on Base!**

Example address: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb`

---

## Step 2: Add Wallet Address to Render (5 minutes)

Now tell your API where to receive payments.

1. **Go to Render Dashboard:**
   - https://dashboard.render.com → regime-api
   - Click **"Environment"** tab

2. **Add new environment variable:**
   - Click **"Add Environment Variable"**

| Key | Value |
|-----|-------|
| `X402_PAY_TO_ADDRESS` | `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb` |

   - **Replace with YOUR wallet address!**

3. **Save:**
   - Click **"Save Changes"**
   - Render will auto-redeploy (~30 seconds)

4. **Wait for redeploy:**
   - Watch the **"Events"** tab
   - Wait for "Deploy live" ✅

---

## Step 3: Verify x402 is Enabled (2 minutes)

Test that x402 is now active:

```bash
curl https://regime-api.onrender.com/x402/info
```

**Expected response:**
```json
{
  "x402_enabled": true,
  "network": "eip155:8453",
  "currency": "USDC",
  "pricing": {
    "/v1/regime/current": "$0.001",
    "/v1/regime/history": "$0.005",
    "/v1/regime/transitions": "$0.003",
    "/v1/regime/classify": "$0.01",
    "/v1/regime/batch": "$0.02"
  },
  "free_endpoints": ["/", "/health", "/x402/info"],
  "how_it_works": "Send a request without payment → receive 402..."
}
```

✅ **If you see `"x402_enabled": true` → It's live!**

---

## Step 4: Test a Payment Request (3 minutes)

Let's test the 402 response (you don't need to actually pay yet):

```bash
# Request regime data WITHOUT payment
curl -i https://regime-api.onrender.com/v1/regime/current
```

**Expected response:**
```
HTTP/2 402 Payment Required
payment-required: true
payment-amount: $0.001
payment-address: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
payment-chain: eip155:8453
payment-currency: USDC
facilitator-url: https://x402.org/facilitator

{
  "error": "Payment required",
  "price": "$0.001",
  "pay_to": "0x742d35...",
  "chain": "eip155:8453",
  "instructions": "Sign payment and include PAYMENT-SIGNATURE header"
}
```

✅ **If you see HTTP 402 → x402 is working!**

---

## How AI Agents Use It

AI agents with USDC wallets can now:

1. **Request data** (no API key needed)
2. **Get 402 response** with payment details
3. **Sign payment** with their wallet
4. **Resend request** with payment signature
5. **Get data** ✅

**Example Python client (for agents):**

```python
import requests
from x402 import X402Client

client = X402Client(wallet_private_key="...")

# Agent pays $0.001 USDC and gets regime data
response = client.get("https://regime-api.onrender.com/v1/regime/current")
regime = response.json()

print(regime['regime'])  # STABLE
```

**No API key. No signup. Just pay and use.**

---

## Pricing (What You Earn Per Query)

| Endpoint | Price | AI Agent Use Case |
|----------|-------|-------------------|
| `/v1/regime/current` | **$0.001** | Quick regime check before placing trade |
| `/v1/regime/history` | **$0.005** | Backtesting strategies |
| `/v1/regime/transitions` | **$0.003** | Analyzing regime stability |
| `/v1/regime/classify` | **$0.01** | Custom asset classification |
| `/v1/regime/batch` | **$0.02** | Batch processing for research |

**Revenue projection:**
- 1,000 queries/day × $0.003 avg = **$3/day = $90/month**
- 10,000 queries/day × $0.003 avg = **$30/day = $900/month**

**Coinbase facilitator fee:**
- First 1,000 transactions/month: **FREE**
- After 1,000: **$0.001 per transaction**

---

## Dual-Mode Auth (x402 + API Keys)

Your API now supports **both**:

1. **API Key mode** (existing):
   - Send `X-API-Key: your_key_here`
   - Uses your tier limits (Free/Basic/Pro)
   - Good for long-term customers

2. **x402 payment mode** (new):
   - No API key needed
   - Pay per query in USDC
   - Good for AI agents, one-off queries

**Both can coexist!** Same endpoints, same data.

---

## Marketing x402 Integration

Now that it's live, tell the world!

### Tweet Template

```
🤖💰 Our Regime API now accepts micropayments!

AI agents can now:
✅ Query market regimes with ZERO signup
✅ Pay per request in USDC (Base network)
✅ No API keys needed

Powered by x402 protocol

Try it: https://regime-api.onrender.com/x402/info

#AI #Crypto #Trading #x402
```

### DM the x402 Partner

If you have contact with the X commenter (@pylonx402 or similar):

```
Hey! Our Regime API is live with x402 integration:

https://regime-api.onrender.com

- 3-state HMM regime classifier (STABLE/TRENDING/HIGH_VOL)
- Pay per query ($0.001-$0.02)
- USDC on Base
- Returns regime + confidence + trading implications

Ready to test integration! Let me know if you want to connect your 20 capabilities.
```

### Add to Website

Update sentinel-algo.com with:
- "Now with x402 micropayments!" badge
- Link to x402/info endpoint
- Explanation for AI agents

---

## Monitoring x402 Payments

### Check Your Wallet Balance

- **Coinbase Wallet:** Open app → Base network → USDC balance
- **MetaMask:** Switch to Base network → USDC token
- **Exchange:** Check USDC deposits (Base network)

### Check Payment Activity

View transactions:
- **Basescan:** https://basescan.org/address/YOUR_ADDRESS
- Replace `YOUR_ADDRESS` with your wallet address
- See all incoming USDC payments

### Render Logs

- Go to Render dashboard → regime-api → **Logs**
- Look for: `[x402] Payment verified: $0.001 from 0x...`

---

## Troubleshooting

### x402_enabled is false
- Check `X402_PAY_TO_ADDRESS` is set in Render environment
- Wallet address must start with `0x` and be 42 characters
- Redeploy the service

### Agent payment fails
- Verify your wallet address is correct
- Check Base network is live (https://status.base.org)
- Ensure facilitator is reachable (https://x402.org)

### Not receiving payments
- Check wallet address in Render env vars
- View transactions on Basescan: https://basescan.org
- Payments might be on testnet (Base Goerli) if agent used test USDC

### 402 response missing headers
- Check Render logs for errors
- Verify `x402_integration.py` is in repo
- Ensure `pip install x402[fastapi]` in requirements.txt

---

## Advanced: Withdraw USDC to Fiat

Once you've accumulated USDC, you can:

1. **Transfer to exchange:**
   - Send USDC from wallet to Coinbase/Kraken
   - Select **Base network** for lowest fees
   - Sell USDC for USD/fiat

2. **Keep in USDC:**
   - USDC is stablecoin ($1 = 1 USDC)
   - Use for other DeFi/trading
   - Or just hold as USD equivalent

---

## Next Steps

✅ **x402 is live!** Now:

1. **Test with a friend** who has a USDC wallet
2. **Monitor payments** in your wallet
3. **Market it** — Tweet, DM partners, update website
4. **Track revenue** — Check wallet daily/weekly

---

## Quick Reference

| What | Where |
|------|-------|
| **x402 Info Endpoint** | https://regime-api.onrender.com/x402/info |
| **Your Wallet** | (your Base USDC address) |
| **View Transactions** | https://basescan.org/address/YOUR_ADDRESS |
| **Facilitator Docs** | https://x402.sh |
| **Base Faucet (testnet)** | https://base.org/faucet |

---

**Total setup time:** ~15 minutes  
**Total cost:** $0  
**Revenue potential:** $90-900+/month

**You're now accepting micropayments from AI agents! 🤖💰**
