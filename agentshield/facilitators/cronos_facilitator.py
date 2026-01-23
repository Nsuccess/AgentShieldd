"""
Cronos x402 Facilitator - Python Implementation
Generates EIP-3009 payment headers for x402 protocol

This module provides Python implementation of the Cronos Facilitator SDK
for generating signed payment headers compatible with the x402 protocol.
"""

import os
import time
import base64
import json
from typing import Optional
from eth_account import Account
from eth_account.messages import encode_typed_data


class CronosFacilitator:
    """
    Generate x402 payment headers for Cronos using EIP-3009
    
    This class implements the buyer-side x402 payment flow by generating
    cryptographically signed payment headers that authorize token transfers
    without requiring gas fees from the user.
    """
    
    # Token configurations for Cronos networks
    TOKENS = {
        "cronos-testnet": {
            "USDC.e": {
                "address": "0xc01efAaF7C5C61bEbFAeb358E1161b537b8bC0e0",  # devUSDC.e from faucet
                "name": "Bridged USDC (Stargate)",
                "version": "1",
            }
        },
        "cronos-mainnet": {
            "USDC.e": {
                "address": "0xc21223249CA28397B4B6541dfFaEcC539BfF0141",
                "name": "Bridged USDC (Stargate)",
                "version": "1",
            }
        }
    }
    
    def __init__(self, network: str = "cronos-testnet"):
        """
        Initialize Cronos Facilitator
        
        Args:
            network: Network name ("cronos-testnet" or "cronos-mainnet")
        """
        self.network = network
        self.chain_id = "338" if network == "cronos-testnet" else "25"
    
    def generate_nonce(self) -> str:
        """
        Generate a random 32-byte nonce for EIP-3009 authorization
        
        Returns:
            Hex string with 0x prefix
        """
        return "0x" + os.urandom(32).hex()
    
    def generate_payment_header(
        self,
        private_key: str,
        pay_to: str,
        asset: str,
        amount: str,
        timeout_seconds: int = 300,
        token_name: Optional[str] = None,
        token_version: Optional[str] = None,
    ) -> str:
        """
        Generate EIP-3009 payment header for x402 payments
        
        This method creates a signed authorization that allows the facilitator
        to transfer tokens on behalf of the user without requiring gas fees.
        
        Args:
            private_key: Wallet private key (with or without 0x prefix)
            pay_to: Recipient address
            asset: Token contract address
            amount: Amount in base units (string, e.g., "1000000" for 1 USDC)
            timeout_seconds: Validity window in seconds (default: 300)
            token_name: EIP-712 domain name (optional, auto-detected)
            token_version: EIP-712 domain version (optional, auto-detected)
        
        Returns:
            Base64-encoded payment header string
        
        Example:
            >>> facilitator = CronosFacilitator("cronos-testnet")
            >>> header = facilitator.generate_payment_header(
            ...     private_key="0x...",
            ...     pay_to="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            ...     asset="0x9e0e7a0C8688b1A4e46b5F4D0A4F6B8F5C8E5D4C",
            ...     amount="1000000"
            ... )
        """
        # Ensure private key has 0x prefix
        if not private_key.startswith("0x"):
            private_key = "0x" + private_key
        
        # Create account from private key
        account = Account.from_key(private_key)
        
        # Normalize addresses for EIP-712 encoding
        # First convert to lowercase to remove invalid checksums, then apply correct checksum
        from web3 import Web3
        
        from_address = Web3.to_checksum_address(account.address.lower())
        to_address = Web3.to_checksum_address(pay_to.lower())
        asset_address = Web3.to_checksum_address(asset.lower())
        
        # Generate unique nonce
        nonce = self.generate_nonce()
        
        # Calculate validity window
        valid_after = 0  # Valid immediately
        valid_before = int(time.time()) + timeout_seconds
        
        # Auto-detect token name and version if not provided
        if token_name is None or token_version is None:
            token_config = self._get_token_config(asset)
            if token_config:
                token_name = token_name or token_config["name"]
                token_version = token_version or token_config["version"]
            else:
                # Fallback defaults
                token_name = token_name or "Bridged USDC (Stargate)"
                token_version = token_version or "1"
        
        # EIP-712 domain
        domain = {
            "name": token_name,
            "version": token_version,
            "chainId": int(self.chain_id),
            "verifyingContract": asset_address,
        }
        
        # EIP-712 types for TransferWithAuthorization
        types = {
            "TransferWithAuthorization": [
                {"name": "from", "type": "address"},
                {"name": "to", "type": "address"},
                {"name": "value", "type": "uint256"},
                {"name": "validAfter", "type": "uint256"},
                {"name": "validBefore", "type": "uint256"},
                {"name": "nonce", "type": "bytes32"},
            ]
        }
        
        # Message to sign
        message = {
            "from": from_address,
            "to": to_address,
            "value": int(amount),
            "validAfter": valid_after,
            "validBefore": valid_before,
            "nonce": nonce,
        }
        
        # Sign with EIP-712
        typed_data = encode_typed_data(
            domain_data=domain,
            message_types=types,
            message_data=message
        )
        signed_message = account.sign_message(typed_data)
        signature = signed_message.signature.hex()
        
        # Ensure signature has 0x prefix
        if not signature.startswith("0x"):
            signature = "0x" + signature
        
        # Construct payment header
        payment_header = {
            "x402Version": 1,
            "scheme": "eip3009",
            "network": self.network,
            "payload": {
                "from": from_address,
                "to": to_address,
                "value": amount,
                "validAfter": valid_after,
                "validBefore": valid_before,
                "nonce": nonce,
                "signature": signature,
                "asset": asset_address,
            },
        }
        
        # Base64 encode
        header_json = json.dumps(payment_header)
        header_b64 = base64.b64encode(header_json.encode()).decode()
        
        return header_b64
    
    def _get_token_config(self, asset: str) -> Optional[dict]:
        """
        Get token configuration by address
        
        Args:
            asset: Token contract address
        
        Returns:
            Token config dict or None if not found
        """
        if self.network not in self.TOKENS:
            return None
        
        for token_name, config in self.TOKENS[self.network].items():
            if config["address"].lower() == asset.lower():
                return config
        
        return None
    
    def decode_payment_header(self, header_b64: str) -> dict:
        """
        Decode a base64-encoded payment header
        
        Args:
            header_b64: Base64-encoded payment header
        
        Returns:
            Decoded payment header dict
        """
        header_json = base64.b64decode(header_b64).decode()
        return json.loads(header_json)


# Convenience function for quick usage
def generate_payment_header(
    private_key: str,
    pay_to: str,
    asset: str,
    amount: str,
    network: str = "cronos-testnet",
    timeout_seconds: int = 300,
) -> str:
    """
    Quick function to generate payment header
    
    Args:
        private_key: Wallet private key
        pay_to: Recipient address
        asset: Token contract address
        amount: Amount in base units (string)
        network: Network name (default: "cronos-testnet")
        timeout_seconds: Validity window (default: 300)
    
    Returns:
        Base64-encoded payment header
    """
    facilitator = CronosFacilitator(network=network)
    return facilitator.generate_payment_header(
        private_key=private_key,
        pay_to=pay_to,
        asset=asset,
        amount=amount,
        timeout_seconds=timeout_seconds,
    )
