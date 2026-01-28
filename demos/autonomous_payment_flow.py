"""
Demo: Agent-to-Agent Payment on Kite AI with AgentShield

This demo shows two AI agents transacting autonomously with AgentShield security.
Agent A provides a service, Agent B pays for it, AgentShield validates everything.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentshield.facilitators.kite_facilitator import KiteFacilitator
from agentshield import PolicyEngine
from agentshield.policy_engine import PolicyConfig
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

console = Console()


class Agent:
    """Base AI Agent class"""
    
    def __init__(self, name: str, role: str, facilitator: KiteFacilitator):
        self.name = name
        self.role = role
        self.facilitator = facilitator
        self.address = facilitator.address
        
    def get_balance(self) -> float:
        """Get agent's balance"""
        return self.facilitator.get_balance()
    
    def speak(self, message: str):
        """Agent speaks"""
        color = "cyan" if self.role == "Provider" else "magenta"
        console.print(f"[{color}]{self.name}:[/{color}] {message}")


class ServiceProvider(Agent):
    """Agent A - Service Provider"""
    
    def __init__(self, facilitator: KiteFacilitator):
        super().__init__("Agent A", "Provider", facilitator)
        self.service_price = 0.05  # 0.05 KITE per service
    
    def offer_service(self) -> dict:
        """Offer service to consumers"""
        return {
            "service": "Premium Data API Access",
            "price": self.service_price,
            "currency": "KITE",
            "provider": self.address
        }
    
    def deliver_service(self, consumer_address: str):
        """Deliver service after payment"""
        self.speak(f"✅ Payment received! Delivering service to {consumer_address[:10]}...")
        time.sleep(1)
        self.speak("📦 Service delivered: API Key = 'sk-demo-12345'")


class ServiceConsumer(Agent):
    """Agent B - Service Consumer"""
    
    def __init__(self, facilitator: KiteFacilitator, policy_engine: PolicyEngine):
        super().__init__("Agent B", "Consumer", facilitator)
        self.policy_engine = policy_engine
    
    def request_service(self, provider: ServiceProvider):
        """Request service from provider"""
        self.speak(f"🔍 Requesting service from {provider.name}...")
        return provider.offer_service()
    
    def pay_for_service(self, service_info: dict) -> tuple:
        """Pay for service with AgentShield validation"""
        price = service_info['price']
        provider_address = service_info['provider']
        
        self.speak(f"💰 Initiating payment: {price} KITE to {provider_address[:10]}...")
        
        # Create transaction
        amount_wei = self.facilitator.w3.to_wei(price, 'ether')
        transaction = {
            'to': provider_address,
            'value': amount_wei,
            'data': '0x',
            'gas': 21000,
            'gasPrice': self.facilitator.w3.eth.gas_price,
            'nonce': self.facilitator.w3.eth.get_transaction_count(self.address),
            'chainId': self.facilitator.CHAIN_ID
        }
        
        # Validate with AgentShield
        self.speak("🛡️  Validating payment with AgentShield...")
        passed, reason = self.policy_engine.validate_transaction(transaction, self.address)
        
        if not passed:
            self.speak(f"❌ Payment blocked: {reason}")
            return False, reason
        
        self.speak("✅ Payment approved by AgentShield!")
        
        # Execute transaction
        try:
            signed_tx = self.facilitator.w3.eth.account.sign_transaction(
                transaction,
                self.facilitator.private_key
            )
            tx_hash = self.facilitator.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            self.speak(f"📤 Payment sent! Hash: {tx_hash.hex()[:20]}...")
            
            # Wait for confirmation
            receipt = self.facilitator.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            if receipt['status'] == 1:
                self.speak("✅ Payment confirmed on blockchain!")
                return True, tx_hash.hex()
            else:
                self.speak("❌ Payment failed on blockchain")
                return False, "Transaction reverted"
                
        except Exception as e:
            self.speak(f"❌ Payment error: {str(e)}")
            return False, str(e)


def print_header():
    """Print demo header"""
    console.print("\n" + "=" * 70)
    console.print("[bold cyan]Agent-to-Agent Payment on Kite AI[/bold cyan]")
    console.print("[dim]Autonomous Agents + AgentShield Security[/dim]")
    console.print("=" * 70 + "\n")


def demo_agent_to_agent():
    """Demo: Agent-to-agent payment with AgentShield"""
    
    print_header()
    
    console.print(Panel(
        "[bold]Scenario:[/bold]\n\n"
        "• Agent A (Provider) offers a premium data service\n"
        "• Agent B (Consumer) wants to use the service\n"
        "• Agent B pays Agent A autonomously\n"
        "• AgentShield validates the payment (4 stages)\n"
        "• Payment executes on Kite Chain\n"
        "• Agent A delivers the service",
        title="🤖 Agent-to-Agent Demo",
        border_style="cyan"
    ))
    console.print()
    
    # Initialize
    console.print("[cyan]→ Initializing agents...[/cyan]\n")
    
    # Create facilitator for Agent B (consumer)
    kite = KiteFacilitator()
    
    if not kite.is_connected():
        console.print("[red]❌ Failed to connect to Kite AI[/red]\n")
        return
    
    if not kite.address:
        console.print("[red]❌ No wallet configured[/red]\n")
        return
    
    balance = kite.get_balance()
    if balance < 0.1:
        console.print(Panel(
            f"[yellow]⚠️  Insufficient balance: {balance:.4f} KITE[/yellow]\n\n"
            "Need at least 0.1 KITE for this demo.\n"
            "Get tokens from: https://faucet.gokite.ai",
            title="Low Balance",
            border_style="yellow"
        ))
        console.print()
        return
    
    # Initialize policy engine
    policy_config = {
        "version": "2.0",
        "enabled": True,
        "policies": [
            {
                "type": "eth_value_limit",
                "max_value_wei": str(kite.w3.to_wei(1, 'ether')),
                "enabled": True,
                "description": "Limit to 1 KITE per transaction"
            },
            {
                "type": "gas_limit",
                "max_gas": 500000,
                "enabled": True
            }
        ],
        "simulation": {"enabled": False},
        "logging": {"level": "minimal"},
        "llm_validation": {"enabled": False}
    }
    
    config = PolicyConfig(policy_config)
    policy_engine = PolicyEngine(config_path=None)
    policy_engine.config = config
    policy_engine.chain_id = kite.CHAIN_ID
    
    # Create agents
    # Note: In real scenario, Agent A would have its own wallet
    # For demo, we use same wallet but show the concept
    agent_a = ServiceProvider(kite)
    agent_b = ServiceConsumer(kite, policy_engine)
    
    # Show agent info
    table = Table(title="Agent Information")
    table.add_column("Agent", style="cyan")
    table.add_column("Role", style="white")
    table.add_column("Address", style="dim")
    table.add_column("Balance", style="green")
    
    table.add_row(
        agent_a.name,
        agent_a.role,
        agent_a.address[:20] + "...",
        f"{agent_a.get_balance():.4f} KITE"
    )
    table.add_row(
        agent_b.name,
        agent_b.role,
        agent_b.address[:20] + "...",
        f"{agent_b.get_balance():.4f} KITE"
    )
    
    console.print(table)
    console.print()
    
    # Start interaction
    console.print(Panel(
        "[bold cyan]Starting Agent Interaction[/bold cyan]",
        border_style="cyan"
    ))
    console.print()
    
    # Step 1: Agent B requests service
    service_info = agent_b.request_service(agent_a)
    time.sleep(0.5)
    
    # Step 2: Agent A offers service
    agent_a.speak(f"📋 Offering: {service_info['service']}")
    agent_a.speak(f"💵 Price: {service_info['price']} {service_info['currency']}")
    time.sleep(0.5)
    console.print()
    
    # Step 3: Agent B decides to pay
    agent_b.speak("✅ Accepting offer. Proceeding with payment...")
    console.print()
    time.sleep(0.5)
    
    # Step 4: Payment with AgentShield validation
    console.print(Panel(
        "[bold]AgentShield 4-Stage Validation[/bold]",
        border_style="yellow"
    ))
    console.print()
    
    success, result = agent_b.pay_for_service(service_info)
    console.print()
    
    # Step 5: Service delivery or failure
    if success:
        agent_a.deliver_service(agent_b.address)
        console.print()
        
        # Show final balances
        console.print("[cyan]→ Final balances:[/cyan]")
        console.print(f"  {agent_a.name}: {agent_a.get_balance():.4f} KITE")
        console.print(f"  {agent_b.name}: {agent_b.get_balance():.4f} KITE")
        console.print()
        
        # Show transaction
        console.print(Panel(
            "[bold green]🎉 TRANSACTION SUCCESSFUL![/bold green]\n\n"
            f"Transaction Hash: {result}\n\n"
            f"View on explorer:\n{kite.get_transaction_url(result)}",
            title="Success",
            border_style="green"
        ))
    else:
        console.print(Panel(
            "[bold red]❌ TRANSACTION FAILED[/bold red]\n\n"
            f"Reason: {result}\n\n"
            "Funds are safe. No payment was executed.",
            title="Failed",
            border_style="red"
        ))
    
    console.print()


def main():
    """Main function"""
    try:
        demo_agent_to_agent()
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted[/yellow]\n")
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]\n")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]\n")


if __name__ == "__main__":
    main()
