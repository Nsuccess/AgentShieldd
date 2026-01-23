@echo off
REM AgentShield - Run All Demos
REM This script runs all 4 demos sequentially

echo.
echo ========================================
echo AgentShield - Demo Runner
echo ========================================
echo.
echo Running all 4 demos...
echo Total time: ~2.5 minutes
echo.

echo.
echo ========================================
echo Demo 1: Real Transaction Execution
echo ========================================
python demos/execute_real_transaction.py

echo.
echo ========================================
echo Demo 2: Crypto.com SDK Integration
echo ========================================
python demos/crypto_com_sdk_demo.py

echo.
echo ========================================
echo Demo 3: Policy-Based Blocking
echo ========================================
python demos/policy_blocking.py

echo.
echo ========================================
echo Demo 4: Honeypot Detection
echo ========================================
python demos/honeypot_detection.py

echo.
echo ========================================
echo All demos completed!
echo ========================================
echo.

pause
