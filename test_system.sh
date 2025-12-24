#!/bin/bash

# Multi-Account Admin Panel - System Test Script
# Tests all components to ensure system readiness

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  Multi-Account Admin Panel - System Test${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Function to print test result
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗${NC} $2"
        ((TESTS_FAILED++))
    fi
}

# Function to run command and capture result
run_test() {
    local test_name="$1"
    local test_command="$2"

    if eval "$test_command" > /dev/null 2>&1; then
        print_result 0 "$test_name"
        return 0
    else
        print_result 1 "$test_name"
        return 1
    fi
}

# =====================================
# 1. ENVIRONMENT CHECKS
# =====================================

echo -e "${YELLOW}[1/7] Environment Checks${NC}"
echo "-----------------------------------"

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    print_result 0 "Python 3 installed: $PYTHON_VERSION"
else
    print_result 1 "Python 3 not found"
fi

# Check PostgreSQL
if command -v psql &> /dev/null; then
    PSQL_VERSION=$(psql --version 2>&1 | head -n 1)
    print_result 0 "PostgreSQL installed: $PSQL_VERSION"
else
    print_result 1 "PostgreSQL not found"
fi

# Check FFmpeg
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n 1 | cut -d' ' -f3)
    print_result 0 "FFmpeg installed: $FFMPEG_VERSION"
else
    print_result 1 "FFmpeg not found (required for video processing)"
fi

# Check pip
run_test "pip installed" "python3 -m pip --version"

echo ""

# =====================================
# 2. PROJECT STRUCTURE
# =====================================

echo -e "${YELLOW}[2/7] Project Structure${NC}"
echo "-----------------------------------"

# Check directories
run_test "Backend directory exists" "[ -d backend ]"
run_test "Frontend directory exists" "[ -d frontend ]"
run_test "Backend app directory exists" "[ -d backend/app ]"
run_test "Frontend assets directory exists" "[ -d frontend/assets ]"

# Check key files
run_test "Backend main.py exists" "[ -f backend/app/main.py ]"
run_test "Backend requirements.txt exists" "[ -f backend/requirements.txt ]"
run_test "Frontend index.html exists" "[ -f frontend/index.html ]"
run_test "Frontend accounts.html exists" "[ -f frontend/accounts.html ]"
run_test "Frontend generator.html exists" "[ -f frontend/generator.html ]"
run_test ".env.example exists" "[ -f .env.example ]"
run_test ".gitignore exists" "[ -f .gitignore ]"

echo ""

# =====================================
# 3. BACKEND DEPENDENCIES
# =====================================

echo -e "${YELLOW}[3/7] Backend Dependencies${NC}"
echo "-----------------------------------"

# Check if virtual environment exists
if [ -d "backend/venv" ] || [ -d "backend/.venv" ]; then
    print_result 0 "Virtual environment found"

    # Activate virtual environment
    if [ -d "backend/venv" ]; then
        source backend/venv/bin/activate 2>/dev/null || true
    elif [ -d "backend/.venv" ]; then
        source backend/.venv/bin/activate 2>/dev/null || true
    fi
else
    print_result 1 "Virtual environment not found (run: python3 -m venv backend/venv)"
fi

# Check Python packages
cd backend 2>/dev/null || true

if python3 -c "import fastapi" 2>/dev/null; then
    FASTAPI_VERSION=$(python3 -c "import fastapi; print(fastapi.__version__)" 2>/dev/null)
    print_result 0 "FastAPI installed: $FASTAPI_VERSION"
else
    print_result 1 "FastAPI not installed"
fi

run_test "SQLAlchemy installed" "python3 -c 'import sqlalchemy'"
run_test "Pydantic installed" "python3 -c 'import pydantic'"
run_test "Uvicorn installed" "python3 -c 'import uvicorn'"
run_test "psycopg2 installed" "python3 -c 'import psycopg2'"
run_test "ffmpeg-python installed" "python3 -c 'import ffmpeg'"

cd .. 2>/dev/null || true

echo ""

# =====================================
# 4. DATABASE CONNECTION
# =====================================

echo -e "${YELLOW}[4/7] Database Connection${NC}"
echo "-----------------------------------"

# Check if database exists
if psql -lqt 2>/dev/null | cut -d \| -f 1 | grep -qw admin_panel; then
    print_result 0 "Database 'admin_panel' exists"

    # Test connection
    if psql -U admin -d admin_panel -c "SELECT 1;" > /dev/null 2>&1; then
        print_result 0 "Database connection successful"
    else
        print_result 1 "Cannot connect to database (check credentials)"
    fi
else
    print_result 1 "Database 'admin_panel' not found"
fi

# Check database tables
if psql -U admin -d admin_panel -c "\dt" 2>/dev/null | grep -q "accounts\|proxies\|videos"; then
    print_result 0 "Database tables initialized"
else
    print_result 1 "Database tables not initialized (run: python backend/init_db.py)"
fi

echo ""

# =====================================
# 5. BACKEND API
# =====================================

echo -e "${YELLOW}[5/7] Backend API${NC}"
echo "-----------------------------------"

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    print_result 0 "Backend server running on port 8000"

    # Test health endpoint
    HEALTH_STATUS=$(curl -s http://localhost:8000/health | grep -o '"status":"healthy"' || echo "")
    if [ ! -z "$HEALTH_STATUS" ]; then
        print_result 0 "Health check endpoint working"
    else
        print_result 1 "Health check endpoint returned unexpected response"
    fi

    # Test API endpoints
    run_test "Root endpoint accessible" "curl -s http://localhost:8000/ > /dev/null"
    run_test "Accounts API accessible" "curl -s http://localhost:8000/api/accounts > /dev/null"
    run_test "Proxies API accessible" "curl -s http://localhost:8000/api/proxies > /dev/null"
    run_test "Analytics API accessible" "curl -s http://localhost:8000/api/analytics/dashboard > /dev/null"
    run_test "API docs accessible" "curl -s http://localhost:8000/docs > /dev/null"

else
    print_result 1 "Backend server not running (start: uvicorn app.main:app --reload)"
    echo -e "${RED}   Skipping API endpoint tests${NC}"
fi

echo ""

# =====================================
# 6. FRONTEND
# =====================================

echo -e "${YELLOW}[6/7] Frontend${NC}"
echo "-----------------------------------"

# Check if frontend is running
if curl -s http://localhost:8080/ > /dev/null 2>&1; then
    print_result 0 "Frontend server running on port 8080"

    run_test "Dashboard page accessible" "curl -s http://localhost:8080/index.html > /dev/null"
    run_test "Accounts page accessible" "curl -s http://localhost:8080/accounts.html > /dev/null"
    run_test "Generator page accessible" "curl -s http://localhost:8080/generator.html > /dev/null"
else
    print_result 1 "Frontend server not running (start: python3 -m http.server 8080)"
    echo -e "${RED}   Skipping frontend page tests${NC}"
fi

# Check static assets
run_test "Main CSS exists" "[ -f frontend/assets/css/main.css ]"
run_test "Dashboard JS exists" "[ -f frontend/assets/js/dashboard.js ]"
run_test "API client exists" "[ -f frontend/assets/js/api.js ]"

echo ""

# =====================================
# 7. SECURITY & CONFIGURATION
# =====================================

echo -e "${YELLOW}[7/7] Security & Configuration${NC}"
echo "-----------------------------------"

# Check .env file
if [ -f "backend/.env" ]; then
    print_result 0 ".env file exists"

    # Check for default secret key
    if grep -q "your-secret-key-change-in-production" backend/.env 2>/dev/null; then
        print_result 1 "WARNING: Using default SECRET_KEY (change in production!)"
    else
        print_result 0 "SECRET_KEY has been customized"
    fi
else
    print_result 1 ".env file not found (copy from .env.example)"
fi

# Check .gitignore
if [ -f ".gitignore" ]; then
    print_result 0 ".gitignore exists"

    # Check if .env is ignored
    if grep -q "\.env" .gitignore; then
        print_result 0 ".env is in .gitignore"
    else
        print_result 1 ".env should be added to .gitignore"
    fi
else
    print_result 1 ".gitignore not found"
fi

# Check uploads directory
if [ -d "backend/uploads" ] || [ -d "uploads" ]; then
    print_result 0 "Uploads directory exists"
else
    print_result 1 "Uploads directory not found (will be created automatically)"
fi

echo ""

# =====================================
# SUMMARY
# =====================================

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  Test Summary${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
SUCCESS_RATE=$((TESTS_PASSED * 100 / TOTAL_TESTS))

echo -e "Total Tests: ${TOTAL_TESTS}"
echo -e "${GREEN}Passed: ${TESTS_PASSED}${NC}"
echo -e "${RED}Failed: ${TESTS_FAILED}${NC}"
echo -e "Success Rate: ${SUCCESS_RATE}%"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed! System is ready.${NC}"
    exit 0
elif [ $SUCCESS_RATE -ge 80 ]; then
    echo -e "${YELLOW}⚠ Most tests passed. Review failures above.${NC}"
    exit 0
else
    echo -e "${RED}✗ Multiple tests failed. System needs attention.${NC}"
    exit 1
fi
