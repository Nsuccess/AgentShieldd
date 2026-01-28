# AgentShield - Run All Kite AI Examples
# This script runs all 3 Kite AI examples sequentially

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "AgentShield - Kite AI Security Suite" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Running all 3 security examples..." -ForegroundColor Yellow
Write-Host "Total time: ~2 minutes`n" -ForegroundColor Yellow

Write-Host "`n🛡️ Example 1: Security Validation Suite`n" -ForegroundColor Cyan
python demos/security_validation_suite.py

Write-Host "`n`n⚡ Example 2: Protected Transaction Execution`n" -ForegroundColor Cyan
python demos/execute_protected_transaction.py

Write-Host "`n`n🤖 Example 3: Autonomous Payment Flow`n" -ForegroundColor Cyan
python demos/autonomous_payment_flow.py

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "All security examples completed!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Read-Host "Press Enter to exit"

