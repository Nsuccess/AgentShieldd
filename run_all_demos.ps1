Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AgentShield - Running All 4 Demos" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/4] Demo 1: Real Transaction Execution" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
python execute_real_transaction.py
Write-Host ""
Write-Host "Press any key to continue to Demo 2..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Write-Host ""

Write-Host "[2/4] Demo 2: Crypto.com AI Agent SDK" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
python crypto_com_sdk_demo.py
Write-Host ""
Write-Host "Press any key to continue to Demo 3..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Write-Host ""

Write-Host "[3/4] Demo 3: Policy-Based Blocking" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
python policy_blocking.py
Write-Host ""
Write-Host "Press any key to continue to Demo 4..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Write-Host ""

Write-Host "[4/4] Demo 4: Honeypot Detection" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
python honeypot_detection.py
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "All 4 Demos Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Bonus: Run AI-powered threat detection with Groq LLM?" -ForegroundColor Cyan
Write-Host "Press any key to run, or Ctrl+C to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Write-Host ""

python suspicious_detection.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "All Demos Finished! Ready for Hackathon!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
