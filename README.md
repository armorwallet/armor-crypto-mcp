# Armor Crypto MCP
Access blockchain, bridging, swapping, staking and crypto trading strategy for your Agent, all in one epic MCP.
       
![Armor MCP]([https://armor-assets-repository.s3.nl-ams.scw.cloud/armor_mcp.png])

## Alpha Testing
We are currently in pre-alpha, and we are testing the capabilities of various agents like Claude Desktop, Cline, Cursor, n8n, etc. 

## Current Features & Tools
- Wallet Management
    - Grouping & Organization
    - 
- Swap & Trades
    - DCA
    - Limit Orders
- Bridge

## Coming Soon
- Staking
- Armor Agents as a Tool

## How Armor Crypto MCP Might be Used
Here are some example prompts that we have been testing with our internal Armor Agents, but could use testing with other agents. Think of this MCP as the bridge to a large number of cryptocurrency ecosystems. Each tool we provide your agent can be combined with other tools to form powerful chains of action.

### Wallet Management
- Creating wallets
```
Create a wallet named test2 and transfer 0.2 SOL to it from test1
```
- Wallet organization
```
Put wallets test1 and test2 into a new group called testing
```
```
List my wallet groups
```
- Archiving wallets
```
Move all of my assets from test3 to test1 and archive test3
```

### DCA and Swaps
- Simple DCA
```
DCA into SOL from 20% of my USDc
```
- Specific DCA
```
Buy SOL with all of my USD in test1 wallet over a period of 3 months, place the orders at midnight every monday and thursday
```
- Placing Orders
```
Buy 0.12 BTC with my SOL at 10% below current market price
```
```
Get out of SOL now!
```
```
Put a stop loss on all my altcoin positions in test2 wallet
```
- Cancelling Orders
```
Cancel all my open orders
```
```
Cancel all my buy orders below 5% of the current market price in SOL
```

### Helpful Notes
- The more specific you are, the more control you can have over whatever strategy you want.
- It will help if you ask for the current state of your assets to better plan what to do.
- All agents are not created equally, and won't use tools in the same way.
- If your agent has Thinking mode or capability, try using that for a boost.
- Talk to your agent about strategy before commanding it to do something.
- None of this is financial advice.

## How to Access
Currently you need to have the armor NFT to get an API Key. More instructions coming soon.

## Usage & Configuration
To use the Armor MCP with your agent, you need the following configuration:
```json
{
  "mcpServers": {
    "armor-wallet-mcp": {
      "command": "uvx",
      "args": ["armor-wallet-mcp"],
      "env": {
        "ARMOR_API_KEY": "<PUT-YOUR-KEY-HERE>"
      }
    }
  }
}
```

## Installation in Claude Desktop (must have Developer Mode enabled)
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
