# PowerShell start script for Windows

Write-Host "🚀 Starting AgentShield API..." -ForegroundColor Cyan
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Start server
Write-Host ""
Write-Host "✅ Starting server on http://localhost:8000" -ForegroundColor Green
Write-Host "📚 API docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

python main.py
