# Armor Crypto MCP
Access blockchain, bridging, swapping, and crypto trading strategy for your Agent, all in one epic MCP.

## Current Organization and Important Files
Currently this repo is not very organized, working on organizing it. Here's a breakdown of what each file is:
- [source.md](source.md): The source prompt for getting any model to attempt coding the MCP
- [armor_client.py](armor_client.py): The direct Armor Client that calls the Armor service
- [build.py](build.py): Builds a draft of the armor mcp server using `source.md` and a model setting
- [armor_mcp.py](armor_mcp.py): The MCP server which wraps the `armor_client`
- [servers_config.json](servers_config.json): The configuration setup that needs to be included in Claude Desktop, Cline, etc. (your agent software) to use Armor MCP
 
## TODO
3. Testing
    - Get the proper CORS situation going
    - Make sure telegram access key flow works
    - Make sure key flow on any given agent works (env var setup?)
4. put on scaleways
5. register with uvx and all the others

