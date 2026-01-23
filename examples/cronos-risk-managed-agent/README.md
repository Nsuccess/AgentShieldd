# Cronos Risk-Managed AI Agent

**AgentShield: The Safety Layer for AI Agents on Cronos**

This example demonstrates how AgentShield protects AI agents from malicious transactions using a 4-stage validation pipeline with honeypot detection.

## 🎯 What This Demo Shows

1. **SafeAgent** - Crypto.com AI Agent wrapped with AgentShield protection
2. **SafeFacilitator** - x402 payments with validation
3. **4-Stage Validation** - LLM Judge → Policy → Simulation → LLM Analysis
4. **Stage 3.5 Honeypot Detection** - Simulates BUY → SELL to detect scams

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# From repository root
pip install -r requirements-hackathon.txt
```

### 2. Configure Environment

```bash
cd examples/cronos-risk-managed-agent
cp .env.example .env

# Edit .env and add your keys:
# - CRYPTO_COM_API_KEY (from https://developers.crypto.com/)
# - PRIVATE_KEY (your wallet private key)
# - GROQ_API_KEY (already provided, or get from https://console.groq.com/)
```

### 3. Get Testnet Tokens

```bash
# Get TCRO from faucet
# Visit: https://cronos.org/faucet

# Get USDC.e from faucet
# Visit: https://faucet.cronos.org
```

### 4. Run Demo

```bash
python safe_agent_demo.py
```

## 📋 Demo Scenarios

### Test 1: Safe USDC Transfer ✅
```
Input: "Send 10 USDC to 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
Expected: APPROVED
Reason: Normal transfer within policy limits
```

### Test 2: Honeypot Token ❌
```
Input: "Buy 100 SCAM tokens"
Expected: BLOCKED
Reason: Stage 3.5 detects honeypot (sell simulation fails)
```

### Test 3: Excessive Amount ❌
```
Input: "Send 1000000 USDC"
Expected: BLOCKED
Reason: Exceeds policy max_transfer_amount
```

## 🏗️ Architecture

```
User Input
    ↓
SafeAgent (Crypto.com AI Agent SDK)
    ↓
AgentShield 4-Stage Validation:
    ├─ Stage 1: LLM Intent Judge (Groq)
    ├─ Stage 2: Policy Validation
    ├─ Stage 3: Tenderly Simulation
    │   └─ Stage 3.5: Honeypot Detection
    └─ Stage 4: LLM Analysis
    ↓
✅ Approved → Execute
❌ Blocked → Protect User
```

## 📁 Project Structure

```
cronos-risk-managed-agent/
├── safe_agent_demo.py          # Main demo script
├── config/
│   └── policy.yaml             # AgentShield policy configuration
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## 🔧 Configuration

### Policy Configuration (`config/policy.yaml`)

```yaml
# Stage 1: LLM Intent Judge
llm_judge:
  enabled: true
  provider: "groq"  # 10x faster than OpenAI!
  model: "llama-3.3-70b-versatile"

# Stage 2: Policy Rules
rules:
  max_transfer_amount:
    USDC: "100000000"  # 100 USDC
  whitelist:
    - "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"

# Stage 3: Simulation + Honeypot Detection
simulation:
  enabled: true
  honeypot_detection:
    enabled: true
    method: "buy_sell_simulation"
    min_sell_ratio: 0.9

# Stage 4: LLM Analysis
llm_analysis:
  enabled: true
  provider: "groq"
```

### Environment Variables (`.env`)

```bash
# Required
CRYPTO_COM_API_KEY=your-api-key
PRIVATE_KEY=0xyour-private-key
GROQ_API_KEY=gsk_...

# Optional
TENDERLY_API_KEY=your-tenderly-key
DEBUG=true
NETWORK=cronos-testnet
```

## 🎬 Expected Output

```
============================================================
DEMO 1: SafeAgent - AI Agent with AgentShield Protection
============================================================

✅ SafeAgent initialized successfully!

┌─ Test 1: Safe USDC Transfer ─────────────────────────────┐
│ Input: Send 10 USDC to 0x742d35Cc6634C0532925a3b844Bc... │
│ Expected: approved                                        │
└───────────────────────────────────────────────────────────┘

✅ APPROVED
Response: Transaction validated and approved

Validation Stages:
┌────────────────────┬────────┬──────────────────────────┐
│ Stage              │ Status │ Details                  │
├────────────────────┼────────┼──────────────────────────┤
│ LLM Intent Judge   │ ✅ Pass│ Safe transaction intent  │
│ Policy Validation  │ ✅ Pass│ Within policy limits     │
│ Tenderly Simulation│ ✅ Pass│ Simulation successful    │
│ LLM Analysis       │ ✅ Pass│ No suspicious activity   │
└────────────────────┴────────┴──────────────────────────┘

┌─ Test 2: Honeypot Token Purchase ────────────────────────┐
│ Input: Buy 100 SCAM tokens                               │
│ Expected: blocked                                        │
└───────────────────────────────────────────────────────────┘

❌ BLOCKED
Reason: Honeypot token detected (Stage 3.5)
Failed Stage: Simulation

Validation Stages:
┌────────────────────┬────────┬──────────────────────────┐
│ Stage              │ Status │ Details                  │
├────────────────────┼────────┼──────────────────────────┤
│ LLM Intent Judge   │ ✅ Pass│ Intent validated         │
│ Policy Validation  │ ✅ Pass│ No policy violations     │
│ Honeypot Detection │ ❌ Fail│ Sell simulation failed   │
└────────────────────┴────────┴──────────────────────────┘

✅ Demo Complete!

AgentShield successfully protected AI agents from:
• Honeypot tokens (Stage 3.5 detection)
• Excessive transfers (Policy validation)
• Malicious transactions (4-stage pipeline)

Ready for Cronos x402 Hackathon submission! 🚀
```

## 🔗 Resources

- **Cronos Testnet Faucet**: https://cronos.org/faucet
- **USDC.e Faucet**: https://faucet.cronos.org
- **Crypto.com AI Agent SDK**: https://ai-agent-sdk-docs.crypto.com/
- **Cronos x402 Docs**: https://docs.cronos.org/cronos-x402-facilitator/
- **AgentShield Docs**: See `../../HACKATHON_GUIDE.md`

## 🎯 Hackathon Submission

This demo is part of the **Cronos x402 Paytech Hackathon** submission:

- **Track 2**: Agentic Finance ($5,000)
- **Track 4**: Dev Tooling ($3,000)
- **Positioning**: "The Safety Layer for AI Agents on Cronos"

## 📝 License

MIT License - See repository root for details
