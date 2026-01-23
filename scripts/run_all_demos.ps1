# AgentShield - Run All Demos
# This script runs all 4 demos sequentially

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "AgentShield - Demo Runner" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Running all 4 demos..." -ForegroundColor Yellow
Write-Host "Total time: ~2.5 minutes`n" -ForegroundColor Yellow

Write-Host "`n🎬 Demo 1: Real Transaction Execution`n" -ForegroundColor Cyan
python demos/execute_real_transaction.py

Write-Host "`n`n🎬 Demo 2: Crypto.com SDK Integration`n" -ForegroundColor Cyan
python demos/crypto_com_sdk_demo.py

Write-Host "`n`n🎬 Demo 3: Policy-Based Blocking`n" -ForegroundColor Cyan
python demos/policy_blocking.py

Write-Host "`n`n🎬 Demo 4: Honeypot Detection`n" -ForegroundColor Cyan
python demos/honeypot_detection.py

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "All demos completed!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Read-Host "Press Enter to exit"
