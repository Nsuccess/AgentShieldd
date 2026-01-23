# 🛡️ AgentShield - Security Layer for AI Agents on Cronos

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Cronos](https://img.shields.io/badge/Cronos-x402-blue.svg)](https://cronos.org)

**AgentShield makes every transaction prove it's safe before it's signed.**

Multi-stage security validation for AI agents: Policy enforcement → Transaction simulation → Honeypot detection → LLM threat analysis.

---

## 🎯 The Problem

AI agents can move funds at machine speed, but they're vulnerable:
- 🎣 Exploited through prompt manipulation
- 💣 Malicious contracts (honeypots, phishing)
- 🤖 Misinterpret intent or hallucinate actions
- 💸 Losses are immediate and irreversible

**Without AgentShield:** Bad approvals and honeypot trades broadcast immediately and become irreversible.

**With AgentShield:** Simulate first, inspect real effects, then enforce a hard block before signature.

---

## 🚀 Quick Start

### Run the Demos (3 minutes)

```bash
# Run all 4 demos automatically
.\run_all_demos.ps1

# Or run manually
python execute_real_transaction.py    # Demo 1: Real TCRO transfer (30s)
python crypto_com_sdk_demo.py          # Demo 2: Crypto.com SDK (45s)
python policy_blocking.py              # Demo 3: Policy enforcement (45s)
python honeypot_detection.py           # Demo 4: Honeypot detection (30s)
```

### Installation

```bash
# Install from source
git clone https://github.com/your-org/agentshield.git
cd agentshield
pip install -e .

# Install dependencies
pip install web3 python-dotenv rich groq crypto-com-ai-agent-client
```

### Integration (3 Lines of Code)

```python
from agentshield import PolicyWalletProvider, PolicyEngine
from coinbase_agentkit import AgentKit, CdpEvmWalletProvider

# Create base wallet
base_wallet = CdpEvmWalletProvider(config)

# Wrap with AgentShield (add security layer)
policy_engine = PolicyEngine(
    config_path="policy.yaml",
    web3_provider=base_wallet,
    chain_id=338  # Cronos testnet
)
policy_wallet = PolicyWalletProvider(base_wallet, policy_engine)

# Use with AgentKit - no other changes needed!
agentkit = AgentKit(wallet_provider=policy_wallet, action_providers=[...])
```

That's it! All transactions now go through multi-stage security validation.

---

## 🛡️ Security Pipeline

AgentShield validates every transaction through 4 stages:

### Stage 1: Intent Judge
- Parse transaction calldata
- Identify function calls and parameters
- Detect token transfers and approvals

### Stage 2: Policy Validation
- ETH value limits
- Address allowlist/denylist
- Per-asset spending limits
- Gas limits
- Function allowlists

### Stage 3: Transaction Simulation
- Tenderly simulation with full execution traces
- Asset/balance change tracking
- Gas estimation
- Revert detection

### Stage 3.5: Honeypot Detection 🆕
- Simulate token BUY transaction
- Automatically test SELL transaction
- Block if tokens cannot be sold back
- **Zero manual blacklisting needed**

### Stage 4: LLM Security Analysis 
- AI-powered malicious pattern detection
- Hidden approval detection
- Unusual fund flow analysis
- Risk scoring and recommendations

---

## 🎬 Live Demos

### Demo 1: Real Transaction Execution
Shows AgentShield validating and executing a real TCRO transfer on Cronos testnet.

**Key Features:**
- 4-stage validation pipeline
- Real blockchain transaction
- Verifiable on Cronos explorer
- Transaction hash and block number

### Demo 2: Crypto.com AI Agent SDK Integration
Shows natural language commands converted to blockchain transactions with security.

**Key Features:**
- Natural language: "Send 0.01 TCRO to address"
- SDK interprets intent
- AgentShield validates
- Real execution with explorer link
- **Track 3: Crypto.com Ecosystem Integration**

### Demo 3: Policy-Based Blocking
Shows AgentShield blocking 3 malicious transaction attempts.

**Scenarios:**
1. Excessive transfer (100 TCRO > 1 TCRO limit) - **BLOCKED**
2. Denied address (null address scam) - **BLOCKED**
3. Rate limit exceeded (4th transaction) - **BLOCKED**

**Result:** 100.6 TCRO protected, blocked before signature

### Demo 4: Honeypot Detection
Shows AgentShield detecting and blocking a real honeypot token on Base Sepolia.

**How it works:**
1. Agent intends to buy tokens
2. AgentShield simulates BUY
3. Detects token receipt
4. Automatically tests SELL
5. Sell fails → **HONEYPOT DETECTED**
6. Transaction blocked before signature

**Contract:** `0xFe836592564C37D6cE99657c379a387CC5CE0868` (Base Sepolia)

---

## 💡 What Makes This Special

### 1. Novel Innovation: Stage 3.5 Honeypot Detection
- **Unique feature** not found in other security tools
- Automatically simulates BUY then SELL
- Catches scam tokens before user loses funds
- Zero manual blacklisting needed

### 2. Multi-Chain Security
- Cronos testnet (Chain ID: 338)
- Base Sepolia (Chain ID: 84532)
- Extensible to any EVM chain

### 3. Real Blockchain Transactions
- Not simulations or mocks
- Verifiable on blockchain explorers
- Real TCRO transfers
- Real honeypot detection

### 4. AI-Powered Analysis
- Real Groq LLM integration
- Model: `llama-3.1-8b-instant`
- 560 tokens/sec, FREE tier
- Detects patterns static rules miss

### 5. Drop-in Integration
- 3 lines of code
- Zero agent modifications
- Wrap existing wallet provider
- Load policy YAML and run

---

## 📋 Policy Configuration

Create a `policy.yaml` file:

```yaml
version: "2.0"
apply_to: [all]

# Logging
logging:
  level: info  # minimal, info, debug

# Policy rules
policies:
  # Limit ETH transfers
  - type: eth_value_limit
    max_value_wei: "1000000000000000000"  # 1 ETH
    enabled: true
    description: "Limit ETH transfers to 1 ETH per transaction"

  # Block malicious addresses
  - type: address_denylist
    denied_addresses:
      - "0x0000000000000000000000000000000000000000"
    enabled: true
    description: "Block transactions to denied addresses"

  # Per-asset spending limits
  - type: per_asset_limit
    asset_limits:
      - name: USDC
        address: "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
        max_amount: "10000000"  # 10 USDC
        decimals: 6
    enabled: true
    description: "Per-asset spending limits"

  # Gas limit
  - type: gas_limit
    max_gas: 500000
    enabled: true
    description: "Limit gas to 500k per transaction"

# Transaction simulation (enables honeypot detection)
simulation:
  enabled: true
  fail_on_revert: true
  estimate_gas: true

# LLM-based validation (optional)
llm_validation:
  enabled: false
  provider: "groq"
  model: "llama-3.1-8b-instant"
  api_key: "${GROQ_API_KEY}"
  block_threshold: 0.70
  warn_threshold: 0.40
```

---

## 🎯 Use Cases

- 🤖 **AI Trading Bots** - Prevent unauthorized trades and limit exposure
- 💼 **Portfolio Managers** - Enforce spending limits across assets
- 🏦 **Treasury Management** - Multi-signature with policy enforcement
- 🎮 **GameFi Agents** - Limit in-game asset transfers
- 🔐 **Security Testing** - Validate smart contract interactions
- 🛡️ **Honeypot Protection** - Automatically detect and block scam tokens

---

## 🏗️ Project Structure

```
agentshield/
├── agentshield/                 # Main package
│   ├── __init__.py
│   ├── __main__.py             # CLI entry point
│   ├── policy_engine.py        # Multi-stage validation pipeline
│   ├── wallet_wrapper.py       # Wallet provider wrapper
│   ├── calldata_parser.py      # ABI decoding
│   ├── simulator.py            # Transaction simulation
│   ├── logger.py               # Logging system
│   ├── llm_judge.py            # LLM-based security analysis
│   ├── facilitators/           # Blockchain facilitators
│   ├── integrations/           # SDK integrations
│   ├── simulators/             # Simulation providers
│   │   └── tenderly.py         # Tenderly integration
│   └── rules/                  # Policy validators
│       └── validators.py
├── agentshield-api/            # REST API server
├── examples/                   # Usage examples
│   ├── autonomous-portfolio-agent/
│   ├── cronos-risk-managed-agent/
│   └── onchain-agent/
├── tests/                      # Test suite
├── execute_real_transaction.py # Demo 1
├── crypto_com_sdk_demo.py      # Demo 2
├── policy_blocking.py          # Demo 3
├── honeypot_detection.py       # Demo 4
├── suspicious_detection.py     # Demo 5
├── run_all_demos.ps1           # Run all demos (PowerShell)
├── run_all_demos.bat           # Run all demos (CMD)
├── README.md                   # This file
├── START_HERE.md               # Quick start guide
├└── pyproject.toml              # Package configuration
```

---

## 📚 Documentation

### Quick Start
- **START_HERE.md** - Entry point, quick start guide
- **QUICK_START.md** - One-page quick reference

### Technical
- **README.md** - This file, complete documentation
- **CHANGELOG.md** - Version history
- **CONTRIBUTING.md** - Contributing guidelines

### Examples
- **examples/cronos-risk-managed-agent/** - Cronos x402 integration
- **examples/autonomous-portfolio-agent/** - Autonomous agent
- **examples/onchain-agent/** - Chatbot integration

---

## 🔧 Environment Variables

```bash
# Wallet (required for real transactions)
PRIVATE_KEY=your_private_key
WALLET_ADDRESS=your_wallet_address

# Groq LLM (for AI threat detection)
GROQ_API_KEY=your_groq_api_key

# Tenderly (optional - for advanced simulation)
TENDERLY_ACCESS_KEY=your_tenderly_key
TENDERLY_ACCOUNT_SLUG=your_account
TENDERLY_PROJECT_SLUG=your_project
```

---

## 🎯 Hackathon Tracks

### Track 2: Agentic Finance ($5,000)
**AgentShield enables risk-managed autonomous agents**
- Policy-based spending limits
- Multi-stage validation
- Honeypot detection
- Real-time threat analysis

### Track 3: Crypto.com Integration ($3,000)
**Natural language interface with security**
- Crypto.com AI Agent SDK integration
- Natural language → Blockchain execution
- AgentShield security layer
- Demo: `crypto_com_sdk_demo.py`

### Track 4: Dev Tooling ($3,000)
**Reusable security SDK for any AI agent**
- 3-line integration
- Zero agent modifications
- Multi-chain support
- Production-ready

**Total Potential: $11,000+ across 3 tracks**

---

## 🔒 Security Best Practices

1. **Start with restrictive policies** - Use low limits and gradually increase
2. **Enable simulation** - Catch failures before sending transactions
3. **Enable honeypot detection** - Protect against scam tokens automatically
4. **Use Tenderly** - Get detailed execution traces and asset changes
5. **Enable LLM validation** - Add AI-powered threat detection
6. **Test on testnet** - Validate policies before mainnet
7. **Monitor logs** - Review transaction validations regularly
8. **Keep denylists updated** - Add known malicious addresses

---

## 🤝 Compatibility

AgentShield works with all Coinbase AgentKit wallet providers:

- ✅ **CDP EVM Wallet Provider**
- ✅ **CDP Smart Wallet Provider**
- ✅ **Ethereum Account Wallet Provider**

Same 3-line integration pattern for all wallet types!

---

## 🧪 Testing

Run the test suite:

```bash
cd tests
python test_complete_system.py
```

**Tests cover:**
- ETH value limits
- Address denylist/allowlist
- Per-asset limits
- Gas limits
- Calldata parsing
- All logging levels

---

## 🌐 Networks Supported

### Testnets
- **Cronos Testnet** (Chain ID: 338)
  - RPC: https://evm-t3.cronos.org/
  - Explorer: https://explorer.cronos.org/testnet
  
- **Base Sepolia** (Chain ID: 84532)
  - RPC: https://sepolia.base.org
  - Explorer: https://sepolia.basescan.org

### Mainnets
- Extensible to any EVM-compatible chain

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 🆘 Support

- **Issues:** [GitHub Issues](https://github.com/your-org/agentshield/issues)
- **Examples:** [examples/](examples/)
- **Documentation:** [README.md](README.md)

---

## 🎬 Demo Video

Watch AgentShield in action: [Demo Video Link]

---

## 🔗 Links

- **Cronos x402:** https://cronos.org
- **Crypto.com AI Agent SDK:** https://crypto.com
- **Groq LLM:** https://groq.com
- **Tenderly:** https://tenderly.co

---

## 🏆 Built for Cronos x402 Hackathon 2026

**AgentShield - The Safety Layer for AI Agents on Cronos**

**Prove it's safe before it's signed.** 🛡️

---

**Key Message:** AgentShield blocks risky transactions **before signature**, so your agents can move fast without taking irreversible risk.

**Integration:** Drop-in security layer. Wrap your wallet, load policy YAML, run unchanged.

**Innovation:** Stage 3.5 Honeypot Detection - automatically simulates BUY then SELL to catch scam tokens.

**Free and open source.** Get started now! 🚀
