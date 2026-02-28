#!/bin/bash

# ═══════════════════════════════════════════════════════════════════
# Regime API — Live Endpoint Test Script
# ═══════════════════════════════════════════════════════════════════
# Run this after deploying to Render to verify all endpoints work.
# Usage: bash TEST_SCRIPT.sh [API_URL]
# Example: bash TEST_SCRIPT.sh https://regime-api.onrender.com
# ═══════════════════════════════════════════════════════════════════

set -e  # Exit on error

# ───────────────────────────────────────────────────────────────────
# CONFIG
# ───────────────────────────────────────────────────────────────────

API_URL="${1:-https://regime-api.onrender.com}"
ADMIN_KEY="sentinel2026"
DEMO_KEY="demo_free_key"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ───────────────────────────────────────────────────────────────────
# TEST FUNCTIONS
# ───────────────────────────────────────────────────────────────────

test_endpoint() {
    local name="$1"
    local url="$2"
    local headers="$3"
    
    echo -n "Testing $name... "
    
    if [ -z "$headers" ]; then
        response=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    else
        response=$(curl -s -o /dev/null -w "%{http_code}" -H "$headers" "$url")
    fi
    
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✅ PASS${NC} (HTTP $response)"
        return 0
    else
        echo -e "${RED}❌ FAIL${NC} (HTTP $response)"
        return 1
    fi
}

test_endpoint_json() {
    local name="$1"
    local url="$2"
    local headers="$3"
    local expected_key="$4"
    
    echo -n "Testing $name... "
    
    if [ -z "$headers" ]; then
        response=$(curl -s "$url")
    else
        response=$(curl -s -H "$headers" "$url")
    fi
    
    # Check if response contains expected key
    if echo "$response" | grep -q "\"$expected_key\""; then
        echo -e "${GREEN}✅ PASS${NC}"
        echo "   Response preview: $(echo "$response" | head -c 100)..."
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        echo "   Response: $response"
        return 1
    fi
}

# ───────────────────────────────────────────────────────────────────
# BANNER
# ───────────────────────────────────────────────────────────────────

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Regime API — Live Endpoint Test"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Testing API at: $API_URL"
echo ""

# ───────────────────────────────────────────────────────────────────
# TESTS
# ───────────────────────────────────────────────────────────────────

PASSED=0
FAILED=0

# Test 1: Health Check (Public)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Public Endpoints (No Auth Required)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if test_endpoint_json "Health Check" "$API_URL/health" "" "status"; then
    ((PASSED++))
else
    ((FAILED++))
fi

# Test 2: Root Endpoint (Public)
if test_endpoint "Root Endpoint" "$API_URL/" ""; then
    ((PASSED++))
else
    ((FAILED++))
fi

# Test 3: x402 Info (Public)
if test_endpoint_json "x402 Info" "$API_URL/x402/info" "" "x402_enabled"; then
    ((PASSED++))
else
    ((FAILED++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Authenticated Endpoints (Free Tier Demo Key)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test 4: Current Regime (Requires API Key)
if test_endpoint_json "Current Regime" "$API_URL/regime/current" "X-API-Key: $DEMO_KEY" "regime"; then
    ((PASSED++))
else
    ((FAILED++))
fi

# Test 5: Regime History (Should work with demo key)
if test_endpoint_json "Regime History" "$API_URL/regime/history?days=7" "X-API-Key: $DEMO_KEY" "regimes"; then
    ((PASSED++))
else
    ((FAILED++))
fi

# Test 6: Regime Transitions (Should work with demo key)
if test_endpoint_json "Regime Transitions" "$API_URL/regime/transitions?days=30" "X-API-Key: $DEMO_KEY" "transitions"; then
    ((PASSED++))
else
    ((FAILED++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Admin Endpoints (Admin Key Required)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test 7: Admin Stats (Requires Admin Key)
if test_endpoint_json "Admin Stats" "$API_URL/admin/stats" "X-Admin-Key: $ADMIN_KEY" "total_requests"; then
    ((PASSED++))
else
    ((FAILED++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Security Tests (Should Fail)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test 8: Regime endpoint without API key (should fail with 401)
echo -n "Testing No API Key (should fail)... "
response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/regime/current")
if [ "$response" = "401" ]; then
    echo -e "${GREEN}✅ PASS${NC} (correctly rejected)"
    ((PASSED++))
else
    echo -e "${RED}❌ FAIL${NC} (got HTTP $response, expected 401)"
    ((FAILED++))
fi

# Test 9: Invalid API key (should fail with 401)
echo -n "Testing Invalid API Key (should fail)... "
response=$(curl -s -o /dev/null -w "%{http_code}" -H "X-API-Key: invalid_key" "$API_URL/regime/current")
if [ "$response" = "401" ]; then
    echo -e "${GREEN}✅ PASS${NC} (correctly rejected)"
    ((PASSED++))
else
    echo -e "${RED}❌ FAIL${NC} (got HTTP $response, expected 401)"
    ((FAILED++))
fi

# ───────────────────────────────────────────────────────────────────
# SUMMARY
# ───────────────────────────────────────────────────────────────────

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  Test Results"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED!${NC}"
    echo ""
    echo "✅ API is fully operational and ready for production use."
    echo ""
    echo "Next steps:"
    echo "  1. Enable x402 micropayments (see x402_INTEGRATION_GUIDE.md)"
    echo "  2. Set up monitoring alerts (see MONITORING_SETUP.md)"
    echo "  3. Start marketing! Tweet the URL and get users."
    echo ""
    exit 0
else
    echo -e "${RED}⚠️  SOME TESTS FAILED${NC}"
    echo ""
    echo "Check the Render logs for details:"
    echo "  https://dashboard.render.com → regime-api → Logs"
    echo ""
    echo "Common issues:"
    echo "  - Free tier sleep: Wait 30 sec after first request"
    echo "  - Missing env vars: Check REGIME_DATA_PATH is set"
    echo "  - Data file missing: Ensure data/regime_data.csv is in repo"
    echo ""
    exit 1
fi
