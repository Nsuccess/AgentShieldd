"""
AgentShield Facilitator Wrappers
Adds 4-stage validation to x402 payment flows
"""

from typing import Optional, Dict, Any
from AgentShield.policy_engine import PolicyEngine
from AgentShield.facilitators.cronos_facilitator import CronosFacilitator, generate_payment_header


class SafeFacilitator:
    """
    x402 Facilitator with AgentShield validation
    
    Wraps CronosFacilitator with 4-stage security:
    1. LLM Intent Judge - Validates transaction intent
    2. Policy Validation - Checks against policy rules
    3. Tenderly Simulation - Simulates transaction on fork
    4. LLM Analysis - Analyzes simulation results
    
    Plus Stage 3.5: Honeypot Detection
    - Simulates BUY → SELL to detect scam tokens
    """
    
    def __init__(
        self,
        policy_path: str,
        private_key: str,
        network: str = "cronos-testnet",
        enable_llm_judge: bool = True,
        enable_simulation: bool = True,
    ):
        """
        Initialize SafeFacilitator
        
        Args:
            policy_path: Path to policy.yaml file
            private_key: Wallet private key for signing
            network: Cronos network ("cronos-testnet" or "cronos-mainnet")
            enable_llm_judge: Enable Stage 1 & 4 LLM validation
            enable_simulation: Enable Stage 3 Tenderly simulation
        """
        self.policy_engine = PolicyEngine(policy_path)
        self.facilitator = CronosFacilitator(network=network)
        self.private_key = private_key
        self.network = network
        self.enable_llm_judge = enable_llm_judge
        self.enable_simulation = enable_simulation
    
    async def generate_safe_payment_header(
        self,
        pay_to: str,
        asset: str,
        amount: str,
        context: Optional[Dict[str, Any]] = None,
        timeout_seconds: int = 300,
    ) -> Dict[str, Any]:
        """
        Generate payment header with 4-stage validation
        
        This method validates the payment through AgentShield's security pipeline
        before generating the signed payment header.
        
        Args:
            pay_to: Recipient address
            asset: Token contract address
            amount: Amount in base units (string)
            context: Additional context for validation (user intent, etc.)
            timeout_seconds: Payment validity window
        
        Returns:
            {
                "approved": bool,
                "payment_header": str (if approved),
                "reason": str (if rejected),
                "validation": dict (validation details),
                "stages": dict (results from each stage)
            }
        
        Example:
            >>> facilitator = SafeFacilitator(
            ...     policy_path="policy.yaml",
            ...     private_key="0x..."
            ... )
            >>> result = await facilitator.generate_safe_payment_header(
            ...     pay_to="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            ...     asset="0x9e0e7a0C8688b1A4e46b5F4D0A4F6B8F5C8E5D4C",
            ...     amount="1000000",
            ...     context={"user_intent": "Pay for API access"}
            ... )
            >>> if result["approved"]:
            ...     print(f"Payment header: {result['payment_header']}")
            ... else:
            ...     print(f"Blocked: {result['reason']}")
        """
        # Prepare context
        if context is None:
            context = {}
        
        context.update({
            "payment_type": "x402",
            "recipient": pay_to,
            "token": asset,
            "amount": amount,
            "network": self.network,
        })
        
        # Stage 1-4: Validate payment through AgentShield pipeline
        # Note: For token transfers, we use data="0x" (no calldata)
        validation_result = await self.policy_engine.validate_transaction(
            to=pay_to,
            value=amount,
            data="0x",
            context=context,
        )
        
        # Check if validation passed
        if not validation_result.get("approved", False):
            return {
                "approved": False,
                "reason": validation_result.get("reason", "Validation failed"),
                "validation": validation_result,
                "stages": validation_result.get("stages", {}),
            }
        
        # Validation passed - generate payment header
        try:
            payment_header = self.facilitator.generate_payment_header(
                private_key=self.private_key,
                pay_to=pay_to,
                asset=asset,
                amount=amount,
                timeout_seconds=timeout_seconds,
            )
            
            return {
                "approved": True,
                "payment_header": payment_header,
                "validation": validation_result,
                "stages": validation_result.get("stages", {}),
                "metadata": {
                    "from": self.facilitator._get_account_address(self.private_key),
                    "to": pay_to,
                    "asset": asset,
                    "amount": amount,
                    "network": self.network,
                    "valid_for_seconds": timeout_seconds,
                }
            }
        
        except Exception as e:
            return {
                "approved": False,
                "reason": f"Failed to generate payment header: {str(e)}",
                "validation": validation_result,
                "stages": validation_result.get("stages", {}),
                "error": str(e),
            }
    
    def generate_unsafe_payment_header(
        self,
        pay_to: str,
        asset: str,
        amount: str,
        timeout_seconds: int = 300,
    ) -> str:
        """
        Generate payment header WITHOUT validation (use with caution!)
        
        This bypasses all AgentShield security checks. Only use this if you've
        already validated the payment through another mechanism.
        
        Args:
            pay_to: Recipient address
            asset: Token contract address
            amount: Amount in base units (string)
            timeout_seconds: Payment validity window
        
        Returns:
            Base64-encoded payment header
        """
        return self.facilitator.generate_payment_header(
            private_key=self.private_key,
            pay_to=pay_to,
            asset=asset,
            amount=amount,
            timeout_seconds=timeout_seconds,
        )


# Export main classes and functions
__all__ = [
    "CronosFacilitator",
    "SafeFacilitator",
    "generate_payment_header",
]
