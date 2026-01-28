"""
Demo: Real Transaction Execution on Kite AI with AgentShield

This demo shows AgentShield validating and executing REAL transactions on Kite Chain.
It demonstrates the complete end-to-end flow with actual blockchain execution.
"""

import sys
import os
from pathlib import Path
from web3 import Web3

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentshield.facilitators.kite_facilitator import KiteFacilitator
from agentshield import PolicyEngine
from agentshield.policy_engine import PolicyConfig
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

console = Console()


def print_header():
    """Print demo header"""
    console.print("\n" + "=" * 70)
    console.print("[bold cyan]AgentShield: Real Transaction Execution on Kite AI[/bold cyan]")
    console.print("[dim]End-to-End Security + Blockchain Execution[/dim]")
    console.print("=" * 70 + "\n")


def demo_real_transaction():
    """Demo: Execute a real transaction with AgentShield validation"""
    
    print_header()
    
    console.print(Panel(
        "[bold]This demo will:[/bold]\n\n"
        "1. Connect to Kite AI testnet\n"
        "2. Check your wallet balance\n"
        "3. Create a real transaction (0.01 KITE transfer)\n"
        "4. Validate through AgentShield (4 stages)\n"
        "5. Execute on blockchain if approved\n"
        "6. Show transaction on explorer",
        title="🛡️  Real Transaction Demo",
        border_style="cyan"
    ))
    console.print()
    
    # Initialize Kite facilitator
    console.print("[cyan]→ Initializing Kite AI facilitator...[/cyan]")
    kite = KiteFacilitator()
    
    if not kite.is_connected():
        console.print("[red]❌ Failed to connect to Kite AI testnet[/red]\n")
        return
    
    console.print("[green]✓ Connected to Kite AI testnet[/green]\n")
    
    # Check wallet
    if not kite.address:
        console.print("[red]❌ No wallet configured in .env file[/red]\n")
        return
    
    balance = kite.get_balance()
    console.print(f"[cyan]Wallet:[/cyan] {kite.address}")
    console.print(f"[cyan]Balance:[/cyan] {balance:.4f} KITE\n")
    
    if balance < 0.02:
        console.print(Panel(
            "[yellow]⚠️  Low balance![/yellow]\n\n"
            f"Current: {balance:.4f} KITE\n"
            "Needed: 0.02 KITE (0.01 for transfer + gas)\n\n"
            "Get more tokens from: https://faucet.gokite.ai",
            title="Insufficient Balance",
            border_style="yellow"
        ))
        console.print()
        return
    
    # Create transaction
    console.print("[cyan]→ Creating transaction...[/cyan]")
    
    # Recipient address (properly checksummed for Kite AI)
    recipient = Web3.to_checksum_address("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0")
    amount_kite = 0.01
    amount_wei = kite.w3.to_wei(amount_kite, 'ether')
    
    transaction = {
        'to': recipient,
        'value': amount_wei,
        'data': '0x',
        'gas': 21000,
        'gasPrice': kite.w3.eth.gas_price,
        'nonce': kite.w3.eth.get_transaction_count(kite.address),
        'chainId': kite.CHAIN_ID
    }
    
    console.print(f"[dim]To: {recipient}[/dim]")
    console.print(f"[dim]Amount: {amount_kite} KITE[/dim]")
    console.print(f"[dim]Gas: 21000[/dim]\n")
    
    # Initialize policy engine
    console.print("[cyan]→ Initializing AgentShield...[/cyan]")
    
    policy_config = {
        "version": "2.0",
        "enabled": True,
        "policies": [
            {
                "type": "eth_value_limit",
                "max_value_wei": str(kite.w3.to_wei(1, 'ether')),
                "enabled": True,
                "description": "Limit transfers to 1 KITE"
            },
            {
                "type": "gas_limit",
                "max_gas": 500000,
                "enabled": True,
                "description": "Limit gas to 500k"
            }
        ],
        "simulation": {"enabled": False},
        "logging": {"level": "info"},
        "llm_validation": {"enabled": False}
    }
    
    config = PolicyConfig(policy_config)
    policy_engine = PolicyEngine(config_path=None)
    policy_engine.config = config
    policy_engine.chain_id = kite.CHAIN_ID
    
    console.print("[green]✓ AgentShield initialized[/green]\n")
    
    # Validate transaction
    console.print(Panel(
        "[bold cyan]Running 4-Stage Validation[/bold cyan]",
        border_style="cyan"
    ))
    console.print()
    
    passed, reason = policy_engine.validate_transaction(transaction, kite.address)
    
    console.print()
    
    # Check result
    if not passed:
        console.print(Panel(
            "[bold red]❌ TRANSACTION BLOCKED[/bold red]\n\n"
            f"Reason: {reason}\n\n"
            "[dim]Transaction blocked before signature. Funds are safe.[/dim]",
            title="Validation Failed",
            border_style="red"
        ))
        console.print()
        return
    
    # Transaction approved - ask for confirmation
    console.print(Panel(
        "[bold green]✅ TRANSACTION APPROVED[/bold green]\n\n"
        f"All security checks passed!\n\n"
        "[yellow]This will execute a REAL transaction on Kite Chain.[/yellow]",
        title="Validation Passed",
        border_style="green"
    ))
    console.print()
    
    confirm = input("Execute transaction? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        console.print("\n[yellow]Transaction cancelled by user[/yellow]\n")
        return
    
    # Execute transaction
    console.print("\n[cyan]→ Signing and broadcasting transaction...[/cyan]")
    
    try:
        # Sign transaction
        signed_tx = kite.w3.eth.account.sign_transaction(
            transaction,
            kite.private_key
        )
        
        # Send transaction
        tx_hash = kite.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash_hex = tx_hash.hex()
        
        console.print(f"[green]✓ Transaction sent![/green]")
        console.print(f"[dim]Hash: {tx_hash_hex}[/dim]\n")
        
        # Wait for confirmation
        console.print("[cyan]→ Waiting for confirmation...[/cyan]")
        
        receipt = kite.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        console.print("[green]✓ Transaction confirmed![/green]\n")
        
        # Show results
        table = Table(title="Transaction Details", show_header=False)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Status", "✅ Success" if receipt['status'] == 1 else "❌ Failed")
        table.add_row("Block Number", str(receipt['blockNumber']))
        table.add_row("Gas Used", str(receipt['gasUsed']))
        table.add_row("Transaction Hash", tx_hash_hex)
        table.add_row("Explorer", kite.get_transaction_url(tx_hash_hex))
        
        console.print(table)
        console.print()
        
        # Show new balance
        new_balance = kite.get_balance()
        console.print(f"[cyan]New Balance:[/cyan] {new_balance:.4f} KITE")
        console.print(f"[dim]Sent: {amount_kite} KITE + gas fees[/dim]\n")
        
        console.print(Panel(
            "[bold green]🎉 SUCCESS![/bold green]\n\n"
            "Transaction executed successfully on Kite AI Chain!\n\n"
            f"View on explorer:\n{kite.get_transaction_url(tx_hash_hex)}",
            title="Transaction Complete",
            border_style="green"
        ))
        console.print()
        
    except Exception as e:
        console.print(f"\n[red]❌ Transaction failed: {str(e)}[/red]\n")


def main():
    """Main function"""
    try:
        demo_real_transaction()
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]\n")
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]\n")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]\n")


if __name__ == "__main__":
    main()
