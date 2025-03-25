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

## Current Features & Tools
- Wallet Management
- Swap & Trades
- Bridge

## Coming Soon
- Staking
- Armor Agents

## How to access

## Usage & Configuration
To use the Armor MCP with your agent, you need the following configuration:
```json
{
  "mcpServers": {
    "armor-wallet-mcp": {
      "command": "uvx",
      "args": ["armor-wallet-mcp"],
      "env": {
        "ARMOR_ACCESS_TOKEN": "<PUT-YOUR-TOKEN-HERE>"
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