# AgentShield API Service

FastAPI service that provides token validation endpoints for Loofta Pay integration.

## Features

- **Honeypot Detection**: Simulates buy/sell to detect tokens that can't be sold
- **Liquidity Checks**: Validates sufficient liquidity for swaps
- **Contract Verification**: Checks token contract safety
- **Multi-chain Support**: Ethereum, Base, Cronos, Arbitrum, Polygon

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

Server runs on `http://localhost:8000`

### Docker

```bash
# Build from project root
docker build -f agentshield-api/Dockerfile -t agentshield-api .

# Run
docker run -p 8000:8000 agentshield-api
```

### Deploy to Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

### Deploy to Render

1. Push to GitHub
2. Go to [render.com](https://render.com)
3. New Web Service → Connect repo
4. Build Command: `pip install -r requirements-hackathon.txt && pip install -r agentshield-api/requirements.txt`
5. Start Command: `cd agentshield-api && uvicorn main:app --host 0.0.0.0 --port $PORT`

## API Endpoints

### `GET /`
Health check

### `GET /health`
Detailed health status

### `POST /validate-token`
Validate a token for safety

**Request:**
```json
{
  "token_address": "0x...",
  "chain": "ethereum",
  "amount": "1.0"
}
```

**Response:**
```json
{
  "is_safe": true,
  "risk_level": "LOW",
  "reason": "Token passed all safety checks",
  "details": { ... },
  "can_buy": true,
  "can_sell": true
}
```

**Risk Levels:**
- `LOW`: Token is safe to use
- `MEDIUM`: Proceed with caution (low liquidity, high slippage)
- `HIGH`: Token is unsafe (honeypot, can't sell)
- `UNKNOWN`: Validation failed or chain not supported

## Environment Variables

See `.env.example` for configuration options.

## Integration with Loofta Pay

Loofta Pay calls this API to validate tokens before allowing payments:

```typescript
const response = await fetch('https://agentshield-api.railway.app/validate-token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    token_address: '0x...',
    chain: 'ethereum',
    amount: '1.0'
  })
});

const { is_safe, risk_level, reason } = await response.json();

if (risk_level === 'HIGH') {
  // Block payment
}
```

## Testing

```bash
# Test honeypot detection (Cronos testnet)
curl -X POST http://localhost:8000/validate-token \
  -H "Content-Type: application/json" \
  -d '{
    "token_address": "0x6001B76e8CeA99a749F591ed6E1cE7a704CF231b",
    "chain": "cronos-testnet",
    "amount": "1.0"
  }'

# Expected: risk_level = "HIGH", reason = "Token cannot be sold"
```

## License

MIT
