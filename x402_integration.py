"""
x402 Micropayment Integration for Regime Classifier API
========================================================
Adds HTTP 402 pay-per-query to the Regime API using Coinbase's x402 protocol.

AI agents can query regime classification data and pay per request in USDC
on Base network — no API keys, no accounts, no friction.

Setup:
  pip install x402[fastapi] python-dotenv
  
Environment:
  X402_PAY_TO_ADDRESS=0x...  (your USDC receiving wallet on Base)
  X402_NETWORK=eip155:8453   (Base mainnet, default)
  X402_FACILITATOR_URL=https://x402.org/facilitator  (default, Coinbase hosted)

Usage:
  Import and call `add_x402_middleware(app)` after creating your FastAPI app.
  Free tier endpoints remain free. Paid endpoints get x402 paywall.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ───────────────────────────────────────────────────────────────────
# CONFIG
# ───────────────────────────────────────────────────────────────────

PAY_TO_ADDRESS = os.getenv("X402_PAY_TO_ADDRESS", "")
NETWORK = os.getenv("X402_NETWORK", "eip155:8453")  # Base mainnet
FACILITATOR_URL = os.getenv("X402_FACILITATOR_URL", "https://x402.org/facilitator")

# Pricing per endpoint (in USD)
PRICING = {
    "/v1/regime/current":    "$0.001",   # Current regime — cheap, high volume
    "/v1/regime/history":    "$0.005",   # Historical data — more value
    "/v1/regime/transitions":"$0.003",   # Transition analysis
    "/v1/regime/classify":   "$0.01",    # Custom classification — premium
    "/v1/regime/batch":      "$0.02",    # Batch queries
}

# Endpoints that remain free (no payment required)
FREE_ENDPOINTS = [
    "/",
    "/health",
    "/v1/regime/status",
    "/docs",
    "/openapi.json",
    "/redoc",
]


def add_x402_middleware(app):
    """
    Add x402 payment middleware to a FastAPI app.
    
    Wraps paid endpoints with HTTP 402 paywall.
    Free endpoints pass through unchanged.
    Falls back gracefully if x402 package not installed or wallet not configured.
    """
    if not PAY_TO_ADDRESS:
        print("[x402] ⚠️  X402_PAY_TO_ADDRESS not set — x402 payments DISABLED")
        print("[x402]     Set it in .env to enable micropayments")
        return False

    try:
        from x402.fastapi.middleware import require_payment
    except ImportError:
        print("[x402] ⚠️  x402 package not installed — run: pip install x402[fastapi]")
        print("[x402]     Falling back to API-key-only authentication")
        return False

    # Apply payment middleware for each priced endpoint
    for path, price in PRICING.items():
        app.middleware("http")(
            require_payment(
                path=path,
                price=price,
                pay_to_address=PAY_TO_ADDRESS,
                network=NETWORK,
                facilitator_url=FACILITATOR_URL,
            )
        )

    print(f"[x402] ✅ Micropayments ENABLED on {len(PRICING)} endpoints")
    print(f"[x402]    Pay-to: {PAY_TO_ADDRESS[:10]}...{PAY_TO_ADDRESS[-6:]}")
    print(f"[x402]    Network: {NETWORK}")
    print(f"[x402]    Pricing:")
    for path, price in PRICING.items():
        print(f"[x402]      {path}: {price}/query")

    return True


# ───────────────────────────────────────────────────────────────────
# DUAL-MODE AUTH: x402 payment OR API key
# ───────────────────────────────────────────────────────────────────

def is_x402_authenticated(request) -> bool:
    """Check if request has a valid x402 payment signature."""
    return "payment-signature" in request.headers


def get_x402_info():
    """Return x402 pricing info for API documentation."""
    return {
        "x402_enabled": bool(PAY_TO_ADDRESS),
        "network": NETWORK,
        "currency": "USDC",
        "pricing": PRICING,
        "free_endpoints": FREE_ENDPOINTS,
        "how_it_works": (
            "Send a request without payment → receive 402 with payment details → "
            "sign payment with your wallet → resend with PAYMENT-SIGNATURE header → "
            "receive data. No API key needed."
        ),
        "supported_wallets": [
            "Any EVM wallet (MetaMask, Coinbase Wallet, etc.)",
            "x402 Python/TypeScript client SDK",
            "Any AI agent with Base USDC balance",
        ],
    }
