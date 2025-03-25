# Armor Crypto MCP
Access blockchain, bridging, swapping, staking and crypto trading strategy for your Agent, all in one epic MCP.

```
     ..                         
  :**888H: `: .xH""                                                               
 X   `8888k XX888       .u    .      ..    .     :           u.      .u    .     
'8hx  48888 ?8888     .d88B :@8c   .888: x888  x888.   ...ue888b   .d88B :@8c    
'8888 '8888 `8888    ="8888f8888r ~`8888~'888X`?888f`  888R Y888r ="8888f8888r  
 %888>'8888  8888      4888>'88"    X888  888X '888>   888R I888>   4888>'88"     
   "8 '888"  8888      4888> '      X888  888X '888>   888R I888>   4888> '    
  .-` X*"    8888      4888>        X888  888X '888>   888R I888>   4888>       
    .xhx.    8888     .d888L .+     X888  888X '888>  u8888cJ888   .d888L .+    
  .H88888h.~`8888.>   ^"8888*"     "*88%""*88" '888!`  "*888*P"    ^"8888*"     
 .~  `%88!` '888*~       "Y"         `~    "    `"`      'Y"          "Y"       
       `"     ""                                                               

      ...    .     ...                        ..       ..                 s    
   .~`"888x.!**h.-``888h.               x .d88"  x .d88"                 :8    
  dX   `8888   :X   48888>               5888R    5888R                 .88    
 '888x  8888  X88.  '8888>        u      '888R    '888R        .u      :888ooo 
 '88888 8888X:8888:   )?""`    us888u.    888R     888R     ud8888.  -*8888888 
  `8888>8888 '88888>.88h.   .@88 "8888"   888R     888R   :888'8888.   8888    
    `8" 888f  `8888>X88888. 9888  9888    888R     888R   d888 '88%"   8888    
   -~` '8%"     88" `88888X 9888  9888    888R     888R   8888.+"      8888    
   .H888n.      XHn.  `*88! 9888  9888    888R     888R   8888L       .8888Lu= 
  :88888888x..x88888X.  `!  9888  9888   .888B .  .888B . '8888c. .+  ^%888*   
  f  ^%888888% `*88888nx"   "888*""888"  ^*888%   ^*888%   "88888%      'Y"    
      `"**"`    `"**""      ^Y"   ^Y'     "%       "%       "YP'              
                                                                                 
```
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