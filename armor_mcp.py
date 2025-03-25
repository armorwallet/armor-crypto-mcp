import os
import json
import logging
from typing import List, Dict, Any

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context

# Import the ArmorWalletAPIClient from your client module.
# Ensure that the file with the Armor API client code is in your PYTHONPATH.
from armor_client import ArmorWalletAPIClient

# Load environment variables (e.g. BASE_API_URL, etc.)
load_dotenv()

# Configure persistent logging (logs will be saved to armor_api_server.log)
logging.basicConfig(
    level=logging.INFO,
    filename="armor_api_server.log",
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create an MCP server instance with FastMCP
mcp = FastMCP("Armor API Server")

# Global variable to hold the authenticated Armor API client
# armor_client: ArmorWalletAPIClient | None = None
ACCESS_TOKEN = os.getenv('ARMOR_ACCESS_TOKEN')
BASE_API_URL = os.getenv('ARMOR_API_URL')

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
        logger.info("Retrieved wallet token balances.")
        return result
    except Exception as e:
        logger.exception("Error in get_wallet_token_balance")
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
        logger.info("Conversion API executed successfully.")
        return result
    except Exception as e:
        logger.exception("Error in conversion_api")
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
        logger.info("Swap quote retrieved successfully.")
        return result
    except Exception as e:
        logger.exception("Error in swap_quote")
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
        logger.info("Swap transaction executed successfully.")
        return result
    except Exception as e:
        logger.exception("Error in swap_transaction")
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
        logger.info("Retrieved all wallets successfully.")
        return result
    except Exception as e:
        logger.exception("Error in get_all_wallets")
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
        logger.info("Token details retrieved successfully.")
        return result
    except Exception as e:
        logger.exception("Error in get_token_details")
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
        logger.info("Wallet groups retrieved successfully.")
        return result
    except Exception as e:
        logger.exception("Error in list_groups")
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
        logger.info(f"Details for group '{group_name}' retrieved successfully.")
        return result
    except Exception as e:
        logger.exception("Error in list_single_group")
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
        logger.info("Wallets created successfully.")
        return result
    except Exception as e:
        logger.exception("Error in create_wallet")
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
        logger.info("Wallets archived successfully.")
        return result
    except Exception as e:
        logger.exception("Error in archive_wallets")
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
        logger.info("Wallets unarchived successfully.")
        return result
    except Exception as e:
        logger.exception("Error in unarchive_wallets")
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
        logger.info("Groups created successfully.")
        return result
    except Exception as e:
        logger.exception("Error in create_groups")
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
        logger.info(f"Wallets added to group '{group_name}' successfully.")
        return result
    except Exception as e:
        logger.exception("Error in add_wallets_to_group")
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
        logger.info("Wallet groups archived successfully.")
        return result
    except Exception as e:
        logger.exception("Error in archive_wallet_group")
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
        logger.info("Wallet groups unarchived successfully.")
        return result
    except Exception as e:
        logger.exception("Error in unarchive_wallet_group")
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
        logger.info(f"Wallets removed from group '{group_name}' successfully.")
        return result
    except Exception as e:
        logger.exception("Error in remove_wallets_from_group")
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
        logger.info("User wallets and groups retrieved successfully.")
        return result
    except Exception as e:
        logger.exception("Error in get_user_wallets_and_groups_list")
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
        logger.info("Tokens transferred successfully.")
        return result
    except Exception as e:
        logger.exception("Error in transfer_tokens")
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
        logger.info("DCA order created successfully.")
        return result
    except Exception as e:
        logger.exception("Error in create_dca_order")
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
        logger.info("DCA orders listed successfully.")
        return result
    except Exception as e:
        logger.exception("Error in list_dca_orders")
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
        logger.info("DCA order cancelled successfully.")
        return result
    except Exception as e:
        logger.exception("Error in cancel_dca_order")
        return [{"error": str(e)}]


@mcp.prompt()
def login_prompt(email: str) -> str:
    """
    A sample prompt to ask the user for their password after providing an email.
    This prompt is intended to be surfaced as a UI element.
    """
    return f"Please enter the Access token for your account {email}."


# To run the server:
if __name__ == "__main__":
    mcp.run()
