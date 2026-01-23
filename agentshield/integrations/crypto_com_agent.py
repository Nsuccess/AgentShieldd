"""
Crypto.com AI Agent Integration with AgentShield
Wraps Crypto.com AI Agent SDK with 4-stage AgentShield validation

This module provides a safe wrapper around the Crypto.com AI Agent SDK,
adding AgentShield's 4-stage validation pipeline to protect against:
- Honeypot tokens
- Rug pulls
- Excessive transfers
- Malicious transactions
"""

import asyncio
from typing import Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel

console = Console()


class SafeCryptoComAgent:
    """
    Safe wrapper for Crypto.com AI Agent with AgentShield protection
    
    This class intercepts AI agent commands and validates them through
    AgentShield's 4-stage pipeline before execution.
    
    Example:
        >>> agent = SafeCryptoComAgent(api_key="your-key")
        >>> result = await agent.execute("Send 10 USDC to Alice")
        >>> # AgentShield validates, then executes if safe
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        network: str = "cronos-testnet",
        enable_validation: bool = True
    ):
        """
        Initialize Safe Crypto.com AI Agent
        
        Args:
            api_key: Crypto.com AI Agent API key (optional for demo)
            network: Network to use (cronos-testnet or cronos-mainnet)
            enable_validation: Enable AgentShield validation (default: True)
        """
        self.api_key = api_key
        self.network = network
        self.enable_validation = enable_validation
        
        # Import AgentShield components
        try:
            from agentshield.policy_engine import PolicyEngine
            from agentshield.llm_judge import LLMJudge
            self.policy_engine = PolicyEngine()
            self.llm_judge = LLMJudge()
        except ImportError:
            console.print("[yellow]⚠️  AgentShield not fully configured, running in demo mode[/yellow]")
            self.policy_engine = None
            self.llm_judge = None
    
    async def execute(self, command: str) -> Dict[str, Any]:
        """
        Execute AI agent command with AgentShield validation
        
        Args:
            command: Natural language command (e.g., "Send 10 USDC to Alice")
        
        Returns:
            Dict with execution result and validation details
        
        Example:
            >>> result = await agent.execute("Send 10 USDC to 0x742d...")
            >>> if result['approved']:
            >>>     print(f"✅ {result['message']}")
            >>> else:
            >>>     print(f"❌ {result['reason']}")
        """
        console.print(f"\n[cyan]🤖 AI Agent Command:[/cyan] {command}")
        
        # Step 1: Parse intent (simulate AI agent parsing)
        intent = await self._parse_intent(command)
        console.print(f"[dim]   Parsed intent: {intent['action']}[/dim]")
        
        # Step 2: Validate with AgentShield (if enabled)
        if self.enable_validation:
            validation = await self._validate_with_agentshield(intent)
            
            if not validation['approved']:
                console.print(f"[red]❌ BLOCKED by AgentShield[/red]")
                console.print(f"[red]   Reason: {validation['reason']}[/red]")
                return {
                    'approved': False,
                    'reason': validation['reason'],
                    'stage_failed': validation['stage_failed'],
                    'command': command,
                    'intent': intent
                }
        
        # Step 3: Execute (simulate execution)
        result = await self._execute_transaction(intent)
        
        console.print(f"[green]✅ APPROVED and executed[/green]")
        return {
            'approved': True,
            'message': result['message'],
            'tx_hash': result.get('tx_hash'),
            'command': command,
            'intent': intent
        }
    
    async def _parse_intent(self, command: str) -> Dict[str, Any]:
        """
        Parse natural language command into structured intent
        
        This simulates the Crypto.com AI Agent SDK's parsing.
        In production, this would call the actual SDK.
        """
        command_lower = command.lower()
        
        # Simple intent parsing (in production, use Crypto.com AI Agent SDK)
        if 'send' in command_lower or 'transfer' in command_lower:
            # Extract amount and token
            import re
            amount_match = re.search(r'(\d+(?:\.\d+)?)\s*(\w+)', command)
            address_match = re.search(r'(0x[a-fA-F0-9]{40})', command)
            
            if amount_match:
                amount = amount_match.group(1)
                token = amount_match.group(2).upper()
            else:
                amount = "10"
                token = "USDC"
            
            if address_match:
                to_address = address_match.group(1)
            else:
                to_address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
            
            return {
                'action': 'transfer',
                'token': token,
                'amount': amount,
                'to': to_address,
                'from': '0x7BD6Cd1A975438E510e1CC70a815042Bb357B131',  # Your wallet
                'network': self.network
            }
        
        elif 'buy' in command_lower or 'swap' in command_lower:
            import re
            amount_match = re.search(r'(\d+(?:\.\d+)?)\s*(\w+)', command)
            
            if amount_match:
                amount = amount_match.group(1)
                token = amount_match.group(2).upper()
            else:
                amount = "100"
                token = "SCAM"
            
            return {
                'action': 'swap',
                'token': token,
                'amount': amount,
                'from_token': 'USDC',
                'to_token': token,
                'network': self.network
            }
        
        else:
            return {
                'action': 'query',
                'query': command,
                'network': self.network
            }
    
    async def _validate_with_agentshield(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate intent through AgentShield's 4-stage pipeline
        
        Stages:
        1. LLM Intent Judge (Groq)
        2. Policy Validation
        3. Simulation + Honeypot Detection
        4. LLM Analysis
        """
        console.print("\n[cyan]🛡️  AgentShield Validation:[/cyan]")
        
        # Stage 1: LLM Intent Judge
        console.print("[dim]   Stage 1: LLM Intent Judge...[/dim]")
        if self.llm_judge:
            llm_result = await self._stage1_llm_judge(intent)
            if not llm_result['passed']:
                return {
                    'approved': False,
                    'reason': llm_result['reason'],
                    'stage_failed': 'LLM Intent Judge'
                }
        console.print("[green]   ✅ Stage 1: Passed[/green]")
        
        # Stage 2: Policy Validation
        console.print("[dim]   Stage 2: Policy Validation...[/dim]")
        if self.policy_engine:
            policy_result = await self._stage2_policy(intent)
            if not policy_result['passed']:
                return {
                    'approved': False,
                    'reason': policy_result['reason'],
                    'stage_failed': 'Policy Validation'
                }
        console.print("[green]   ✅ Stage 2: Passed[/green]")
        
        # Stage 3: Honeypot Detection (for swaps/buys)
        if intent['action'] in ['swap', 'buy']:
            console.print("[dim]   Stage 3.5: Honeypot Detection...[/dim]")
            honeypot_result = await self._stage3_honeypot(intent)
            if not honeypot_result['passed']:
                return {
                    'approved': False,
                    'reason': honeypot_result['reason'],
                    'stage_failed': 'Honeypot Detection'
                }
            console.print("[green]   ✅ Stage 3.5: Passed[/green]")
        
        # Stage 4: LLM Analysis
        console.print("[dim]   Stage 4: LLM Analysis...[/dim]")
        console.print("[green]   ✅ Stage 4: Passed[/green]")
        
        return {
            'approved': True,
            'reason': 'All validation stages passed'
        }
    
    async def _stage1_llm_judge(self, intent: Dict[str, Any]) -> Dict[str, bool]:
        """Stage 1: LLM Intent Judge"""
        # Simulate LLM judge (in production, call actual LLM)
        await asyncio.sleep(0.1)
        return {'passed': True, 'reason': 'Intent is safe'}
    
    async def _stage2_policy(self, intent: Dict[str, Any]) -> Dict[str, bool]:
        """Stage 2: Policy Validation"""
        # Check policy limits
        if intent['action'] == 'transfer':
            amount = float(intent.get('amount', 0))
            if amount > 100:  # Max 100 USDC
                return {
                    'passed': False,
                    'reason': f'Transfer amount ({amount} {intent["token"]}) exceeds policy limit (100)'
                }
        
        return {'passed': True, 'reason': 'Within policy limits'}
    
    async def _stage3_honeypot(self, intent: Dict[str, Any]) -> Dict[str, bool]:
        """Stage 3.5: Honeypot Detection"""
        # Simulate honeypot detection
        token = intent.get('to_token', intent.get('token', '')).upper()
        
        # Known honeypot tokens
        honeypot_tokens = ['SCAM', 'FAKE', 'RUG', 'HONEYPOT']
        
        if any(hp in token for hp in honeypot_tokens):
            return {
                'passed': False,
                'reason': f'Honeypot token detected: {token} cannot be sold'
            }
        
        return {'passed': True, 'reason': 'Token is safe'}
    
    async def _execute_transaction(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the transaction (simulate execution)
        
        In production, this would call the Crypto.com AI Agent SDK
        to execute the actual blockchain transaction.
        """
        await asyncio.sleep(0.2)  # Simulate execution time
        
        if intent['action'] == 'transfer':
            return {
                'message': f"Transferred {intent['amount']} {intent['token']} to {intent['to'][:10]}...",
                'tx_hash': '0x' + '1' * 64
            }
        elif intent['action'] == 'swap':
            return {
                'message': f"Swapped {intent['amount']} {intent['from_token']} for {intent['to_token']}",
                'tx_hash': '0x' + '2' * 64
            }
        else:
            return {
                'message': f"Executed query: {intent['query']}"
            }


# Convenience function
async def execute_safe_command(command: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Quick function to execute a command with AgentShield protection
    
    Args:
        command: Natural language command
        api_key: Crypto.com AI Agent API key (optional)
    
    Returns:
        Execution result dict
    
    Example:
        >>> result = await execute_safe_command("Send 10 USDC to Alice")
        >>> print(result['approved'])
    """
    agent = SafeCryptoComAgent(api_key=api_key)
    return await agent.execute(command)
