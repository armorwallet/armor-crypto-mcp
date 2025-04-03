# Armor Crypto MCP
*Alpha Test version 0.1.2*

A single source for interating AI Agents with the Crypto ecosystem. This includes Wallet creatio and management, swaps, transfers, event based trades like DCA, stop loss and take profit and much more. The Armor MCP supports Solana in Alpha and when in beta will support more than a dozen blockchans including Ethereum. Base, Avalanche, Bitcoin, Sui, Berachain, megaETH, Optamism, Ton, BNB and Arbitrum among others. Using Armors' MCP you can bring all of crypto into your AI Agent with a unified logic and complete set of tools.
       
![Armor MCP](https://armor-assets-repository.s3.nl-ams.scw.cloud/armor_mcp.png)
<br />
<br />
<br />
<br />
<br />
<br />
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
<br />
<br />
![Armor MCP Diagram](https://armor-assets-repository.s3.nl-ams.scw.cloud/amor_mcp_diagram.png)
<br />
<br />
<br />
<br />
<br />
<br />
# Installation
```text
pip install armor-cryptp-mcp
```
<br />
<br />
<br />
<br />
<br />
<br />

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

## Installation
1. Make sure you have python installed
2. Run `pip install uv` in a terminal (command line interpreter)
3. Your agent software (Claude, etc.) will handle execution of the MCP server

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
<br />
<br />
<br />
<br />
<br />
<br />

# Installation in Claude Desktop
1. Must have Developer Mode enabled
2. Open Claude Desktop's File Menu top left of the window.
3. Go to File > Settings
4. Under Developer, click Edit Configuration
5. In the config file, insert the `armor-wallet-mcp` section from above
6. Make sure to replace the placeholder with your API key
7. Save the file and start a new Chat in Claude Desktop

## Installation in Cline
Coming soon

## Installation for n8n
1. Open the n8n app
2. Bottom-left of screen click `...` next to your username and click `Settings`
3. On the left panel, click `Community nodes` and then `Install a Community Node` button
4. In the search field for `npm Package Name` type in *mcp*
5. Install `MCP Nodes`
6. Add any MCP node, for example: `List Tools`
7. In the MCP Client `Parameters` tab, click `Select Credential` and click `Create new credential`
8. Under `Command` enter `uvx`
9. Under `Arguments` enter `armor-crypto-mcp`
10. Under `Environments` enter `ARMOR_API_KEY=eyJhbGciOiJIUzI1NiIsIn...` paste the full API Key value after the `=`
11. Back in the `Parameters` tab you can choose the MCP `Operation` for that Node
<br />
<br />
<br />
<br />
<br />
<br />
# Using Armor MCP

Once you have setup the Armor MCP [here are some prompts you can use to get started](https://github.com/armorwallet/armor-crypto-mcp/blob/main/README_prompts.md)
<br />
<br />
<br />
<br />
<br />
<br />
