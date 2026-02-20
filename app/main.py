"""
Regime Classifier API - FastAPI Application
Built by Sentinel Global Enterprises
"""

from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
from pathlib import Path
import os
import hashlib
import time
from collections import defaultdict

# ───────────────────────────────────────────────────────────────────
# CONFIG
# ───────────────────────────────────────────────────────────────────

REGIME_DATA_PATH = Path(os.getenv("REGIME_DATA_PATH", "/mnt/c/NinjaTrader/data/regime_data.csv"))
API_VERSION = "1.0.0"

# Simple in-memory rate limiting (replace with Redis for production)
rate_limit_storage = defaultdict(list)

# Tier limits (requests per day)
TIER_LIMITS = {
    "free": 100,
    "basic": 5000,
    "pro": 50000,
    "enterprise": 999999,
}

# Tier features
TIER_FEATURES = {
    "free": {"history_days": 0, "transitions": False, "classify": False, "websocket": False},
    "basic": {"history_days": 90, "transitions": True, "classify": False, "websocket": False},
    "pro": {"history_days": 365, "transitions": True, "classify": True, "websocket": True},
    "enterprise": {"history_days": 999999, "transitions": True, "classify": True, "websocket": True},
}

# Mock API key storage (replace with database in production)
# Format: {api_key_hash: {"tier": "free", "email": "user@example.com"}}
API_KEYS = {
    hashlib.sha256("demo_free_key".encode()).hexdigest(): {"tier": "free", "email": "demo@sentinel-algo.com"},
    hashlib.sha256("demo_basic_key".encode()).hexdigest(): {"tier": "basic", "email": "basic@sentinel-algo.com"},
    hashlib.sha256("demo_pro_key".encode()).hexdigest(): {"tier": "pro", "email": "pro@sentinel-algo.com"},
}

# ───────────────────────────────────────────────────────────────────
# MODELS
# ───────────────────────────────────────────────────────────────────

class RegimeResponse(BaseModel):
    regime: str
    timestamp: datetime
    spy_price: Optional[float] = None
    metrics: Dict[str, Optional[float]]
    trading_implications: List[str]
    regime_duration_days: int

class HistoryItem(BaseModel):
    date: str
    regime: str
    accel_z: float
    div_z: float
    signal_strength: float

class HistoryResponse(BaseModel):
    data: List[HistoryItem]
    total_days: int
    regime_distribution: Dict[str, int]

class TransitionItem(BaseModel):
    date: str
    from_regime: str
    to_regime: str
    trigger: str
    duration_before_change_days: int

class TransitionsResponse(BaseModel):
    transitions: List[TransitionItem]
    total_transitions: int
    avg_regime_duration_days: float

class OHLCVBar(BaseModel):
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

class ClassifyRequest(BaseModel):
    symbol: str
    data: List[OHLCVBar]
    vix_value: float = Field(..., description="Current VIX level")

class ClassifyResponse(BaseModel):
    regime: str
    confidence: float
    metrics: Dict[str, float]
    warning: Optional[str] = None

# ───────────────────────────────────────────────────────────────────
# APP SETUP
# ───────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Regime Classifier API",
    description="Real-time market regime classification powered by HMM",
    version=API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ───────────────────────────────────────────────────────────────────
# AUTHENTICATION & RATE LIMITING
# ───────────────────────────────────────────────────────────────────

def hash_key(api_key: str) -> str:
    """Hash API key for secure storage lookup."""
    return hashlib.sha256(api_key.encode()).hexdigest()

def validate_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> Dict[str, Any]:
    """Validate API key and return user info."""
    key_hash = hash_key(x_api_key)
    if key_hash not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return API_KEYS[key_hash]

def check_rate_limit(user_info: dict, request: Request):
    """Check if user has exceeded rate limit."""
    tier = user_info["tier"]
    limit = TIER_LIMITS[tier]
    
    # Get user's request history (last 24 hours)
    now = time.time()
    cutoff = now - 86400  # 24 hours ago
    key = user_info["email"]
    
    # Clean old entries
    rate_limit_storage[key] = [t for t in rate_limit_storage[key] if t > cutoff]
    
    # Check limit
    if len(rate_limit_storage[key]) >= limit:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Tier '{tier}' allows {limit} requests/day. Upgrade at api.sentinel-algo.com"
        )
    
    # Record this request
    rate_limit_storage[key].append(now)

def check_feature_access(user_info: dict, feature: str, required_value: Any = True):
    """Check if user's tier has access to a feature."""
    tier = user_info["tier"]
    features = TIER_FEATURES[tier]
    
    if feature not in features:
        raise HTTPException(status_code=403, detail=f"Feature '{feature}' not available in tier '{tier}'")
    
    if isinstance(required_value, int):
        if features[feature] < required_value:
            raise HTTPException(
                status_code=403,
                detail=f"Feature '{feature}' limited to {features[feature]} in tier '{tier}'. Upgrade for more access."
            )
    elif features[feature] != required_value:
        raise HTTPException(
            status_code=403,
            detail=f"Feature '{feature}' not available in tier '{tier}'. Upgrade to access this feature."
        )

# ───────────────────────────────────────────────────────────────────
# DATA LOADING
# ───────────────────────────────────────────────────────────────────

def load_regime_data() -> pd.DataFrame:
    """Load regime data from CSV."""
    if not REGIME_DATA_PATH.exists():
        raise HTTPException(status_code=503, detail="Regime data not available. Contact support.")
    
    df = pd.read_csv(REGIME_DATA_PATH)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def get_current_regime() -> Dict[str, Any]:
    """Get current regime classification."""
    df = load_regime_data()
    latest = df.iloc[-1]
    
    # Get regime duration
    regime = latest['Regime']
    duration = 1
    for i in range(len(df) - 2, -1, -1):
        if df.iloc[i]['Regime'] == regime:
            duration += 1
        else:
            break
    
    # Trading implications
    implications = get_trading_implications(regime, latest['SignalStrength'])
    
    return {
        "regime": regime,
        "timestamp": datetime.now(),
        "spy_price": None,  # Would fetch from Yahoo Finance in production
        "metrics": {
            "accel_z": float(latest['AccelZ']),
            "div_z": float(latest['DivZ']),
            "signal_strength": float(latest['SignalStrength']),
            "vix": None,  # Would fetch from Yahoo Finance
            "rv20": None,  # Would calculate from recent data
        },
        "trading_implications": implications,
        "regime_duration_days": duration,
    }

def get_trading_implications(regime: str, signal_strength: float) -> List[str]:
    """Get trading implications for a regime."""
    implications = []
    
    if regime == "STABLE":
        implications.append("Put credit spreads (PCS) are optimal in this regime")
        implications.append("Sell premium — theta decay is your friend")
        if signal_strength < 0.5:
            implications.append("Consider buying cheap options for asymmetric bets")
    elif regime == "FRAGILE_ACCEL":
        implications.append("Acceleration instability detected — momentum may shift")
        implications.append("Tighten stops on mean-reversion positions")
        implications.append("Watch for trend breaks")
    elif regime == "FRAGILE_DIV":
        implications.append("Divergence instability — beware whipsaws")
        implications.append("Avoid counter-trend entries")
        implications.append("Wider strikes recommended for credit spreads")
    elif regime == "FRAGILE_BOTH":
        implications.append("High chaos regime — reduce position size")
        implications.append("Widen strikes significantly")
        implications.append("Consider cash positions until clarity returns")
    
    return implications

# ───────────────────────────────────────────────────────────────────
# ENDPOINTS
# ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    """API root - health check."""
    return {
        "name": "Regime Classifier API",
        "version": API_VERSION,
        "status": "operational",
        "docs": "/docs",
        "signup": "https://api.sentinel-algo.com/signup",
    }

@app.get("/health")
def health():
    """Health check endpoint."""
    try:
        load_regime_data()
        return {"status": "healthy", "timestamp": datetime.now()}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )

@app.get("/regime/current", response_model=RegimeResponse)
def get_current(
    request: Request,
    user_info: dict = Depends(validate_api_key),
):
    """Get current SPY regime classification."""
    check_rate_limit(user_info, request)
    
    data = get_current_regime()
    return RegimeResponse(**data)

@app.get("/regime/history", response_model=HistoryResponse)
def get_history(
    days: int = 30,
    request: Request = None,
    user_info: dict = Depends(validate_api_key),
):
    """Get historical regime data."""
    check_rate_limit(user_info, request)
    check_feature_access(user_info, "history_days", days)
    
    df = load_regime_data()
    
    # Get last N days
    df_filtered = df.tail(min(days, len(df)))
    
    # Build response
    data = []
    for _, row in df_filtered.iterrows():
        data.append(HistoryItem(
            date=row['Date'].strftime('%Y-%m-%d'),
            regime=row['Regime'],
            accel_z=float(row['AccelZ']),
            div_z=float(row['DivZ']),
            signal_strength=float(row['SignalStrength']),
        ))
    
    # Calculate distribution
    distribution = df_filtered['Regime'].value_counts().to_dict()
    
    return HistoryResponse(
        data=data,
        total_days=len(data),
        regime_distribution=distribution,
    )

@app.get("/regime/transitions", response_model=TransitionsResponse)
def get_transitions(
    since: str,
    request: Request = None,
    user_info: dict = Depends(validate_api_key),
):
    """Get regime transition events."""
    check_rate_limit(user_info, request)
    check_feature_access(user_info, "transitions", True)
    
    df = load_regime_data()
    
    # Filter by date
    since_date = pd.to_datetime(since)
    df_filtered = df[df['Date'] >= since_date]
    
    # Find transitions
    transitions = []
    prev_regime = None
    prev_date = None
    duration = 0
    
    for i, row in df_filtered.iterrows():
        regime = row['Regime']
        date_str = row['Date'].strftime('%Y-%m-%d')
        
        if prev_regime is not None and regime != prev_regime:
            # Transition detected
            trigger = f"Signal strength: {row['SignalStrength']:.2f}"
            if row['AccelZ'] > 1.0 and row['DivZ'] > 1.0:
                trigger = "Both acceleration and divergence instability"
            elif row['AccelZ'] > 1.0:
                trigger = "Acceleration instability detected"
            elif row['DivZ'] > 1.0:
                trigger = "Divergence instability detected"
            
            transitions.append(TransitionItem(
                date=date_str,
                from_regime=prev_regime,
                to_regime=regime,
                trigger=trigger,
                duration_before_change_days=duration,
            ))
            duration = 0
        
        prev_regime = regime
        prev_date = date_str
        duration += 1
    
    avg_duration = sum(t.duration_before_change_days for t in transitions) / len(transitions) if transitions else 0
    
    return TransitionsResponse(
        transitions=transitions,
        total_transitions=len(transitions),
        avg_regime_duration_days=round(avg_duration, 1),
    )

@app.post("/regime/classify", response_model=ClassifyResponse)
def classify_custom(
    request_body: ClassifyRequest,
    request: Request = None,
    user_info: dict = Depends(validate_api_key),
):
    """Classify custom OHLCV data."""
    check_rate_limit(user_info, request)
    check_feature_access(user_info, "classify", True)
    
    # Validate data length
    if len(request_body.data) < 60:
        raise HTTPException(
            status_code=400,
            detail="Minimum 60 bars required for classification"
        )
    
    # Simple classification logic (would use PyramidalHMM in production)
    # For MVP, use simplified rules-based classification
    closes = [bar.close for bar in request_body.data]
    
    # Calculate metrics
    returns = np.diff(np.log(closes))
    rv20 = float(np.std(returns[-20:]) * np.sqrt(252) * 100) if len(returns) >= 20 else 0.0
    
    # Simplified regime classification
    if request_body.vix_value > 25:
        regime = "FRAGILE_BOTH"
        confidence = 0.85
    elif rv20 > 20:
        regime = "FRAGILE_ACCEL"
        confidence = 0.75
    elif rv20 < 12:
        regime = "STABLE"
        confidence = 0.90
    else:
        regime = "STABLE"
        confidence = 0.70
    
    metrics = {
        "accel_z": 0.0,  # Would calculate with full HMM model
        "div_z": 0.0,
        "signal_strength": 0.0,
        "rv20": rv20,
    }
    
    warning = None
    if len(request_body.data) < 100:
        warning = "Less than 100 bars provided — classification may be less accurate"
    
    return ClassifyResponse(
        regime=regime,
        confidence=confidence,
        metrics=metrics,
        warning=warning,
    )

# ───────────────────────────────────────────────────────────────────
# ADMIN ENDPOINTS (for internal monitoring)
# ───────────────────────────────────────────────────────────────────

@app.get("/admin/stats")
def admin_stats(admin_key: str = Header(..., alias="X-Admin-Key")):
    """Get API usage stats (admin only)."""
    if admin_key != os.getenv("ADMIN_KEY", "change_me_in_production"):
        raise HTTPException(status_code=403, detail="Invalid admin key")
    
    total_requests = sum(len(v) for v in rate_limit_storage.values())
    users_by_tier = defaultdict(int)
    for user_info in API_KEYS.values():
        users_by_tier[user_info["tier"]] += 1
    
    return {
        "total_requests_24h": total_requests,
        "active_users_24h": len(rate_limit_storage),
        "users_by_tier": dict(users_by_tier),
        "total_users": len(API_KEYS),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
