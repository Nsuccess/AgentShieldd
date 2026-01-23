#!/usr/bin/env python3
"""
Quick Demo - AgentShield x Cronos x402
Shows the complete integration working without requiring testnet funds
"""

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from AgentShield.facilitators import CronosFacilitator

console = Console()


def demo_facilitator():
    """Demo 1: Show CronosFacilitator in action"""
    console.print(Panel.fit(
        "[bold cyan]Demo 1: CronosFacilitator[/bold cyan]\n"
        "[yellow]Python implementation of EIP-3009 payment headers[/yellow]",
        border_style="cyan"
    ))
    
    # Initialize facilitator
    console.print("\n[bold]Step 1:[/bold] Initialize CronosFacilitator")
    code = """
from AgentShield.facilitators import CronosFacilitator

facilitator = CronosFacilitator(network="cronos-testnet")
"""
    console.print(Syntax(code, "python", theme="monokai", line_numbers=False))
    
    facilitator = CronosFacilitator(network="cronos-testnet")
    console.print(f"[green]✅ Initialized for {facilitator.network} (Chain ID: {facilitator.chain_id})[/green]\n")
    
    # Generate payment header
    console.print("[bold]Step 2:[/bold] Generate EIP-3009 payment header")
    code = """
header = facilitator.generate_payment_header(
    private_key="0x" + "1" * 64,  # Test key
    pay_to="0x742D35CC6634c0532925A3b844BC9E7595F0BEb0",
    asset="0xc21223249CA28397B4B6541dfFaEcC539BfF0141",  # USDC.e
    amount="1000000",  # 1 USDC
    timeout_seconds=300
)
"""
    console.print(Syntax(code, "python", theme="monokai", line_numbers=False))
    
    test_private_key = "0x" + "1" * 64
    header = facilitator.generate_payment_header(
        private_key=test_private_key,
        pay_to="0x742D35CC6634c0532925A3b844BC9E7595F0BEb0",
        asset="0xc21223249CA28397B4B6541dfFaEcC539BfF0141",
        amount="1000000",
        timeout_seconds=300,
    )
    
    console.print(f"[green]✅ Payment header generated![/green]")
    console.print(f"[dim]Header (first 80 chars): {header[:80]}...[/dim]\n")
    
    # Decode and show
    console.print("[bold]Step 3:[/bold] Decode payment header")
    decoded = facilitator.decode_payment_header(header)
    
    console.print("[cyan]Payment Details:[/cyan]")
    console.print(f"  • Version: [yellow]{decoded['x402Version']}[/yellow]")
    console.print(f"  • Scheme: [yellow]{decoded['scheme']}[/yellow]")
    console.print(f"  • Network: [yellow]{decoded['network']}[/yellow]")
    console.print(f"  • From: [yellow]{decoded['payload']['from']}[/yellow]")
    console.print(f"  • To: [yellow]{decoded['payload']['to']}[/yellow]")
    console.print(f"  • Amount: [yellow]{decoded['payload']['value']}[/yellow] (1 USDC)")
    console.print(f"  • Signature: [yellow]{decoded['payload']['signature'][:20]}...[/yellow]\n")


def demo_safe_facilitator():
    """Demo 2: Show SafeFacilitator with AgentShield validation"""
    console.print(Panel.fit(
        "[bold cyan]Demo 2: SafeFacilitator[/bold cyan]\n"
        "[yellow]Adding 4-stage AgentShield validation to x402 payments[/yellow]",
        border_style="cyan"
    ))
    
    console.print("\n[bold]Integration Example:[/bold]")
    code = """
from AgentShield.facilitators import SafeFacilitator

# Initialize with AgentShield validation
safe_facilitator = SafeFacilitator(
    policy_path="config/policy.yaml",
    private_key="0x...",
    network="cronos-testnet"
)

# Generate payment with validation
result = await safe_facilitator.generate_safe_payment_header(
    pay_to="0x742D35CC6634c0532925A3b844BC9E7595F0BEb0",
    asset="0xc21223249CA28397B4B6541dfFaEcC539BfF0141",
    amount="1000000",
    context={"purpose": "API access"}
)

if result["approved"]:
    # Payment passed all 4 validation stages!
    payment_header = result["payment_header"]
    print("✅ Safe to proceed with payment")
else:
    # Payment blocked by AgentShield
    print(f"❌ Blocked: {result['reason']}")
"""
    console.print(Syntax(code, "python", theme="monokai", line_numbers=False))
    
    console.print("\n[cyan]4-Stage Validation Pipeline:[/cyan]")
    console.print("  [yellow]Stage 1:[/yellow] LLM Intent Judge - Validates transaction intent")
    console.print("  [yellow]Stage 2:[/yellow] Policy Validation - Checks whitelist/blacklist, limits")
    console.print("  [yellow]Stage 3:[/yellow] Tenderly Simulation - Simulates transaction on fork")
    console.print("  [yellow]Stage 3.5:[/yellow] Honeypot Detection - Simulates BUY → SELL")
    console.print("  [yellow]Stage 4:[/yellow] LLM Analysis - Analyzes simulation results\n")


def demo_x402_flow():
    """Demo 3: Show complete x402 protocol flow"""
    console.print(Panel.fit(
        "[bold cyan]Demo 3: x402 Protocol Flow[/bold cyan]\n"
        "[yellow]Complete payment flow with resource service[/yellow]",
        border_style="cyan"
    ))
    
    console.print("\n[bold]x402 Protocol Flow:[/bold]\n")
    
    console.print("[yellow]1. Client requests protected resource[/yellow]")
    console.print("   [dim]GET /api/protected-data[/dim]\n")
    
    console.print("[yellow]2. Service returns 402 Payment Required[/yellow]")
    console.print("   [dim]Status: 402[/dim]")
    console.print("   [dim]Body: { accepts: [{ payTo, asset, maxAmountRequired, ... }] }[/dim]\n")
    
    console.print("[yellow]3. Client generates payment header[/yellow]")
    console.print("   [dim]Uses CronosFacilitator to sign EIP-3009 authorization[/dim]\n")
    
    console.print("[yellow]4. Client settles payment[/yellow]")
    console.print("   [dim]POST /api/pay[/dim]")
    console.print("   [dim]Body: { paymentId, paymentHeader, paymentRequirements }[/dim]\n")
    
    console.print("[yellow]5. Service verifies and settles[/yellow]")
    console.print("   [dim]Facilitator verifies signature and executes token transfer[/dim]\n")
    
    console.print("[yellow]6. Client retries with payment ID[/yellow]")
    console.print("   [dim]GET /api/protected-data[/dim]")
    console.print("   [dim]Header: x-payment-id: <paymentId>[/dim]\n")
    
    console.print("[yellow]7. Service returns protected content[/yellow]")
    console.print("   [dim]Status: 200[/dim]")
    console.print("   [dim]Body: { ok: true, data: { ... } }[/dim]\n")


def demo_architecture():
    """Demo 4: Show AgentShield architecture"""
    console.print(Panel.fit(
        "[bold cyan]Demo 4: AgentShield Architecture[/bold cyan]\n"
        "[yellow]The Safety Layer for AI Agents on Cronos[/yellow]",
        border_style="cyan"
    ))
    
    console.print("\n[bold]Component Overview:[/bold]\n")
    
    console.print("[cyan]1. CronosFacilitator[/cyan]")
    console.print("   • Python implementation of EIP-3009 payment headers")
    console.print("   • Compatible with Cronos x402 protocol")
    console.print("   • Uses eth_account for EIP-712 signing\n")
    
    console.print("[cyan]2. SafeFacilitator[/cyan]")
    console.print("   • Wraps CronosFacilitator with AgentShield validation")
    console.print("   • 4-stage security pipeline")
    console.print("   • Blocks malicious transactions before execution\n")
    
    console.print("[cyan]3. SafeAgent[/cyan]")
    console.print("   • Wraps Crypto.com AI Agent SDK")
    console.print("   • Intercepts blockchain transactions")
    console.print("   • Validates through AgentShield pipeline\n")
    
    console.print("[cyan]4. x402 Resource Service[/cyan]")
    console.print("   • Bun-based API server")
    console.print("   • Implements x402 payment protocol")
    console.print("   • Agent discovery (A2A protocol)\n")
    
    console.print("[bold]Key Features:[/bold]\n")
    console.print("  [green]✅[/green] Honeypot Detection (Stage 3.5)")
    console.print("  [green]✅[/green] LLM-based Intent Validation")
    console.print("  [green]✅[/green] Policy Enforcement")
    console.print("  [green]✅[/green] Transaction Simulation")
    console.print("  [green]✅[/green] x402 Payment Integration\n")


def main():
    """Run all demos"""
    console.print("\n")
    console.print(Panel.fit(
        "[bold white]AgentShield x Cronos x402[/bold white]\n"
        "[cyan]The Safety Layer for AI Agents on Cronos[/cyan]\n\n"
        "[dim]Quick Demo - No Testnet Required[/dim]",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    # Demo 1: Facilitator
    demo_facilitator()
    console.print("\n" + "─" * 80 + "\n")
    
    # Demo 2: SafeFacilitator
    demo_safe_facilitator()
    console.print("\n" + "─" * 80 + "\n")
    
    # Demo 3: x402 Flow
    demo_x402_flow()
    console.print("\n" + "─" * 80 + "\n")
    
    # Demo 4: Architecture
    demo_architecture()
    
    # Summary
    console.print(Panel.fit(
        "[bold green]✅ Demo Complete![/bold green]\n\n"
        "[cyan]What We Showed:[/cyan]\n"
        "  • Python implementation of Cronos x402 Facilitator\n"
        "  • 4-stage AgentShield validation pipeline\n"
        "  • Complete x402 protocol flow\n"
        "  • Clean architecture and integration\n\n"
        "[yellow]Next Steps:[/yellow]\n"
        "  1. Get testnet wallet (2 min)\n"
        "  2. Get testnet TCRO (3 min)\n"
        "  3. Run live demo (5 min)\n"
        "  4. Record video (30 min)\n"
        "  5. Submit to DoraHacks (10 min)\n\n"
        "[bold]Expected Prize: $8,000[/bold] 💰",
        border_style="green",
        padding=(1, 2)
    ))


if __name__ == "__main__":
    main()
