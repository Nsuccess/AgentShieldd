@echo off
echo ========================================
echo AgentShield - Running All 4 Demos
echo ========================================
echo.

echo [1/4] Demo 1: Real Transaction Execution
echo ========================================
python execute_real_transaction.py
echo.
echo Press any key to continue to Demo 2...
pause > nul
echo.

echo [2/4] Demo 2: Crypto.com AI Agent SDK
echo ========================================
python crypto_com_sdk_demo.py
echo.
echo Press any key to continue to Demo 3...
pause > nul
echo.

echo [3/4] Demo 3: Policy-Based Blocking
echo ========================================
python policy_blocking.py
echo.
echo Press any key to continue to Demo 4...
pause > nul
echo.

echo [4/4] Demo 4: Honeypot Detection
echo ========================================
python honeypot_detection.py
echo.

echo ========================================
echo All 4 Demos Complete!
echo ========================================
echo.
echo Bonus: Run AI-powered threat detection with Groq LLM?
echo Press any key to run, or Ctrl+C to exit...
pause > nul
echo.

python suspicious_detection.py

echo.
echo ========================================
echo All Demos Finished! Ready for Hackathon!
echo ========================================
pause
