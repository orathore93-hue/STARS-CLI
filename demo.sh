#!/bin/bash
# TARS CLI Demo Script for Screenshots/Recording

echo "🎬 TARS CLI Demo - Recording Script"
echo "===================================="
echo ""

# Colors for better visibility
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

demo_command() {
    echo -e "${CYAN}$ $1${NC}"
    sleep 1
    eval $1
    sleep 2
    echo ""
}

echo "📸 Demo 1: On-Call Dashboard"
echo "----------------------------"
demo_command "tars oncall"

echo ""
echo "📸 Demo 2: Health Check"
echo "----------------------"
demo_command "tars health"

echo ""
echo "📸 Demo 3: Triage Issues"
echo "-----------------------"
demo_command "tars triage"

echo ""
echo "📸 Demo 4: Live Pod Monitoring (5 seconds)"
echo "------------------------------------------"
echo -e "${CYAN}$ tars watch${NC}"
timeout 5 tars watch || true
echo ""

echo ""
echo "📸 Demo 5: Top Resource Consumers"
echo "---------------------------------"
demo_command "tars top"

echo ""
echo "📸 Demo 6: Cluster Metrics"
echo "-------------------------"
demo_command "tars metrics"

echo ""
echo "✅ Demo Complete!"
echo ""
echo "Screenshots saved? Now create:"
echo "1. Animated GIF from recording"
echo "2. Individual screenshots for README"
echo "3. Short video demo (30-60 seconds)"
