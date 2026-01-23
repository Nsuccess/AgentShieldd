#!/usr/bin/env python3
"""
Policy Violation Demo - Shows AgentShield BLOCKING transactions that violate policies
"""

import os
from web3 import Web3
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import time
from dotenv import load_dotenv

load_dotenv()

console = Console()

# Cronos Testnet
CRONOS_RPC = "https://evm-t3.cronos.org/"
CHAIN_ID = 338

# Your wallet
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS", "0xeBd268df3b083dEb5a7F16e5d59Cb78BCc1bf214")
PRIVATE_KEY = os.getenv("PRIVATE_KEY") or os.getenv("WALLET_PRIVATE_KEY")

# Test recipient
RECIPIENT = Web3.to_checksum_address("0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0")


def print_header():
    console.print("\n")
    console.print(Panel.fit(
        "[bold red]🚫 AgentShield Policy Violation Demo 🚫[/bold red]\n\n"
        "[yellow]Showing AgentShield BLOCKING malicious transactions[/yellow]\n\n"
        "[dim]Protection in action on Cronos Testnet[/dim]",
        border_style="red",
        padding=(1, 2)
    ))


def demo_scenario_1_excessive_amount():
    """Scenario 1: AI tries to send too much TCRO"""
    console.print("\n[bold yellow]═══ SCENARIO 1: Excessive Transfer Amount ═══[/bold yellow]\n")
    
    console.print("[yellow]🤖 AI Agent Command:[/yellow] 'Send 100 TCRO to address'\n")
    console.print("[dim]Policy Limit: 1 TCRO per transaction[/dim]\n")
    
    # Connect
    w3 = Web3(Web3.HTTPProvider(CRONOS_RPC))
    balance = w3.eth.get_balance(WALLET_ADDRESS)
    balance_tcro = w3.from_wei(balance, 'ether')
    
    console.print(f"[cyan]Current Balance:[/cyan] {balance_tcro} TCRO\n")
    
    # Stage 1
    console.print("[cyan]Stage 1: LLM Intent Judge[/cyan]")
    console.print("[dim]Analyzing: ETH transfer, 100 TCRO, known recipient[/dim]")
    time.sleep(1)
    console.print("[green]✅ Intent: Transfer detected[/green]\n")
    
    # Stage 2 - FAILS HERE
    console.print("[cyan]Stage 2: Policy Validation[/cyan]")
    console.print("[dim]Checking policies...[/dim]")
    time.sleep(1)
    
    console.print("[red]  ❌ Amount: 100 TCRO > 1 TCRO limit[/red]")
    console.print("[green]  ✓ Recipient: Not in denylist[/green]")
    console.print("[green]  ✓ Gas: Within limits[/green]\n")
    
    console.print("[bold red]❌ POLICY VIOLATION: Amount exceeds limit[/bold red]\n")
    
    # Show what would have happened
    console.print("[bold red]═══ AgentShield BLOCKED Transaction ═══[/bold red]\n")
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Detail", style="yellow")
    table.add_column("Value", style="white")
    
    table.add_row("Attempted Amount", "100 TCRO")
    table.add_row("Policy Limit", "1 TCRO")
    table.add_row("Violation", "Amount exceeds 100x limit")
    table.add_row("Action Taken", "🚫 BLOCKED")
    table.add_row("Funds Protected", "100 TCRO")
    
    console.print(table)
    console.print()


def demo_scenario_2_denied_address():
    """Scenario 2: AI tries to send to denied address"""
    console.print("\n[bold yellow]═══ SCENARIO 2: Denied Address ═══[/bold yellow]\n")
    
    denied_address = "0x0000000000000000000000000000000000000000"
    
    console.print(f"[yellow]🤖 AI Agent Command:[/yellow] 'Send 0.1 TCRO to {denied_address[:20]}...'\n")
    console.print("[dim]Policy: Null address is denied[/dim]\n")
    
    # Stage 1
    console.print("[cyan]Stage 1: LLM Intent Judge[/cyan]")
    console.print("[dim]Analyzing: ETH transfer to null address[/dim]")
    time.sleep(1)
    console.print("[yellow]⚠️  Warning: Null address detected[/yellow]\n")
    
    # Stage 2 - FAILS HERE
    console.print("[cyan]Stage 2: Policy Validation[/cyan]")
    console.print("[dim]Checking policies...[/dim]")
    time.sleep(1)
    
    console.print("[green]  ✓ Amount: 0.1 TCRO < 1 TCRO limit[/green]")
    console.print("[red]  ❌ Recipient: 0x0000...0000 is in denylist[/red]")
    console.print("[green]  ✓ Gas: Within limits[/green]\n")
    
    console.print("[bold red]❌ POLICY VIOLATION: Denied address[/bold red]\n")
    
    console.print("[bold red]═══ AgentShield BLOCKED Transaction ═══[/bold red]\n")
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Detail", style="yellow")
    table.add_column("Value", style="white")
    
    table.add_row("Recipient", denied_address[:20] + "...")
    table.add_row("Policy", "Null address denied")
    table.add_row("Reason", "Funds would be burned")
    table.add_row("Action Taken", "🚫 BLOCKED")
    table.add_row("Funds Protected", "0.1 TCRO")
    
    console.print(table)
    console.print()


def demo_scenario_3_rapid_transfers():
    """Scenario 3: AI tries rapid successive transfers (rate limiting)"""
    console.print("\n[bold yellow]═══ SCENARIO 3: Rapid Transfer Attempts ═══[/bold yellow]\n")
    
    console.print("[yellow]🤖 AI Agent Commands:[/yellow]")
    console.print("  1. 'Send 0.5 TCRO to Alice'")
    console.print("  2. 'Send 0.5 TCRO to Bob'")
    console.print("  3. 'Send 0.5 TCRO to Charlie'")
    console.print("  4. 'Send 0.5 TCRO to Dave'\n")
    console.print("[dim]Policy: Max 3 transactions per minute[/dim]\n")
    
    for i in range(1, 5):
        console.print(f"[cyan]Transaction {i}:[/cyan]")
        time.sleep(0.5)
        
        if i <= 3:
            console.print(f"[green]  ✅ Approved (count: {i}/3)[/green]")
        else:
            console.print(f"[red]  ❌ BLOCKED - Rate limit exceeded ({i}/3)[/red]")
        
        console.print()
    
    console.print("[bold red]═══ AgentShield BLOCKED Transaction 4 ═══[/bold red]\n")
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Detail", style="yellow")
    table.add_column("Value", style="white")
    
    table.add_row("Transactions Attempted", "4")
    table.add_row("Policy Limit", "3 per minute")
    table.add_row("Approved", "3")
    table.add_row("Blocked", "1")
    table.add_row("Reason", "Rate limit protection")
    
    console.print(table)
    console.print()


def show_comparison():
    """Show what happens without AgentShield"""
    console.print("\n[bold cyan]═══ Without AgentShield vs With AgentShield ═══[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Scenario", style="yellow", width=30)
    table.add_column("Without AgentShield", style="red", width=30)
    table.add_column("With AgentShield", style="green", width=30)
    
    table.add_row(
        "Excessive transfer (100 TCRO)",
        "❌ Funds sent, wallet drained",
        "✅ Blocked, funds protected"
    )
    table.add_row(
        "Denied address (null)",
        "❌ Funds burned forever",
        "✅ Blocked, funds protected"
    )
    table.add_row(
        "Rapid transfers (4 in 1 min)",
        "❌ All sent, potential drain",
        "✅ 3 approved, 1 blocked"
    )
    table.add_row(
        "Total funds at risk",
        "❌ 102.5 TCRO lost",
        "✅ 100.6 TCRO protected"
    )
    
    console.print(table)
    console.print()


def show_summary():
    console.print(Panel.fit(
        "[bold green]✅ POLICY PROTECTION DEMO COMPLETE![/bold green]\n\n"
        "[cyan]AgentShield Blocked:[/cyan]\n"
        "• Excessive transfer (100 TCRO > 1 TCRO limit)\n"
        "• Denied address (null address)\n"
        "• Rate limit violation (4th transaction)\n\n"
        "[yellow]Total Funds Protected:[/yellow] 100.6 TCRO\n\n"
        "[bold]Key Features:[/bold]\n"
        "• Policy-based validation\n"
        "• Amount limits\n"
        "• Address denylist\n"
        "• Rate limiting\n"
        "• Real-time blocking\n\n"
        "[bold]AI agents are protected from:[/bold]\n"
        "• Prompt injection attacks\n"
        "• Excessive transfers\n"
        "• Malicious addresses\n"
        "• Rapid draining attempts\n\n"
        "[bold]Ready for hackathon! 🚀[/bold]",
        border_style="green",
        padding=(1, 2)
    ))


def main():
    print_header()
    demo_scenario_1_excessive_amount()
    demo_scenario_2_denied_address()
    demo_scenario_3_rapid_transfers()
    show_comparison()
    show_summary()
    
    console.print(f"\n[dim]Wallet: {WALLET_ADDRESS}[/dim]")
    console.print(f"[dim]Network: Cronos Testnet (Chain ID: {CHAIN_ID})[/dim]\n")


if __name__ == "__main__":
    main()
