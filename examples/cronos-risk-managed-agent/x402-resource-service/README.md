# AgentShield x402 Resource Service

A simple x402-compatible API service that demonstrates how AgentShield protects AI agents accessing paid resources on Cronos.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
bun install
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Run Service

```bash
# Development mode (with auto-reload)
bun run dev

# Production mode
bun start
```

## 📡 API Endpoints

### GET `/health`
Health check endpoint

**Response:**
```json
{
  "ok": true,
  "service": "AgentShield x402 Resource Service",
  "network": "cronos-testnet",
  "timestamp": "2026-01-20T..."
}
```

### GET `/.well-known/agent-card`
Agent discovery endpoint (A2A protocol)

**Response:**
```json
{
  "name": "AgentShield Protected Data Service",
  "description": "AI-powered market data with AgentShield security validation",
  "resources": [...]
}
```

### GET `/api/protected-data`
Protected resource requiring x402 payment

**Without payment:**
```
Status: 402 Payment Required
{
  "message": "Payment required to access this resource",
  "accepts": [{
    "payTo": "0x...",
    "asset": "0x...",
    "maxAmountRequired": "1000000",
    "maxTimeoutSeconds": 300,
    "scheme": "eip3009",
    "extra": {
      "paymentId": "uuid"
    }
  }]
}
```

**With payment:**
```
Status: 200 OK
Headers: x-payment-id: <payment-id>
{
  "ok": true,
  "data": {
    "message": "Access granted!",
    "content": {...}
  }
}
```

### POST `/api/pay`
Settlement endpoint for x402 payments

**Request:**
```json
{
  "paymentId": "uuid",
  "paymentHeader": "base64-encoded-header",
  "paymentRequirements": {...}
}
```

**Response:**
```json
{
  "ok": true,
  "paymentId": "uuid",
  "transactionHash": "0x...",
  "message": "Payment verified and settled"
}
```

## 🔄 x402 Payment Flow

1. **Client requests resource** → GET `/api/protected-data`
2. **Server returns 402** with payment requirements
3. **Client generates payment header** using AgentShield SafeFacilitator
4. **Client settles payment** → POST `/api/pay`
5. **Client retries request** → GET `/api/protected-data` with `x-payment-id` header
6. **Server returns protected data** → 200 OK

## 🛡️ AgentShield Integration

This service works seamlessly with AgentShield's SafeFacilitator:

```python
from AgentShield.facilitators import SafeFacilitator

# Initialize with validation
facilitator = SafeFacilitator(
    policy_path="policy.yaml",
    private_key="0x...",
    network="cronos-testnet"
)

# Generate safe payment header (with 4-stage validation)
result = await facilitator.generate_safe_payment_header(
    pay_to="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    asset="0x9e0e7a0C8688b1A4e46b5F4D0A4F6B8F5C8E5D4C",
    amount="1000000",
    context={"purpose": "API access"}
)

if result["approved"]:
    # Use payment header to access resource
    payment_header = result["payment_header"]
```

## 🧪 Testing

```bash
# Test health endpoint
curl http://localhost:3000/health

# Test agent card
curl http://localhost:3000/.well-known/agent-card

# Test protected resource (should return 402)
curl http://localhost:3000/api/protected-data
```

## 📦 Built With

- **Bun** - Fast JavaScript runtime
- **Hono** - Lightweight web framework
- **@crypto.com/facilitator-client** - Cronos x402 SDK

## 🔗 Resources

- **Cronos x402 Docs**: https://docs.cronos.org/cronos-x402-facilitator/
- **Facilitator SDK**: https://www.npmjs.com/package/@crypto.com/facilitator-client
- **AgentShield**: See main repository README
