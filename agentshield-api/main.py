"""
AgentShield API Service
Provides token validation endpoints for Just Pay integration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import sys

# Add parent directory to path to import agentshield
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(
    title="AgentShield API",
    description="Token validation and fraud detection for crypto payments",
    version="1.0.0"
)

# Enable CORS for Just Pay frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenValidationRequest(BaseModel):
    token_address: str
    chain: str
    amount: Optional[str] = "1.0"

class ValidationResponse(BaseModel):
    is_safe: bool
    risk_level: str  # LOW, MEDIUM, HIGH, UNKNOWN
    reason: str
    details: Dict[str, Any]
    can_buy: Optional[bool] = None
    can_sell: Optional[bool] = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "AgentShield API",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "agentshield-api",
        "endpoints": {
            "validate_token": "/validate-token",
            "health": "/health"
        }
    }

@app.post("/validate-token", response_model=ValidationResponse)
async def validate_token(req: TokenValidationRequest):
    """
    Validate if a token is safe to use for payment.
    
    Checks:
    1. Honeypot detection (buy/sell simulation)
    2. Contract verification
    3. Liquidity checks
    
    Returns:
    - is_safe: Whether the token passed validation
    - risk_level: LOW, MEDIUM, HIGH, or UNKNOWN
    - reason: Human-readable explanation
    - details: Full validation results
    """
    try:
        # Import here to avoid issues if agentshield not installed
        from agentshield.simulator import simulate_swap
        from web3 import Web3
        
        # Normalize chain name
        chain_map = {
            "ethereum": "ethereum",
            "eth": "ethereum",
            "base": "base",
            "cronos": "cronos",
            "cronos-testnet": "cronos-testnet",
            "arbitrum": "arbitrum",
            "arb": "arbitrum",
            "polygon": "polygon",
            "matic": "polygon",
        }
        
        normalized_chain = chain_map.get(req.chain.lower(), req.chain.lower())
        
        # Get RPC URL for chain
        rpc_urls = {
            "ethereum": os.getenv("ETHEREUM_RPC", "https://eth.llamarpc.com"),
            "base": os.getenv("BASE_RPC", "https://mainnet.base.org"),
            "cronos": os.getenv("CRONOS_RPC", "https://evm.cronos.org"),
            "cronos-testnet": os.getenv("CRONOS_TESTNET_RPC", "https://evm-t3.cronos.org"),
            "arbitrum": os.getenv("ARBITRUM_RPC", "https://arb1.arbitrum.io/rpc"),
            "polygon": os.getenv("POLYGON_RPC", "https://polygon-rpc.com"),
        }
        
        rpc_url = rpc_urls.get(normalized_chain)
        if not rpc_url:
            return ValidationResponse(
                is_safe=True,
                risk_level="UNKNOWN",
                reason=f"Chain {req.chain} not supported for validation",
                details={"chain": req.chain, "supported": False}
            )
        
        # Validate token address format
        if not Web3.is_address(req.token_address):
            return ValidationResponse(
                is_safe=False,
                risk_level="HIGH",
                reason="Invalid token address format",
                details={"token_address": req.token_address, "valid": False}
            )
        
        # Run honeypot detection
        print(f"[AgentShield] Validating token {req.token_address} on {normalized_chain}")
        
        result = simulate_swap(
            token_address=req.token_address,
            rpc_url=rpc_url,
            amount=req.amount
        )
        
        print(f"[AgentShield] Validation result: {result}")
        
        # Analyze results
        can_buy = result.get("can_buy", True)
        can_sell = result.get("can_sell", True)
        
        if not can_sell:
            return ValidationResponse(
                is_safe=False,
                risk_level="HIGH",
                reason="Token cannot be sold (honeypot detected)",
                details=result,
                can_buy=can_buy,
                can_sell=can_sell
            )
        
        if not can_buy:
            return ValidationResponse(
                is_safe=False,
                risk_level="HIGH",
                reason="Token cannot be bought",
                details=result,
                can_buy=can_buy,
                can_sell=can_sell
            )
        
        # Check for warnings
        if result.get("liquidity_warning"):
            return ValidationResponse(
                is_safe=True,
                risk_level="MEDIUM",
                reason="Low liquidity detected - proceed with caution",
                details=result,
                can_buy=can_buy,
                can_sell=can_sell
            )
        
        if result.get("high_slippage"):
            return ValidationResponse(
                is_safe=True,
                risk_level="MEDIUM",
                reason="High slippage detected - large price impact",
                details=result,
                can_buy=can_buy,
                can_sell=can_sell
            )
        
        # All checks passed
        return ValidationResponse(
            is_safe=True,
            risk_level="LOW",
            reason="Token passed all safety checks",
            details=result,
            can_buy=can_buy,
            can_sell=can_sell
        )
        
    except ImportError as e:
        print(f"[AgentShield] Import error: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"AgentShield module not available: {str(e)}"
        )
    except Exception as e:
        print(f"[AgentShield] Validation error: {e}")
        # Fail open - don't block if validation fails
        return ValidationResponse(
            is_safe=True,
            risk_level="UNKNOWN",
            reason=f"Validation error: {str(e)}",
            details={"error": str(e), "type": type(e).__name__}
        )

@app.post("/x402/generate-header")
async def generate_x402_header(request: dict):
    """
    Generate x402 payment header using Cronos Facilitator
    
    Request body:
        private_key: Wallet private key
        pay_to: Recipient address
        asset: Token contract address
        amount: Amount in base units (string)
        network: Network name (cronos-testnet or cronos-mainnet)
        timeout_seconds: Validity window (default: 300)
    
    Returns:
        payment_header: Base64-encoded payment header
        decoded: Decoded payment header for verification
        network: Network used
    """
    try:
        from agentshield.facilitators import CronosFacilitator
        
        private_key = request.get("private_key")
        pay_to = request.get("pay_to")
        asset = request.get("asset")
        amount = request.get("amount")
        network = request.get("network", "cronos-testnet")
        timeout_seconds = request.get("timeout_seconds", 300)
        
        if not all([private_key, pay_to, asset, amount]):
            raise HTTPException(
                status_code=400,
                detail="Missing required fields: private_key, pay_to, asset, amount"
            )
        
        # Initialize facilitator
        facilitator = CronosFacilitator(network=network)
        
        # Generate payment header
        payment_header = facilitator.generate_payment_header(
            private_key=private_key,
            pay_to=pay_to,
            asset=asset,
            amount=amount,
            timeout_seconds=timeout_seconds
        )
        
        # Decode for verification
        decoded = facilitator.decode_payment_header(payment_header)
        
        return {
            "payment_header": payment_header,
            "decoded": decoded,
            "network": network,
            "protocol": "eip3009"
        }
        
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="Cronos Facilitator not available. Install required dependencies."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
