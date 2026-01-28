"""
Demo: AgentShield on Kite AI Chain

This demo shows AgentShield validating transactions on Kite AI testnet.
Demonstrates the 4-stage security pipeline protecting autonomous agent payments.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentshield.facilitators.kite_facilitator import KiteFacilitator
from agentshield import PolicyEngine, PolicyWalletProvider
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

console = Console()


def print_header():
    """Print demo header"""
    console.print("\n" + "=" * 70)
    console.print("[bold cyan]AgentShield on Kite AI Chain[/bold cyan]")
    console.print("[dim]Security Layer for Autonomous Agent Payments[/dim]")
    console.print("=" * 70 + "\n")


def print_kite_info(facilitator: KiteFacilitator):
    """Print Kite Chain information"""
    info = facilitator.get_chain_info()
    
    table = Table(title="Kite AI Testnet Information", show_header=False)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Chain Name", info['chain_name'])
    table.add_row("Chain ID", str(info['chain_id']))
    table.add_row("RPC URL", info['rpc_url'])
    table.add_row("Explorer", info['explorer_url'])
    table.add_row("Faucet", info['faucet_url'])
    table.add_row("Native Token", info['native_token'])
    table.add_row("Connected", "✅ Yes" if info['connected'] else "❌ No")
    
    if info['block_number']:
        table.add_row("Block Number", str(info['block_number']))
    
    console.print(table)
    console.print()


def print_wallet_info(facilitator: KiteFacilitator):
    """Print wallet information"""
    if not facilitator.address:
        console.print("[yellow]⚠️  No wallet configured[/yellow]\n")
        return
    
    balance = facilitator.get_balance()
    
    table = Table(title="Wallet Information", show_header=False)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Address", facilitator.address)
    table.add_row("Balance", f"{balance:.4f} KITE")
    table.add_row("Explorer", facilitator.get_address_url(facilitator.address))
    
    console.print(table)
    console.print()
    
    if balance < 0.01:
        console.print(Panel(
            f"[yellow]⚠️  Low balance! Get free KITE tokens from:\n{facilitator.FAUCET_URL}[/yellow]",
            title="Faucet Info",
            border_style="yellow"
        ))
        console.print()


def demo_transaction_validation():
    """Demo: Transaction validation on Kite Chain"""
    console.print(Panel(
        "[bold]Demo: Transaction Validation on Kite AI[/bold]\n\n"
        "This demo shows AgentShield's 4-stage validation pipeline:\n"
        "1. Intent Judge - Parse transaction intent\n"
        "2. Policy Validation - Check against rules\n"
        "3. Pre-Execution - Simulate transaction\n"
        "4. Risk Analysis - LLM threat detection",
        title="🛡️  AgentShield Demo",
        border_style="cyan"
    ))
    console.print()
    
    # Initialize Kite facilitator
    console.print("[cyan]→ Initializing Kite AI facilitator...[/cyan]")
    facilitator = KiteFacilitator()
    
    if not facilitator.is_connected():
        console.print("[red]❌ Failed to connect to Kite AI testnet[/red]")
        console.print(f"[dim]RPC URL: {facilitator.rpc_url}[/dim]\n")
        return
    
    console.print("[green]✓ Connected to Kite AI testnet[/green]\n")
    
    # Print chain info
    print_kite_info(facilitator)
    
    # Print wallet info
    print_wallet_info(facilitator)
    
    # Check if wallet is configured
    if not facilitator.address:
        console.print(Panel(
            "[yellow]⚠️  No wallet configured![/yellow]\n\n"
            "To run this demo with a real wallet:\n"
            "1. Get a private key from MetaMask or create new wallet\n"
            "2. Add to .env file: KITE_PRIVATE_KEY=your_key_here\n"
            "3. Get testnet KITE from faucet\n"
            "4. Run demo again",
            title="Setup Required",
            border_style="yellow"
        ))
        console.print()
        return
    
    # Create sample transaction
    console.print("[cyan]→ Creating sample transaction...[/cyan]")
    
    # Example: Send 0.01 KITE to another address
    recipient = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"  # Example address
    amount_kite = 0.01
    amount_wei = facilitator.w3.to_wei(amount_kite, 'ether')
    
    transaction = {
        'to': recipient,
        'value': amount_wei,
        'data': '0x',
        'gas': 21000,
    }
    
    console.print(f"[dim]To: {recipient}[/dim]")
    console.print(f"[dim]Value: {amount_kite} KITE[/dim]")
    console.print(f"[dim]Gas: 21000[/dim]\n")
    
    # Initialize policy engine
    console.print("[cyan]→ Initializing AgentShield policy engine...[/cyan]")
    
    # Create a simple policy for demo
    policy_config = {
        "version": "2.0",
        "enabled": True,
        "policies": [
            {
                "type": "eth_value_limit",
                "max_value_wei": str(facilitator.w3.to_wei(1, 'ether')),  # 1 KITE limit
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
        "simulation": {
            "enabled": False,  # Disable for basic demo
            "fail_on_revert": True
        },
        "logging": {
            "level": "info"
        },
        "llm_validation": {
            "enabled": False  # Disable for basic demo
        }
    }
    
    # Create policy engine with config
    from agentshield.policy_engine import PolicyConfig
    config = PolicyConfig(policy_config)
    
    from agentshield import PolicyEngine
    policy_engine = PolicyEngine(config_path=None)
    policy_engine.config = config
    policy_engine.chain_id = facilitator.CHAIN_ID
    
    console.print("[green]✓ Policy engine initialized[/green]\n")
    
    # Validate transaction
    console.print(Panel(
        "[bold cyan]Running 4-Stage Validation Pipeline[/bold cyan]",
        border_style="cyan"
    ))
    console.print()
    
    passed, reason = policy_engine.validate_transaction(transaction, facilitator.address)
    
    console.print()
    
    # Show result
    if passed:
        console.print(Panel(
            "[bold green]✅ TRANSACTION APPROVED[/bold green]\n\n"
            f"Reason: {reason}\n\n"
            "[dim]All security checks passed. Transaction is safe to execute.[/dim]",
            title="Validation Result",
            border_style="green"
        ))
        
        console.print("\n[dim]In a real scenario, this transaction would now be signed and broadcast to Kite Chain.[/dim]\n")
    else:
        console.print(Panel(
            "[bold red]❌ TRANSACTION BLOCKED[/bold red]\n\n"
            f"Reason: {reason}\n\n"
            "[dim]Transaction blocked before signature. Funds are safe.[/dim]",
            title="Validation Result",
            border_style="red"
        ))
        console.print()


def main():
    """Main demo function"""
    print_header()
    
    try:
        demo_transaction_validation()
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]\n")
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]\n")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]\n")
    
    console.print("[dim]Demo complete![/dim]\n")


if __name__ == "__main__":
    main()
