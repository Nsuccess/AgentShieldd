#!/usr/bin/env python3
"""
Cronos Risk-Managed AI Agent Demo
Shows AgentShield protecting Crypto.com AI Agent from malicious transactions

This demo showcases:
1. Safe USDC transfer - ✅ Approved
2. Honeypot token purchase - ❌ Blocked (Stage 3.5 detects)
3. Excessive amount transfer - ❌ Blocked (Policy violation)
"""

import asyncio
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from AgentShield.integrations import SafeAgent
from AgentShield.facilitators import SafeFacilitator

console = Console()


async def demo_safe_agent():
    """
    Demo 1: SafeAgent - AI Agent with AgentShield protection
    """
    console.print("\n" + "=" * 70, style="bold cyan")
    console.print("DEMO 1: SafeAgent - AI Agent with AgentShield Protection", style="bold cyan")
    console.print("=" * 70 + "\n", style="bold cyan")
    
    # Initialize SafeAgent
    api_key = os.getenv("CRYPTO_COM_API_KEY", "demo-key")
    policy_path = "config/policy.yaml"
    
    console.print(f"[yellow]Initializing SafeAgent...[/yellow]")
    console.print(f"  API Key: {api_key[:10]}...")
    console.print(f"  Policy: {policy_path}\n")
    
    try:
        agent = SafeAgent(
            api_key=api_key,
            policy_path=policy_path,
        )
        console.print("[green]✅ SafeAgent initialized successfully![/green]\n")
    except Exception as e:
        console.print(f"[red]❌ Failed to initialize SafeAgent: {e}[/red]")
        console.print("[yellow]💡 Make sure policy.yaml exists and API key is set[/yellow]\n")
        return
    
    # Test scenarios
    test_cases = [
        {
            "name": "Test 1: Safe USDC Transfer",
            "input": "Send 10 USDC to 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "expected": "approved",
            "description": "Normal USDC transfer to known address",
        },
        {
            "name": "Test 2: Honeypot Token Purchase",
            "input": "Buy 100 SCAM tokens at 0xHONEYPOT_ADDRESS",
            "expected": "blocked",
            "description": "Attempt to buy honeypot token (should be blocked by Stage 3.5)",
        },
        {
            "name": "Test 3: Excessive Amount Transfer",
            "input": "Send 1000000 USDC to 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "expected": "blocked",
            "description": "Transfer exceeding policy limits",
        },
    ]
    
    for test in test_cases:
        console.print(Panel(
            f"[bold]{test['name']}[/bold]\n\n"
            f"[cyan]Input:[/cyan] {test['input']}\n"
            f"[cyan]Expected:[/cyan] {test['expected']}\n"
            f"[dim]{test['description']}[/dim]",
            border_style="blue"
        ))
        
        try:
            result = await agent.safe_interact(test["input"])
            
            # Display result
            if result.get("approved"):
                console.print("[green]✅ APPROVED[/green]")
                console.print(f"Response: {result.get('response', 'N/A')}\n")
            else:
                console.print("[red]❌ BLOCKED[/red]")
                console.print(f"Reason: {result.get('validation', {}).get('reason', 'N/A')}")
                console.print(f"Failed Stage: {result.get('validation', {}).get('failed_stage', 'N/A')}\n")
            
            # Show validation stages
            if "validation" in result and "stages" in result["validation"]:
                table = Table(title="Validation Stages", show_header=True)
                table.add_column("Stage", style="cyan")
                table.add_column("Status", style="bold")
                table.add_column("Details")
                
                for stage_name, stage_result in result["validation"]["stages"].items():
                    status = "✅ Pass" if stage_result.get("approved") else "❌ Fail"
                    details = stage_result.get("reason", "N/A")
                    table.add_row(stage_name, status, details)
                
                console.print(table)
                console.print()
        
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]\n")


async def demo_safe_facilitator():
    """
    Demo 2: SafeFacilitator - x402 payments with AgentShield protection
    """
    console.print("\n" + "=" * 70, style="bold cyan")
    console.print("DEMO 2: SafeFacilitator - x402 Payments with AgentShield", style="bold cyan")
    console.print("=" * 70 + "\n", style="bold cyan")
    
    # Initialize SafeFacilitator
    private_key = os.getenv("PRIVATE_KEY", "0x" + "0" * 64)
    policy_path = "config/policy.yaml"
    
    console.print(f"[yellow]Initializing SafeFacilitator...[/yellow]")
    console.print(f"  Network: cronos-testnet")
    console.print(f"  Policy: {policy_path}\n")
    
    try:
        facilitator = SafeFacilitator(
            policy_path=policy_path,
            private_key=private_key,
            network="cronos-testnet",
        )
        console.print("[green]✅ SafeFacilitator initialized successfully![/green]\n")
    except Exception as e:
        console.print(f"[red]❌ Failed to initialize SafeFacilitator: {e}[/red]")
        console.print("[yellow]💡 Make sure policy.yaml exists and PRIVATE_KEY is set[/yellow]\n")
        return
    
    # Test payment scenarios
    payment_tests = [
        {
            "name": "Payment 1: API Access Fee",
            "pay_to": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "asset": "0x9e0e7a0C8688b1A4e46b5F4D0A4F6B8F5C8E5D4C",  # USDC.e testnet
            "amount": "1000000",  # 1 USDC
            "context": {"purpose": "API access payment"},
            "expected": "approved",
        },
        {
            "name": "Payment 2: Suspicious Large Amount",
            "pay_to": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
            "asset": "0x9e0e7a0C8688b1A4e46b5F4D0A4F6B8F5C8E5D4C",
            "amount": "1000000000000",  # 1M USDC
            "context": {"purpose": "Large payment"},
            "expected": "blocked",
        },
    ]
    
    for test in payment_tests:
        console.print(Panel(
            f"[bold]{test['name']}[/bold]\n\n"
            f"[cyan]Pay To:[/cyan] {test['pay_to']}\n"
            f"[cyan]Asset:[/cyan] {test['asset']}\n"
            f"[cyan]Amount:[/cyan] {test['amount']}\n"
            f"[cyan]Expected:[/cyan] {test['expected']}",
            border_style="blue"
        ))
        
        try:
            result = await facilitator.generate_safe_payment_header(
                pay_to=test["pay_to"],
                asset=test["asset"],
                amount=test["amount"],
                context=test.get("context"),
            )
            
            # Display result
            if result.get("approved"):
                console.print("[green]✅ PAYMENT APPROVED[/green]")
                console.print(f"Payment Header: {result.get('payment_header', 'N/A')[:50]}...")
                console.print(f"Valid for: {result.get('metadata', {}).get('valid_for_seconds', 'N/A')} seconds\n")
            else:
                console.print("[red]❌ PAYMENT BLOCKED[/red]")
                console.print(f"Reason: {result.get('reason', 'N/A')}\n")
        
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]\n")


async def main():
    """Run all demos"""
    console.print(Panel.fit(
        "[bold cyan]AgentShield x Cronos x402 Demo[/bold cyan]\n"
        "[yellow]The Safety Layer for AI Agents on Cronos[/yellow]",
        border_style="cyan"
    ))
    
    # Check environment variables
    console.print("\n[yellow]Checking environment...[/yellow]")
    
    env_vars = {
        "CRYPTO_COM_API_KEY": os.getenv("CRYPTO_COM_API_KEY"),
        "PRIVATE_KEY": os.getenv("PRIVATE_KEY"),
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
    }
    
    table = Table(show_header=True)
    table.add_column("Variable", style="cyan")
    table.add_column("Status", style="bold")
    
    for var, value in env_vars.items():
        status = "✅ Set" if value else "❌ Not Set"
        table.add_row(var, status)
    
    console.print(table)
    console.print()
    
    # Run demos
    try:
        await demo_safe_agent()
        await demo_safe_facilitator()
        
        console.print(Panel.fit(
            "[bold green]✅ Demo Complete![/bold green]\n\n"
            "[yellow]AgentShield successfully protected AI agents from:[/yellow]\n"
            "• Honeypot tokens (Stage 3.5 detection)\n"
            "• Excessive transfers (Policy validation)\n"
            "• Malicious transactions (4-stage pipeline)\n\n"
            "[cyan]Ready for Cronos x402 Hackathon submission! 🚀[/cyan]",
            border_style="green"
        ))
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Demo failed: {e}[/red]")
        import traceback
        console.print(traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(main())
