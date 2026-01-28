# 🛡️ AgentShield

**Production-Ready Security Layer for Autonomous Agent Payments on Kite AI Chain**

[![Demo Video](https://img.shields.io/badge/Demo-Video-red?style=for-the-badge&logo=youtube)](https://youtu.be/J03qnUu6dDM)
[![Kite AI](https://img.shields.io/badge/Kite_AI-Testnet-green?style=for-the-badge)](https://testnet.gokite.ai/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)

---

## 🎯 Overview

AgentShield is a security validation system for autonomous agent payments on Kite AI Chain. It validates every transaction through a 4-stage pipeline and blocks malicious transactions **before signature**, ensuring funds are always safe.

### Key Features

- ✅ **4-Stage Validation Pipeline** - Intent Judge → Policy Validation → Pre-Execution → Risk Analysis
- ✅ **Policy Enforcement** - Spending limits, address denylists, gas limits
- ✅ **Real-Time Simulation** - Test transactions before execution
- ✅ **Attack Prevention** - Blocks prompt injection, excessive amounts, malicious addresses
- ✅ **Autonomous Payments** - Secure agent-to-agent transactions
- ✅ **Drop-in Integration** - 3 lines of code to add security

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Nsuccess/AgentShield.git
cd AgentShield

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your Kite AI wallet credentials to .env
```

### Run Security Validation

```bash
# Run complete security validation suite
python demos/security_validation_suite.py

# Or run all examples
.\scripts\run_all_demos.ps1  # Windows PowerShell
```

---

## 🎬 Demo Video

Watch AgentShield in action: **[Demo Video](https://youtu.be/J03qnUu6dDM)**

The demo shows:
- ✅ Real transaction execution on Kite AI testnet
- ✅ Blocking excessive amount (100 KITE)
- ✅ Blocking null address (burn prevention)
- ✅ Blocking prompt injection attack
- ✅ Autonomous agent-to-agent payment

---

## 🛡️ How It Works

### 4-Stage Validation Pipeline

```
AI Agent Request
      ↓
┌─────────────────────┐
│ Stage 1: Intent     │ ← Parse transaction intent
│ Judge               │
└─────────────────────┘
      ↓
┌─────────────────────┐
│ Stage 2: Policy     │ ← Check spending limits, address lists
│ Validation          │
└─────────────────────┘
      ↓
┌─────────────────────┐
│ Stage 3: Pre-       │ ← Simulate transaction
│ Execution           │
└─────────────────────┘
      ↓
┌─────────────────────┐
│ Stage 4: Risk       │ ← AI-powered threat detection
│ Analysis            │
└─────────────────────┘
      ↓
   APPROVED ✅ or BLOCKED 🚫
      ↓
  Sign & Execute (if approved)
```

### Security Features

**Policy Enforcement:**
- Spending limits per transaction
- Address allowlists/denylists
- Gas limit controls
- Rate limiting

**Attack Prevention:**
- Prompt injection detection
- Null address blocking
- Excessive amount blocking
- Malicious contract detection

---

## 📊 Proven Results

### Real Transactions on Kite AI Testnet

**Security Validation Suite:**
- TX: `0xcaf35dbbb2d326896dd85df08c6831ec06d13b915ca949b48b5a252e7560e911`
- Block: 19584019
- Status: ✅ CONFIRMED

**Protected Transaction:**
- TX: `0x2d9e7652879753aea1ee328cbdc633e039813c2951cbdd3076dc5e71d1b776d4`
- Block: 19563670
- Status: ✅ CONFIRMED

**Autonomous Payment:**
- TX: `0x3ce2d540805b50b3d0185147bec0e0a82f395395f3120f48d417cda5ebfd5371`
- Status: ✅ CONFIRMED

### Attacks Blocked

- 🚫 Excessive amount (100 KITE) - BLOCKED
- 🚫 Null address (0.1 KITE) - BLOCKED
- 🚫 Prompt injection - BLOCKED

**Total Protected:** 100.1+ KITE

---

## 💻 Usage Examples

### Example 1: Security Validation Suite

```bash
python demos/security_validation_suite.py
```

Shows all 4 security scenarios:
1. Real transaction execution
2. Excessive amount blocking
3. Null address blocking
4. Prompt injection detection

### Example 2: Protected Transaction

```bash
python demos/execute_protected_transaction.py
```

Demonstrates complete transaction flow with 4-stage validation.

### Example 3: Autonomous Payment

```bash
python demos/autonomous_payment_flow.py
```

Shows agent-to-agent payment with built-in security.

---

## 🔧 Integration

### 3-Line Integration

```python
from agentshield import PolicyEngine
from agentshield.facilitators import KiteFacilitator

# 1. Create facilitator
kite = KiteFacilitator(private_key, wallet_address)

# 2. Wrap with AgentShield
policy = PolicyEngine(config_path="policy.yaml")

# 3. Validate before executing
result = policy.validate(transaction)
if result.approved:
    kite.execute_transaction(transaction)
```

### Policy Configuration

```yaml
# policy.yaml
eth_value_limit: 1.0  # Max 1 KITE per transaction
gas_limit: 500000
address_denylist:
  - "0x0000000000000000000000000000000000000000"
```

---

## 🌐 Kite AI Integration

### Network Details

- **Network:** Kite AI Testnet
- **Chain ID:** 2368
- **RPC:** https://rpc-testnet.gokite.ai/
- **Explorer:** https://testnet.gokite.ai/
- **Faucet:** https://faucet.gokite.ai/

### Why Kite AI?

Kite AI is a Layer-1 blockchain built for autonomous agent payments. AgentShield provides the security layer that makes these payments safe.

---

## 📁 Project Structure

```
AgentShield/
├── agentshield/              # Core security engine
│   ├── policy_engine.py      # 4-stage validation
│   ├── wallet_wrapper.py     # Transaction wrapper
│   ├── facilitators/         # Blockchain connectors
│   │   └── kite_facilitator.py
│   └── rules/                # Policy validators
├── demos/                    # Example scripts
│   ├── security_validation_suite.py
│   ├── execute_protected_transaction.py
│   └── autonomous_payment_flow.py
├── scripts/                  # Automation scripts
│   └── run_all_demos.ps1
├── tests/                    # Test suite
├── README.md                 # This file
└── policy.yaml              # Security policy config
```

---

## 🎯 Use Cases

### 1. Autonomous Agent Payments
Secure payments between AI agents without human intervention.

### 2. DeFi Agent Protection
Protect DeFi trading agents from malicious transactions.

### 3. Agent Marketplaces
Enable safe agent-to-agent commerce with built-in security.

### 4. Subscription Services
Automated subscription payments with spending controls.

---

## 🔒 Security

### What AgentShield Protects Against

- ✅ Prompt injection attacks
- ✅ Excessive amount transfers
- ✅ Null address (burn) transactions
- ✅ Malicious contract interactions
- ✅ Unauthorized recipients
- ✅ Gas limit exploits

### How It Works

**All validation happens BEFORE signature.** If any check fails, the transaction is blocked and never reaches the blockchain. This ensures:
- No irreversible losses
- No wasted gas fees
- Complete fund safety

---

## 📚 Documentation

- **Quick Start:** [QUICK_START.md](QUICK_START.md)
- **Integration Guide:** [KITE_AI_INTEGRATION.md](KITE_AI_INTEGRATION.md)
- **Getting Started:** [START_HERE.md](START_HERE.md)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 🏆 SPARK AI Hackathon

**Track:** Kite AI - Payment Track  
**Demo Video:** https://youtu.be/J03qnUu6dDM

AgentShield demonstrates production-ready security for autonomous agent payments on Kite AI Chain, with real transactions and proven attack prevention.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Demo Video:** https://youtu.be/J03qnUu6dDM
- **Kite AI Docs:** https://docs.gokite.ai/
- **Kite AI Explorer:** https://testnet.gokite.ai/
- **GitHub:** https://github.com/Nsuccess/AgentShield

---

## 👤 Author

**Success Nwachukwu**
- GitHub: [@Nsuccess](https://github.com/Nsuccess)
- Email: successnwachukwu368@gmail.com
- Telegram: @Rijkaardio

---

## 🙏 Acknowledgments

- Kite AI team for the amazing payment infrastructure
- SPARK AI Hackathon organizers
- The Web3 security community

---

**AgentShield - Prove it's safe before it's signed. 🛡️**

*Production-ready security for autonomous agent payments on Kite AI Chain*
