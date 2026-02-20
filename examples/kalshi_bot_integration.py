#!/usr/bin/env python3
"""
Example: Integrate Regime Classifier API with Kalshi Bot

Shows how to replace local regime detection with API calls.
This makes the bot stateless and allows sharing regime data across multiple bots.
"""

import requests
from typing import Dict, Any

# Configuration
REGIME_API_URL = "https://api.sentinel-algo.com"  # Or localhost for testing
REGIME_API_KEY = "your_api_key_here"  # Get from api.sentinel-algo.com

class RegimeAPI:
    """Simple client for Regime Classifier API."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.sentinel-algo.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"X-API-Key": api_key}
    
    def get_current_regime(self) -> Dict[str, Any]:
        """Get current market regime."""
        response = requests.get(
            f"{self.base_url}/regime/current",
            headers=self.headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    
    def should_trade_pcs(self) -> tuple[bool, str]:
        """
        Check if current regime is favorable for put credit spreads.
        
        Returns:
            (should_trade, reason)
        """
        regime_data = self.get_current_regime()
        regime = regime_data['regime']
        signal_strength = regime_data['metrics']['signal_strength']
        
        if regime == 'STABLE' and signal_strength < 0.5:
            return True, "STABLE regime with low signal strength - PCS optimal"
        elif regime == 'STABLE':
            return True, f"STABLE regime (strength={signal_strength:.2f}) - PCS acceptable"
        elif regime == 'FRAGILE_DIV':
            return False, "FRAGILE_DIV regime - avoid PCS (whipsaw risk)"
        elif regime == 'FRAGILE_ACCEL':
            return False, "FRAGILE_ACCEL regime - avoid PCS (momentum shifts)"
        elif regime == 'FRAGILE_BOTH':
            return False, "FRAGILE_BOTH regime - stay out (high chaos)"
        else:
            return False, f"Unknown regime: {regime}"


# ─────────────────────────────────────────────────────────────────────
# EXAMPLE 1: Replace detect_regime() in kalshi_bot.py
# ─────────────────────────────────────────────────────────────────────

def generate_signal_with_api(klines):
    """
    Drop-in replacement for generate_signal_v2() in kalshi_bot.py
    Uses Regime API instead of local detection.
    """
    # Initialize API client (cache this in production)
    regime_api = RegimeAPI(api_key=REGIME_API_KEY)
    
    # Get current regime from API
    try:
        regime_data = regime_api.get_current_regime()
        regime = regime_data['regime']
        signal_strength = regime_data['metrics']['signal_strength']
    except Exception as e:
        print(f"⚠️  Regime API error: {e}")
        print("   Falling back to no-regime-filter mode")
        regime = None
        signal_strength = 0
    
    # ... rest of your signal logic (RSI, MACD, etc.)
    
    # Regime filter (replace local detect_regime() logic)
    if regime == 'FRAGILE_DIV':
        return None, {"skip_reason": "regime_api_fragile_div"}
    
    # If regime is STABLE or None (API error), continue with normal signal logic
    # Your existing signal generation code here...
    
    signal_meta = {
        "regime": regime,
        "regime_source": "api",  # Track that we used the API
        "signal_strength": signal_strength,
    }
    
    return "LONG", signal_meta  # Or your actual signal logic


# ─────────────────────────────────────────────────────────────────────
# EXAMPLE 2: Pre-trade filter for any strategy
# ─────────────────────────────────────────────────────────────────────

def should_trade_today(api_key: str) -> bool:
    """
    Check regime before market open to decide if trading today.
    
    Usage:
        if should_trade_today(API_KEY):
            start_trading_bot()
        else:
            print("Skipping trading today - unfavorable regime")
    """
    regime_api = RegimeAPI(api_key)
    
    try:
        should_trade, reason = regime_api.should_trade_pcs()
        print(f"🔬 Regime check: {reason}")
        return should_trade
    except Exception as e:
        print(f"⚠️  Regime API error: {e}")
        print("   Trading anyway (no regime filter)")
        return True  # Or False if you prefer to skip on API errors


# ─────────────────────────────────────────────────────────────────────
# EXAMPLE 3: Multi-bot coordination (same regime data everywhere)
# ─────────────────────────────────────────────────────────────────────

def get_shared_regime(api_key: str) -> str:
    """
    All your bots (Kalshi, PCS, etc.) call this to get the same regime.
    No more inconsistencies from local calculations!
    """
    regime_api = RegimeAPI(api_key)
    data = regime_api.get_current_regime()
    return data['regime']


# ─────────────────────────────────────────────────────────────────────
# EXAMPLE 4: Backtest with historical regime data
# ─────────────────────────────────────────────────────────────────────

def backtest_with_regime_api(api_key: str, days: int = 90):
    """
    Fetch historical regime data for backtesting.
    
    Requires: Basic tier or higher (free tier doesn't have history access)
    """
    headers = {"X-API-Key": api_key}
    response = requests.get(
        f"{REGIME_API_URL}/regime/history?days={days}",
        headers=headers
    )
    
    if response.status_code == 403:
        print("⚠️  History endpoint not available in Free tier")
        print("   Upgrade to Basic ($19/mo) for 90 days of history")
        return None
    
    response.raise_for_status()
    data = response.json()
    
    # Convert to DataFrame for analysis
    import pandas as pd
    df = pd.DataFrame(data['data'])
    df['date'] = pd.to_datetime(df['date'])
    
    print(f"📊 Loaded {len(df)} days of regime data")
    print(f"   Regime distribution: {data['regime_distribution']}")
    
    return df


# ─────────────────────────────────────────────────────────────────────
# EXAMPLE 5: Discord/Telegram alert bot
# ─────────────────────────────────────────────────────────────────────

def regime_alert_bot(api_key: str, interval_minutes: int = 15):
    """
    Monitors regime changes and sends alerts.
    
    Run this as a background process:
        python kalshi_bot_integration.py --alert-mode
    """
    import time
    
    regime_api = RegimeAPI(api_key)
    last_regime = None
    
    print("🤖 Regime Alert Bot started")
    print(f"   Checking every {interval_minutes} minutes")
    
    while True:
        try:
            data = regime_api.get_current_regime()
            current_regime = data['regime']
            signal_strength = data['metrics']['signal_strength']
            
            if last_regime and current_regime != last_regime:
                # Regime changed!
                print(f"\n🚨 REGIME CHANGE ALERT!")
                print(f"   {last_regime} → {current_regime}")
                print(f"   Signal strength: {signal_strength:.2f}")
                print(f"   Implications: {data['trading_implications'][0]}")
                
                # Send to Discord/Telegram (implement your webhook here)
                # send_discord_alert(f"Regime changed: {last_regime} → {current_regime}")
            
            last_regime = current_regime
            
        except Exception as e:
            print(f"⚠️  Error checking regime: {e}")
        
        # Wait before next check
        time.sleep(interval_minutes * 60)


# ─────────────────────────────────────────────────────────────────────
# USAGE EXAMPLES
# ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    
    # Example 1: Check if you should trade today
    print("=" * 60)
    print("Example 1: Should I trade today?")
    print("=" * 60)
    
    api_key = "demo_free_key"  # Replace with your actual API key
    
    if should_trade_today(api_key):
        print("✅ Green light - favorable regime for trading")
    else:
        print("🛑 Red light - skip trading today")
    
    print()
    
    # Example 2: Get current regime for all bots
    print("=" * 60)
    print("Example 2: Shared regime across all bots")
    print("=" * 60)
    
    regime = get_shared_regime(api_key)
    print(f"Current regime: {regime}")
    print("   (Kalshi bot, PCS bot, and momentum bot all see the same regime)")
    
    print()
    
    # Example 3: Detailed regime data
    print("=" * 60)
    print("Example 3: Full regime data")
    print("=" * 60)
    
    regime_api = RegimeAPI(api_key)
    data = regime_api.get_current_regime()
    
    print(f"Regime: {data['regime']}")
    print(f"Duration: {data['regime_duration_days']} days")
    print(f"Metrics:")
    print(f"  - Accel Z: {data['metrics']['accel_z']:.2f}")
    print(f"  - Div Z: {data['metrics']['div_z']:.2f}")
    print(f"  - Signal Strength: {data['metrics']['signal_strength']:.2f}")
    print(f"Trading Implications:")
    for implication in data['trading_implications']:
        print(f"  • {implication}")
    
    print()
    print("=" * 60)
    print("💡 Integration Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Replace REGIME_API_KEY with your actual API key")
    print("2. Replace local detect_regime() calls with regime_api.get_current_regime()")
    print("3. Test locally, then deploy")
    print()
    print("Benefits:")
    print("✅ No more local regime calculation (saves CPU)")
    print("✅ Consistent regime across all your bots")
    print("✅ Access to historical data for backtesting")
    print("✅ Real-time updates via WebSocket (Pro tier)")
