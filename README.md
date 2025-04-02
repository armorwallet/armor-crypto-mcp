# Armor Crypto MCP
*Alpha Test version 0.1.2*

A single source for interating AI Agents with the Crypto ecosystem. This includes Wallet creatio and management, swaps, transfers, event based trades like DCA, stop loss and take profit and much more. The Armor MCP supports Solana in Alpha and when in beta will support more than a dozen blockchans including Ethereum. Base, Avalanche, Bitcoin, Sui, Berachain, megaETH, Optamism, Ton, BNB and Arbitrum among others. Using Armors' MCP you can bring all of crypto into your AI Agent with a unified logic and complete set of tools.
       
![Armor MCP](https://armor-assets-repository.s3.nl-ams.scw.cloud/armor_mcp.png)
\
\
\
# Features

🧠 AI Native

📙 Wallet Management

🔃 Swaps

🌈 Specialized trades (DCA, Stop Loss etc.)

⛓️ Multi-chain

↔️ Cross-chain transations

🥩 Staking

🤖 Fast intergration to Agentic frameworks

👫 Social Sentiment

🔮 Prediction
\
\
\
# Installation
```text
pip install armor-cryptp-mcp
```
\
\
\
# Alpha Testing

We are currently in pre-alpha, and we are testing the capabilities of various agents and agentic frameworks like Claude Desktop, Cline, Cursor, n8n, etc. 

## Current Features & Tools
- Wallet Management
    - Grouping & Organization
    - Archiving
- Swap & Trades
    - DCA
    - Limit Orders
- Supports Solana blockchain

## Coming Soon
- Staking
- Armor Agents as a Tool
- More Blockchain Support

## MCP Setup
Currently you need to have the Armor NFT to get an API Key.
Get it [here](https://codex.armorwallet.ai/)

## Usage & Configuration
To use the Armor MCP with your agent, you need the following configuration:
```json
{
  "mcpServers": {
    "armor-crypto-mcp": {
      "command": "uvx",
      "args": ["armor-crypto-mcp"],
      "env": {
        "ARMOR_API_KEY": "<PUT-YOUR-KEY-HERE>"
      }
    }
  }
}
```
\
\
\
# Installation in Claude Desktop (must have Developer Mode enabled)
1. Open Claude Desktop's File Menu top left of the window.
2. Go to File > Settings
3. Under Developer, click Edit Configuration
4. In the config file, insert the `armor-wallet-mcp` section from above
5. Make sure to replace the placeholder with your API key
6. Save the file and start a new Chat in Claude Desktop

## Installation in Cline
Coming soon

## Installation for n8n
Coming soon
\
\
\
# Using Armor MCP
Once you have setup the Armor MCP [here are some prompts you can use to get started](https://github.com/armorwallet/armor-crypto-mcp/blob/main/README_prompts.md).

