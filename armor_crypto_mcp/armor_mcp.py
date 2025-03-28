import os
import json
import logging
from typing import List, Dict, Any

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context

# Import the ArmorWalletAPIClient from your client module.
from .armor_client import ArmorWalletAPIClient

# Load environment variables (e.g. BASE_API_URL, etc.)
load_dotenv()

# Create an MCP server instance with FastMCP
mcp = FastMCP("Armor Crypto MCP")

# Global variable to hold the authenticated Armor API client
ACCESS_TOKEN = os.getenv('ARMOR_ACCESS_TOKEN')
BASE_API_URL = os.getenv('ARMOR_API_URL') or None

armor_client = ArmorWalletAPIClient(ACCESS_TOKEN, base_api_url=BASE_API_URL)


@mcp.tool()
async def get_wallet_token_balance(wallet_token_pairs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Get the balance for a list of wallet/token pairs.
    
    Expects a list of dictionaries each with 'wallet' and 'token' keys.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.get_wallet_token_balance(wallet_token_pairs)
        
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def conversion_api(conversion_requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Perform token conversion.
    
    Expects a list of conversion requests with keys: input_amount, input_token, output_token.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.conversion_api(conversion_requests)
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.tool()
async def swap_quote(swap_quote_requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Retrieve a swap quote.
    
    Expects a list of swap quote requests.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.swap_quote(swap_quote_requests)
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.tool()
async def swap_transaction(swap_transaction_requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Execute a swap transaction.
    
    Expects a list of swap transaction requests.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.swap_transaction(swap_transaction_requests)
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.resource("wallets://all")
async def get_all_wallets() -> List[Dict[str, Any]]:
    """
    Retrieve all wallets with balances.
    
    This is a resource endpoint intended for read-only operations.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.get_all_wallets()
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


# Additional MCP Tools for Armor API Endpoints

@mcp.tool()
async def get_token_details(token_details_requests: list[dict]) -> list[dict]:
    """
    Retrieve token details.
    
    Expects a list of token details requests with keys such as 'query' and 'include_details'.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.get_token_details(token_details_requests)
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.tool()
async def list_groups() -> list[dict]:
    """
    List all wallet groups.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.list_groups()
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.tool()
async def list_single_group(group_name: str) -> dict:
    """
    Retrieve details for a single wallet group.
    
    Expects the group name as a parameter.
    """
    if not armor_client:
        return {"error": "Not logged in"}
    try:
        result = await armor_client.list_single_group(group_name)
        
        return result
    except Exception as e:
        
        return {"error": str(e)}


@mcp.tool()
async def create_wallet(wallet_names_list: list[str]) -> list[dict]:
    """
    Create new wallets.
    
    Expects a list of wallet names.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.create_wallet(wallet_names_list)
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.tool()
async def archive_wallets(wallet_names_list: list[str]) -> list[dict]:
    """
    Archive wallets.
    
    Expects a list of wallet names.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.archive_wallets(wallet_names_list)
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.tool()
async def unarchive_wallets(wallet_names_list: list[str]) -> list[dict]:
    """
    Unarchive wallets.
    
    Expects a list of wallet names.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.unarchive_wallets(wallet_names_list)
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.tool()
async def create_groups(group_names_list: list[str]) -> list[dict]:
    """
    Create new wallet groups.
    
    Expects a list of group names.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.create_groups(group_names_list)
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.tool()
async def add_wallets_to_group(group_name: str, wallet_names_list: list[str]) -> list[dict]:
    """
    Add wallets to a specified group.
    
    Expects the group name and a list of wallet names.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.add_wallets_to_group(group_name, wallet_names_list)
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.tool()
async def archive_wallet_group(group_names_list: list[str]) -> list[dict]:
    """
    Archive wallet groups.
    
    Expects a list of group names.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.archive_wallet_group(group_names_list)
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.tool()
async def unarchive_wallet_group(group_names_list: list[str]) -> list[dict]:
    """
    Unarchive wallet groups.
    
    Expects a list of group names.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.unarchive_wallet_group(group_names_list)
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.tool()
async def remove_wallets_from_group(group_name: str, wallet_names_list: list[str]) -> list[dict]:
    """
    Remove wallets from a specified group.
    
    Expects the group name and a list of wallet names.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.remove_wallets_from_group(group_name, wallet_names_list)
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.tool()
async def get_user_wallets_and_groups_list() -> dict:
    """
    Retrieve the list of user wallets and wallet groups.
    """
    if not armor_client:
        return {"error": "Not logged in"}
    try:
        result = await armor_client.get_user_wallets_and_groups_list()
        
        return result
    except Exception as e:
        
        return {"error": str(e)}


@mcp.tool()
async def transfer_tokens(transfer_tokens_requests: list[dict]) -> list[dict]:
    """
    Transfer tokens from one wallet to another.
    
    Expects a list of transfer token requests with the necessary parameters.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.transfer_tokens(transfer_tokens_requests)
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.tool()
async def create_dca_order(dca_order_requests: list[dict]) -> list[dict]:
    """
    Create a DCA order.
    
    Expects a list of DCA order requests with required parameters.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.create_dca_order(dca_order_requests)
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.tool()
async def list_dca_orders() -> list[dict]:
    """
    List all DCA orders.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.list_dca_orders()
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.tool()
async def cancel_dca_order(cancel_dca_order_requests: list[dict]) -> list[dict]:
    """
    Cancel a DCA order.
    
    Expects a list of cancel DCA order requests with the required order IDs.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result = await armor_client.cancel_dca_order(cancel_dca_order_requests)
        
        return result
    except Exception as e:
        
        return [{"error": str(e)}]


@mcp.prompt()
def login_prompt(email: str) -> str:
    """
    A sample prompt to ask the user for their password after providing an email.
    This prompt is intended to be surfaced as a UI element.
    """
    return f"Please enter the Access token for your account {email}."


def main():
    mcp.run()
    
if __name__ == "__main__":
    main()