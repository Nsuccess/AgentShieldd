/**
 * AgentARC x402 Resource Service
 * 
 * A simple x402-compatible API that requires payment for access.
 * This demonstrates how AgentARC can protect AI agents accessing
 * paid resources on Cronos.
 */

import { Hono } from 'hono';
import { Facilitator, CronosNetwork, type PaymentRequirements } from '@crypto.com/facilitator-client';

const app = new Hono();

// Initialize Facilitator for Cronos Testnet
const facilitator = new Facilitator({
  network: (Bun.env.NETWORK || 'cronos-testnet') as CronosNetwork,
});

// In-memory storage for payment IDs (use Redis in production)
const payments = new Map<string, { paid: boolean; timestamp: number }>();

/**
 * Protected resource endpoint
 * Returns 402 if payment required, 200 if paid
 */
app.get('/api/protected-data', async (c) => {
  const paymentId = c.req.header('x-payment-id');
  
  // Check if payment already made
  if (paymentId && payments.get(paymentId)?.paid) {
    return c.json({
      ok: true,
      data: {
        message: 'Access granted! Here is your protected data.',
        timestamp: new Date().toISOString(),
        content: {
          market_data: {
            CRO_USD: 0.12,
            BTC_USD: 45000,
            ETH_USD: 2500,
          },
          ai_insights: [
            'Market sentiment: Bullish',
            'Recommended action: HOLD',
            'Risk level: Medium',
          ],
        },
      },
    });
  }
  
  // Payment required - return 402
  const newPaymentId = crypto.randomUUID();
  const paymentRequirements: PaymentRequirements = {
    scheme: 'exact',
    network: (Bun.env.NETWORK || 'cronos-testnet') as CronosNetwork,
    payTo: Bun.env.PAYMENT_RECIPIENT || '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',
    asset: Bun.env.USDC_ADDRESS || '0x9e0e7a0C8688b1A4e46b5F4D0A4F6B8F5C8E5D4C',
    maxAmountRequired: '1000000', // 1 USDC
    maxTimeoutSeconds: 300,
    description: 'Access to protected market data',
    mimeType: 'application/json',
    resource: '/api/protected-data',
    outputSchema: {},
    extra: {
      paymentId: newPaymentId,
    },
  };
  
  // Store payment ID
  payments.set(newPaymentId, { paid: false, timestamp: Date.now() });
  
  return c.json(
    {
      x402Version: 1,
      error: 'payment_required',
      message: 'Payment required to access this resource',
      accepts: [paymentRequirements],
    },
    402
  );
});

/**
 * Settlement endpoint
 * Verifies payment and marks as paid
 */
app.post('/api/pay', async (c) => {
  try {
    const requestBody = await c.req.json();
    const { paymentId, paymentHeader, paymentRequirements } = requestBody;
    
    if (!paymentId || !paymentHeader || !paymentRequirements) {
      return c.json({ error: 'Missing required fields' }, 400);
    }
    
    // Prepare body for Facilitator SDK
    const body = {
      x402Version: 1,
      paymentHeader,
      paymentRequirements,
    };
    
    // Step 1: Verify payment
    const verifyResult = await facilitator.verifyPayment(body);
    if (!verifyResult.isValid) {
      return c.json(
        {
          error: 'Payment verification failed',
          details: verifyResult,
        },
        400
      );
    }
    
    // Step 2: Settle payment
    const settleResult = await facilitator.settlePayment(body);
    
    if (settleResult.event === 'payment.settled') {
      // Mark payment as paid
      payments.set(paymentId, { paid: true, timestamp: Date.now() });
      
      return c.json({
        ok: true,
        paymentId,
        transactionHash: settleResult.txHash,
        message: 'Payment verified and settled',
      });
    } else {
      return c.json(
        {
          error: 'Payment settlement failed',
          details: settleResult,
        },
        400
      );
    }
  } catch (error) {
    console.error('Settlement error:', error);
    return c.json(
      {
        error: 'Settlement failed',
        details: error instanceof Error ? error.message : 'Unknown error',
      },
      500
    );
  }
});

/**
 * Health check endpoint
 */
app.get('/health', (c) => {
  return c.json({
    ok: true,
    service: 'AgentARC x402 Resource Service',
    network: Bun.env.NETWORK || 'cronos-testnet',
    timestamp: new Date().toISOString(),
  });
});

/**
 * Well-known endpoint for agent discovery (A2A protocol)
 */
app.get('/.well-known/agent-card', (c) => {
  return c.json({
    name: 'AgentARC Protected Data Service',
    description: 'AI-powered market data with AgentARC security validation',
    url: Bun.env.SERVICE_URL || 'http://localhost:3000',
    version: '1.0.0',
    resources: [
      {
        name: 'Protected Market Data',
        description: 'Real-time market data and AI insights',
        url: '/api/protected-data',
        paywall: {
          protocol: 'x402',
          settlement: '/api/pay',
          accepts: [
            {
              scheme: 'eip3009',
              network: Bun.env.NETWORK || 'cronos-testnet',
              asset: Bun.env.USDC_ADDRESS || '0x9e0e7a0C8688b1A4e46b5F4D0A4F6B8F5C8E5D4C',
              maxAmountRequired: '1000000',
            },
          ],
        },
      },
    ],
  });
});

// Start server
const port = parseInt(Bun.env.PORT || '3000');
console.log(`🚀 AgentARC x402 Resource Service starting on port ${port}...`);
console.log(`📡 Network: ${Bun.env.NETWORK || 'cronos-testnet'}`);
console.log(`💰 Payment recipient: ${Bun.env.PAYMENT_RECIPIENT || '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb'}`);
console.log(`\n✅ Server ready!`);
console.log(`   Health: http://localhost:${port}/health`);
console.log(`   Agent Card: http://localhost:${port}/.well-known/agent-card`);
console.log(`   Protected Data: http://localhost:${port}/api/protected-data\n`);

export default {
  port,
  fetch: app.fetch,
};
