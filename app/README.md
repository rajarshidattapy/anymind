# MantleMemo: Built for Mantle Global Hackathon 2025

MantleMemo turns AI conversations into reusable intelligence coordinated on Mantle.  
Instead of fine-tuning models or rebuilding prompts, MantleMemo captures long-term agent memory and exposes it as permissioned, composable intelligence.

## What it does
- Wraps any stateless LLM with persistent memory
- Each LLM can have multiple isolated chats (memory capsules)
- Memory is reused across apps via API or SDK
- Intelligence stays off-chain; trust, access, and payments live on Mantle.

## Why Mantle
Mantle provides low-cost, high-frequency coordination for agent identity, access control, staking, and usage tracking.  
This makes intelligence portable, trustless, and composable across applications.

## Core Concepts
- **Agent**: Persistent identity that owns intelligence
- **Chat (Capsule)**: Isolated memory scope within an agent
- **Memory**: Semantic knowledge extracted from conversations
- **Runtime**: Injects memory into LLM calls without modifying the model

## 🚀 Web3 Integration

MantleMemo is now fully integrated with smart contracts on Mantle Sepolia Testnet:

### Smart Contract Features
- **Agent Registration**: On-chain agent identity and ownership
- **Capsule Creation**: Decentralized memory capsule marketplace
- **Staking System**: Stake MNT to signal capsule credibility (7-day lock period)
- **Query Payments**: Direct MNT payments for capsule access
- **Earnings Withdrawal**: Creators can withdraw earnings anytime
- **Transparent Economics**: All transactions verifiable on-chain

### Contract Address
**Mantle Sepolia**: `0x4287F8a28AC24FF1b0723D26747CBE7F39C9C167`

### How It Works
1. **Create Agent**: Register your AI agent identity on-chain
2. **Stake & List**: Stake MNT on your agent to create a marketplace capsule
3. **Earn from Queries**: Users pay MNT to query your capsule, you earn automatically
4. **Withdraw Earnings**: Pull your earnings from the smart contract anytime

## SDK Usage (Read-Only)
```python
from mantlememo import Agent

agent = Agent(
    agent_id="agent_123",
    chat_id="governance_chat",
)

response = agent.chat("Analyze proposal X")
````

## Architecture

* **Frontend**: React with MetaMask integration + Smart Contract UI
* **Smart Contract**: Solidity on Mantle Sepolia (Agent registry, staking, payments)
* **Runtime**: FastAPI
* **Chats & Messages**: Redis
* **Agents & Capsules**: PostgreSQL + Blockchain hybrid
* **Semantic Memory**: mem0 (off-chain)
* **Coordination Layer**: Mantle (EVM)

## Wallet & Payments

* **Wallet**: MetaMask (EVM-compatible)
* **Network**: Mantle Sepolia Testnet (Chain ID: 5003)
* **Token**: MNT (native gas token)
* **RPC**: https://rpc.sepolia.mantle.xyz
* **Explorer**: https://explorer.sepolia.mantle.xyz
* **Contract**: [View on Explorer](https://explorer.sepolia.mantle.xyz/address/0x4287F8a28AC24FF1b0723D26747CBE7F39C9C167)

## Getting Started

### Prerequisites
1. Install MetaMask browser extension
2. Add Mantle Sepolia Testnet to MetaMask
3. Get testnet MNT from [Mantle Faucet](https://faucet.sepolia.mantle.xyz/)

### Running the App
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Connect wallet and start creating agents!
```

### Web3 Features
- **Marketplace**: Browse and purchase AI memory capsules
- **Staking**: Stake MNT on your agents to list them
- **Earnings**: Track and withdraw your capsule earnings
- **Wallet**: View balance and transaction history

## What MantleMemo is NOT

* ❌ No model fine-tuning
* ❌ No raw data on-chain
* ❌ No prompt marketplace
* ❌ No AI inference on-chain

## Status

✅ **MVP Live**: Full Web3 integration with smart contracts on Mantle Sepolia Testnet  
✅ **Marketplace**: Decentralized capsule trading with MNT payments  
✅ **Staking**: Real MNT staking with lock periods and earnings  
✅ **SDK Access**: Persistent agent intelligence via API and SDK

