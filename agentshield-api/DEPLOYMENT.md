# AgentShield API Deployment Guide

## Option 1: Railway (Recommended - Easiest)

### Prerequisites
- GitHub account
- Railway account (free tier available)

### Steps

1. **Push code to GitHub**
```bash
git add agentshield-api/
git commit -m "Add AgentShield API service"
git push origin main
```

2. **Deploy to Railway**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect the Dockerfile

3. **Configure Environment**
   - Add environment variables (optional):
     - `ETHEREUM_RPC`
     - `BASE_RPC`
     - `CRONOS_TESTNET_RPC`

4. **Get URL**
   - Railway will provide a URL like: `https://agentshield-api.up.railway.app`
   - Copy this URL for Loofta Pay integration

### Cost
- Free tier: 500 hours/month (enough for hackathon)
- Paid: $5/month for unlimited

---

## Option 2: Render

### Steps

1. **Push to GitHub** (same as above)

2. **Create Web Service**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo

3. **Configure Build**
   - **Build Command**: 
     ```bash
     pip install -r requirements-hackathon.txt && pip install -r agentshield-api/requirements.txt
     ```
   - **Start Command**:
     ```bash
     cd agentshield-api && uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

4. **Environment Variables**
   - Add RPC URLs as needed

5. **Deploy**
   - Render will build and deploy
   - Get URL: `https://agentshield-api.onrender.com`

### Cost
- Free tier: Available (with spin-down after inactivity)
- Paid: $7/month for always-on

---

## Option 3: Vercel (Serverless)

### Steps

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Create vercel.json**
```json
{
  "builds": [
    {
      "src": "agentshield-api/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "agentshield-api/main.py"
    }
  ]
}
```

3. **Deploy**
```bash
vercel --prod
```

### Cost
- Free tier: 100GB bandwidth/month
- Paid: $20/month for more

---

## Option 4: Local Development

### For testing only

```bash
# Install dependencies
pip install -r agentshield-api/requirements.txt

# Run server
cd agentshield-api
python main.py
```

Server runs on `http://localhost:8000`

---

## Testing Deployment

Once deployed, test with:

```bash
# Replace with your deployment URL
export API_URL="https://agentshield-api.railway.app"

# Test health
curl $API_URL/health

# Test validation
curl -X POST $API_URL/validate-token \
  -H "Content-Type: application/json" \
  -d '{
    "token_address": "0x6001B76e8CeA99a749F591ed6E1cE7a704CF231b",
    "chain": "cronos-testnet",
    "amount": "1.0"
  }'
```

Expected response:
```json
{
  "is_safe": false,
  "risk_level": "HIGH",
  "reason": "Token cannot be sold (honeypot detected)",
  ...
}
```

---

## Next Steps

After deployment:
1. Copy your API URL
2. Add to Loofta Pay `.env.local`:
   ```
   AGENTSHIELD_API_URL=https://your-api-url.railway.app
   ```
3. Continue with Loofta Pay integration (Step 2)
