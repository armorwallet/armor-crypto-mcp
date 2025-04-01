import os
import json
import logging
from typing import List, Dict, Any

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context

# Import the ArmorWalletAPIClient and types from your client module.
from .armor_client import (
    ArmorWalletAPIClient,
    WalletTokenPairs,
    WalletTokenBalance,
    ConversionRequest,
    ConversionResponse,
    SwapQuoteRequest,
    SwapQuoteResponse,
    SwapTransactionRequest,
    SwapTransactionResponse,
    Wallet,
    TokenDetailsRequest,
    TokenDetailsResponse,
    GroupInfo,
    SingleGroupInfo,
    WalletInfo,
    WalletArchiveOrUnarchiveResponse,
    CreateGroupResponse,
    AddWalletToGroupResponse,
    GroupArchiveOrUnarchiveResponse,
    RemoveWalletFromGroupResponse,
    UserWalletsAndGroupsResponse,
    TransferTokensRequest,
    TransferTokenResponse,
    DCAOrderRequest,
    DCAOrderResponse,
    CancelDCAOrderRequest,
    CancelDCAOrderResponse
)

# Load environment variables (e.g. BASE_API_URL, etc.)
load_dotenv()

# Create an MCP server instance with FastMCP
mcp = FastMCP("Armor Crypto MCP")

# Global variable to hold the authenticated Armor API client
ACCESS_TOKEN = os.getenv('ARMOR_API_KEY') or os.getenv('ARMOR_ACCESS_TOKEN')
BASE_API_URL = os.getenv('ARMOR_API_URL') or 'https://app.armorwallet.ai/api/v1'

armor_client = ArmorWalletAPIClient(ACCESS_TOKEN, base_api_url=BASE_API_URL)


@mcp.tool()
async def get_wallet_token_balance(wallet_token_pairs: List[WalletTokenPairs]) -> List[WalletTokenBalance]:
    """
    Get the balance for a list of wallet/token pairs.
    
    Expects a list of WalletTokenPairs, returns a list of WalletTokenBalance.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[WalletTokenBalance] = await armor_client.get_wallet_token_balance(wallet_token_pairs)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def conversion_api(conversion_requests: List[ConversionRequest]) -> List[ConversionResponse]:
    """
    Perform token conversion.
    
    Expects a list of ConversionRequest, returns a list of ConversionResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[ConversionResponse] = await armor_client.conversion_api(conversion_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def swap_quote(swap_quote_requests: List[SwapQuoteRequest]) -> List[SwapQuoteResponse]:
    """
    Retrieve a swap quote.
    
    Expects a list of SwapQuoteRequest, returns a list of SwapQuoteResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[SwapQuoteResponse] = await armor_client.swap_quote(swap_quote_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def swap_transaction(swap_transaction_requests: List[SwapTransactionRequest]) -> List[SwapTransactionResponse]:
    """
    Execute a swap transaction.
    
    Expects a list of SwapTransactionRequest, returns a list of SwapTransactionResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[SwapTransactionResponse] = await armor_client.swap_transaction(swap_transaction_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.resource("wallets://all")
async def get_all_wallets() -> List[Wallet]:
    """
    Retrieve all wallets with balances.
    
    Returns a list of Wallet.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[Wallet] = await armor_client.get_all_wallets()
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_token_details(token_details_requests: List[TokenDetailsRequest]) -> List[TokenDetailsResponse]:
    """
    Retrieve token details.
    
    Expects a list of TokenDetailsRequest, returns a list of TokenDetailsResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[TokenDetailsResponse] = await armor_client.get_token_details(token_details_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def list_groups() -> List[GroupInfo]:
    """
    List all wallet groups.
    
    Returns a list of GroupInfo.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[GroupInfo] = await armor_client.list_groups()
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def list_single_group(group_name: str) -> SingleGroupInfo:
    """
    Retrieve details for a single wallet group.
    
    Expects the group name as a parameter, returns SingleGroupInfo.
    """
    if not armor_client:
        return {"error": "Not logged in"}
    try:
        result: SingleGroupInfo = await armor_client.list_single_group(group_name)
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def create_wallet(wallet_names_list: List[str]) -> List[WalletInfo]:
    """
    Create new wallets.
    
    Expects a list of wallet names, returns a list of WalletInfo.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[WalletInfo] = await armor_client.create_wallet(wallet_names_list)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def archive_wallets(wallet_names_list: List[str]) -> List[WalletArchiveOrUnarchiveResponse]:
    """
    Archive wallets.
    
    Expects a list of wallet names, returns a list of WalletArchiveOrUnarchiveResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[WalletArchiveOrUnarchiveResponse] = await armor_client.archive_wallets(wallet_names_list)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def unarchive_wallets(wallet_names_list: List[str]) -> List[WalletArchiveOrUnarchiveResponse]:
    """
    Unarchive wallets.
    
    Expects a list of wallet names, returns a list of WalletArchiveOrUnarchiveResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[WalletArchiveOrUnarchiveResponse] = await armor_client.unarchive_wallets(wallet_names_list)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def create_groups(group_names_list: List[str]) -> List[CreateGroupResponse]:
    """
    Create new wallet groups.
    
    Expects a list of group names, returns a list of CreateGroupResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[CreateGroupResponse] = await armor_client.create_groups(group_names_list)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def add_wallets_to_group(group_name: str, wallet_names_list: List[str]) -> List[AddWalletToGroupResponse]:
    """
    Add wallets to a specified group.
    
    Expects the group name and a list of wallet names, returns a list of AddWalletToGroupResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[AddWalletToGroupResponse] = await armor_client.add_wallets_to_group(group_name, wallet_names_list)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def archive_wallet_group(group_names_list: List[str]) -> List[GroupArchiveOrUnarchiveResponse]:
    """
    Archive wallet groups.
    
    Expects a list of group names, returns a list of GroupArchiveOrUnarchiveResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[GroupArchiveOrUnarchiveResponse] = await armor_client.archive_wallet_group(group_names_list)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def unarchive_wallet_group(group_names_list: List[str]) -> List[GroupArchiveOrUnarchiveResponse]:
    """
    Unarchive wallet groups.
    
    Expects a list of group names, returns a list of GroupArchiveOrUnarchiveResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[GroupArchiveOrUnarchiveResponse] = await armor_client.unarchive_wallet_group(group_names_list)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def remove_wallets_from_group(group_name: str, wallet_names_list: List[str]) -> List[RemoveWalletFromGroupResponse]:
    """
    Remove wallets from a specified group.
    
    Expects the group name and a list of wallet names, returns a list of RemoveWalletFromGroupResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[RemoveWalletFromGroupResponse] = await armor_client.remove_wallets_from_group(group_name, wallet_names_list)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_user_wallets_and_groups_list() -> UserWalletsAndGroupsResponse:
    """
    Retrieve the list of user wallets and wallet groups.
    
    Returns UserWalletsAndGroupsResponse.
    """
    if not armor_client:
        return {"error": "Not logged in"}
    try:
        result: UserWalletsAndGroupsResponse = await armor_client.get_user_wallets_and_groups_list()
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def transfer_tokens(transfer_tokens_requests: List[TransferTokensRequest]) -> List[TransferTokenResponse]:
    """
    Transfer tokens from one wallet to another.
    
    Expects a list of TransferTokensRequest, returns a list of TransferTokenResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[TransferTokenResponse] = await armor_client.transfer_tokens(transfer_tokens_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def create_dca_order(dca_order_requests: List[DCAOrderRequest]) -> List[DCAOrderResponse]:
    """
    Create a DCA order.
    
    Expects a list of DCAOrderRequest, returns a list of DCAOrderResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[DCAOrderResponse] = await armor_client.create_dca_order(dca_order_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def list_dca_orders() -> List[DCAOrderResponse]:
    """
    List all DCA orders.
    
    Returns a list of DCAOrderResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[DCAOrderResponse] = await armor_client.list_dca_orders()
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def cancel_dca_order(cancel_dca_order_requests: List[CancelDCAOrderRequest]) -> List[CancelDCAOrderResponse]:
    """
    Cancel a DCA order.
    
    Expects a list of CancelDCAOrderRequest, returns a list of CancelDCAOrderResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[CancelDCAOrderResponse] = await armor_client.cancel_dca_order(cancel_dca_order_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.prompt()
def login_prompt(email: str) -> str:
    """
    A sample prompt to ask the user for their access token after providing an email.
    """
    return f"Please enter the Access token for your account {email}."


def main():
    mcp.run()
    
if __name__ == "__main__":
    main()
