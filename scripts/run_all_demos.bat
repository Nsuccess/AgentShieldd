@echo off
REM AgentShield - Run All Kite AI Examples
REM This script runs all 3 Kite AI examples sequentially

echo.
echo ========================================
echo AgentShield - Kite AI Security Suite
echo ========================================
echo.
echo Running all 3 security examples...
echo Total time: ~2 minutes
echo.

echo.
echo ========================================
echo Example 1: Security Validation Suite
echo ========================================
python demos/security_validation_suite.py

echo.
echo ========================================
echo Example 2: Protected Transaction Execution
echo ========================================
python demos/execute_protected_transaction.py

echo.
echo ========================================
echo Example 3: Autonomous Payment Flow
echo ========================================
python demos/autonomous_payment_flow.py

echo.
echo ========================================
echo All security examples completed!
echo ========================================
echo.

pause

