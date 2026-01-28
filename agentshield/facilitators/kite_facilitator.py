"""
Kite AI Chain Facilitator

Provides blockchain interaction utilities for Kite AI Chain (testnet)
"""

from web3 import Web3
from typing import Optional, Dict, Any
import os


class KiteFacilitator:
    """
    Facilitator for Kite AI Chain
    
    Kite AI is a Layer-1 blockchain built for autonomous agent payments.
    This facilitator provides utilities for interacting with Kite Chain.
    """
    
    # Kite AI Testnet Configuration
    CHAIN_ID = 2368
    CHAIN_NAME = "KiteAI Testnet"
    RPC_URL = "https://rpc-testnet.gokite.ai/"
    EXPLORER_URL = "https://testnet.kitescan.ai/"
    FAUCET_URL = "https://faucet.gokite.ai"
    NATIVE_TOKEN = "KITE"
    
    def __init__(self, rpc_url: Optional[str] = None, private_key: Optional[str] = None):
        """
        Initialize Kite facilitator
        
        Args:
            rpc_url: Custom RPC URL (defaults to testnet)
            private_key: Private key for signing transactions
        """
        self.rpc_url = rpc_url or os.getenv("KITE_RPC_URL", self.RPC_URL)
        self.private_key = private_key or os.getenv("KITE_PRIVATE_KEY")
        
        # Initialize Web3
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        
        # Set up account if private key provided
        if self.private_key:
            self.account = self.w3.eth.account.from_key(self.private_key)
            self.address = self.account.address
        else:
            self.account = None
            self.address = os.getenv("KITE_WALLET_ADDRESS")
    
    def is_connected(self) -> bool:
        """Check if connected to Kite Chain"""
        try:
            return self.w3.is_connected()
        except Exception:
            return False
    
    def get_balance(self, address: Optional[str] = None) -> float:
        """
        Get KITE balance for address
        
        Args:
            address: Address to check (defaults to facilitator address)
            
        Returns:
            Balance in KITE
        """
        addr = address or self.address
        if not addr:
            raise ValueError("No address provided")
        
        balance_wei = self.w3.eth.get_balance(addr)
        return float(self.w3.from_wei(balance_wei, 'ether'))
    
    def get_transaction_url(self, tx_hash: str) -> str:
        """
        Get block explorer URL for transaction
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            Explorer URL
        """
        if not tx_hash.startswith('0x'):
            tx_hash = f'0x{tx_hash}'
        return f"{self.EXPLORER_URL}tx/{tx_hash}"
    
    def get_address_url(self, address: str) -> str:
        """
        Get block explorer URL for address
        
        Args:
            address: Wallet address
            
        Returns:
            Explorer URL
        """
        return f"{self.EXPLORER_URL}address/{address}"
    
    def send_transaction(self, transaction: Dict[str, Any]) -> str:
        """
        Send transaction to Kite Chain
        
        Args:
            transaction: Transaction dict with to, value, data, etc.
            
        Returns:
            Transaction hash
        """
        if not self.account:
            raise ValueError("No private key configured")
        
        # Build transaction
        tx = {
            'from': self.address,
            'to': transaction.get('to'),
            'value': transaction.get('value', 0),
            'data': transaction.get('data', '0x'),
            'gas': transaction.get('gas', 100000),
            'gasPrice': self.w3.eth.gas_price,
            'nonce': self.w3.eth.get_transaction_count(self.address),
            'chainId': self.CHAIN_ID
        }
        
        # Sign transaction
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        
        # Send transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        return tx_hash.hex()
    
    def wait_for_transaction(self, tx_hash: str, timeout: int = 120) -> Dict[str, Any]:
        """
        Wait for transaction confirmation
        
        Args:
            tx_hash: Transaction hash
            timeout: Timeout in seconds
            
        Returns:
            Transaction receipt
        """
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
        return dict(receipt)
    
    def get_chain_info(self) -> Dict[str, Any]:
        """
        Get Kite Chain information
        
        Returns:
            Chain info dict
        """
        return {
            'chain_id': self.CHAIN_ID,
            'chain_name': self.CHAIN_NAME,
            'rpc_url': self.rpc_url,
            'explorer_url': self.EXPLORER_URL,
            'faucet_url': self.FAUCET_URL,
            'native_token': self.NATIVE_TOKEN,
            'connected': self.is_connected(),
            'block_number': self.w3.eth.block_number if self.is_connected() else None
        }
    
    def estimate_gas(self, transaction: Dict[str, Any]) -> int:
        """
        Estimate gas for transaction
        
        Args:
            transaction: Transaction dict
            
        Returns:
            Estimated gas
        """
        return self.w3.eth.estimate_gas(transaction)
    
    @classmethod
    def get_faucet_info(cls) -> str:
        """Get faucet information"""
        return f"""
Kite AI Testnet Faucet
======================
URL: {cls.FAUCET_URL}

Get free KITE tokens for testing on Kite AI testnet.
"""


# Convenience function
def create_kite_facilitator(private_key: Optional[str] = None) -> KiteFacilitator:
    """
    Create a Kite facilitator instance
    
    Args:
        private_key: Optional private key
        
    Returns:
        KiteFacilitator instance
    """
    return KiteFacilitator(private_key=private_key)


if __name__ == "__main__":
    # Test connection
    facilitator = KiteFacilitator()
    info = facilitator.get_chain_info()
    
    print("Kite AI Chain Information:")
    print("=" * 50)
    for key, value in info.items():
        print(f"{key}: {value}")
    
    if facilitator.address:
        print(f"\nWallet Address: {facilitator.address}")
        print(f"Balance: {facilitator.get_balance()} KITE")
        print(f"Explorer: {facilitator.get_address_url(facilitator.address)}")
    
    print(f"\n{KiteFacilitator.get_faucet_info()}")
