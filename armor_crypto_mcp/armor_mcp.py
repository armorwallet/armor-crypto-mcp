import os
from typing import List

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context


# Import base models
from .armor_client import (
    ArmorWalletAPIClient,
    WalletTokenBalance,
    ConversionResponse,
    SwapQuoteResponse,
    SwapTransactionResponse,
    Wallet,
    TokenDetailsResponse,
    GroupInfo,
    SingleGroupInfo,
    WalletInfo,
    WalletArchiveOrUnarchiveResponse,
    CreateGroupResponse,
    AddWalletToGroupResponse,
    GroupArchiveOrUnarchiveResponse,
    RemoveWalletFromGroupResponse,
    TransferTokenResponse,
    DCAOrderResponse,
    CancelDCAOrderResponse,
    ListSingleGroupRequest,
    WalletTokenPairsContainer,
    ConversionRequestContainer,
    SwapQuoteRequestContainer,
    SwapTransactionRequestContainer,
    TokenDetailsRequestContainer,
    TransferTokensRequestContainer,
    DCAOrderRequestContainer,
    CancelDCAOrderRequestContainer,
    CreateWalletRequestContainer,
    ArchiveWalletsRequestContainer,
    UnarchiveWalletRequestContainer,
    CreateGroupsRequestContainer,
    AddWalletToGroupRequestContainer,
    ArchiveWalletGroupRequestContainer,
    UnarchiveWalletGroupRequestContainer,
    RemoveWalletsFromGroupRequestContainer,
    CreateOrderRequestContainer,
    CancelOrderRequestContainer,
    CreateOrderResponseContainer,
    CancelOrderResponseContainer,
    StakeQuoteRequestContainer,
    UnstakeQuoteRequestContainer,
    StakeTransactionRequestContainer,
    UnstakeTransactionRequestContainer,
)

# Load environment variables (e.g. BASE_API_URL, etc.)
load_dotenv()

# Create an MCP server instance with FastMCP
mcp = FastMCP("Armor Crypto MCP")

# Global variable to hold the authenticated Armor API client
ACCESS_TOKEN = os.getenv('ARMOR_API_KEY') or os.getenv('ARMOR_ACCESS_TOKEN')
BASE_API_URL = os.getenv('ARMOR_API_URL') or 'https://app.armorwallet.ai/api/v1'

armor_client = ArmorWalletAPIClient(ACCESS_TOKEN, base_api_url=BASE_API_URL) #, log_path='armor_client.log')

# Include version endpoint
from armor_crypto_mcp import __version__
@mcp.tool()
async def get_armor_mcp_version():
    # return  __version__
    return {'armor_version': __version__}

@mcp.tool()
async def get_wallet_token_balance(wallet_token_pairs: WalletTokenPairsContainer) -> List[WalletTokenBalance]:
    """
    Get the balance for a list of wallet/token pairs.
    
    Expects a WalletTokenPairsContainer, returns a list of WalletTokenBalance.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[WalletTokenBalance] = await armor_client.get_wallet_token_balance(wallet_token_pairs)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def conversion_api(conversion_requests: ConversionRequestContainer) -> List[ConversionResponse]:
    """
    Perform token conversion.
    
    Expects a ConversionRequestContainer, returns a list of ConversionResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[ConversionResponse] = await armor_client.conversion_api(conversion_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def swap_quote(swap_quote_requests: SwapQuoteRequestContainer) -> List[SwapQuoteResponse]:
    """
    Retrieve a swap quote.
    
    Expects a SwapQuoteRequestContainer, returns a list of SwapQuoteResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[SwapQuoteResponse] = await armor_client.swap_quote(swap_quote_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def swap_transaction(swap_transaction_requests: SwapTransactionRequestContainer) -> List[SwapTransactionResponse]:
    """
    Execute a swap transaction.
    
    Expects a SwapTransactionRequestContainer, returns a list of SwapTransactionResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[SwapTransactionResponse] = await armor_client.swap_transaction(swap_transaction_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_all_wallets() -> List[Wallet]:
    """
    Retrieve all wallets with balances.
    
    Returns a list of Wallets and asssets
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[Wallet] = await armor_client.get_all_wallets()
        return result
    except Exception as e:
        return [{"error": str(e)}]
    

@mcp.tool()
async def get_all_orders() -> List:
    """
    Retrieve all limit and stop loss orders.
    
    Returns a list of orders.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List = await armor_client.get_all_orders()
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_token_details(token_details_requests: TokenDetailsRequestContainer) -> List[TokenDetailsResponse]:
    """
    Retrieve token details.
    
    Expects a TokenDetailsRequestContainer, returns a list of TokenDetailsResponse.
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
async def list_single_group(list_single_group_requests: ListSingleGroupRequest) -> SingleGroupInfo:
    """
    Retrieve details for a single wallet group.
    
    Expects the group name as a parameter, returns SingleGroupInfo.
    """
    if not armor_client:
        return {"error": "Not logged in"}
    try:
        result: SingleGroupInfo = await armor_client.list_single_group(list_single_group_requests)
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def create_wallet(create_wallet_requests: CreateWalletRequestContainer) -> List[WalletInfo]:
    """
    Create new wallets.
    
    Expects a list of wallet names, returns a list of WalletInfo.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[WalletInfo] = await armor_client.create_wallet(create_wallet_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def archive_wallets(archive_wallet_requests: ArchiveWalletsRequestContainer) -> List[WalletArchiveOrUnarchiveResponse]:
    """
    Archive wallets.
    
    Expects a list of wallet names, returns a list of WalletArchiveOrUnarchiveResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[WalletArchiveOrUnarchiveResponse] = await armor_client.archive_wallets(archive_wallet_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def unarchive_wallets(unarchive_wallet_requests: UnarchiveWalletRequestContainer) -> List[WalletArchiveOrUnarchiveResponse]:
    """
    Unarchive wallets.
    
    Expects a list of wallet names, returns a list of WalletArchiveOrUnarchiveResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[WalletArchiveOrUnarchiveResponse] = await armor_client.unarchive_wallets(unarchive_wallet_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def create_groups(create_groups_requests: CreateGroupsRequestContainer) -> List[CreateGroupResponse]:
    """
    Create new wallet groups.
    
    Expects a list of group names, returns a list of CreateGroupResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[CreateGroupResponse] = await armor_client.create_groups(create_groups_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def add_wallets_to_group(add_wallet_to_group_requests: AddWalletToGroupRequestContainer) -> List[AddWalletToGroupResponse]:
    """
    Add wallets to a specified group.
    
    Expects the group name and a list of wallet names, returns a list of AddWalletToGroupResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[AddWalletToGroupResponse] = await armor_client.add_wallets_to_group(add_wallet_to_group_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def archive_wallet_group(archive_wallet_group_requests: ArchiveWalletGroupRequestContainer) -> List[GroupArchiveOrUnarchiveResponse]:
    """
    Archive wallet groups.
    
    Expects a list of group names, returns a list of GroupArchiveOrUnarchiveResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[GroupArchiveOrUnarchiveResponse] = await armor_client.archive_wallet_group(archive_wallet_group_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def unarchive_wallet_group(unarchive_wallet_group_requests: UnarchiveWalletGroupRequestContainer) -> List[GroupArchiveOrUnarchiveResponse]:
    """
    Unarchive wallet groups.
    
    Expects a list of group names, returns a list of GroupArchiveOrUnarchiveResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[GroupArchiveOrUnarchiveResponse] = await armor_client.unarchive_wallet_group(unarchive_wallet_group_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def remove_wallets_from_group(remove_wallets_from_group_requests: RemoveWalletsFromGroupRequestContainer) -> List[RemoveWalletFromGroupResponse]:
    """
    Remove wallets from a specified group.
    
    Expects the group name and a list of wallet names, returns a list of RemoveWalletFromGroupResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[RemoveWalletFromGroupResponse] = await armor_client.remove_wallets_from_group(remove_wallets_from_group_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def transfer_tokens(transfer_tokens_requests: TransferTokensRequestContainer) -> List[TransferTokenResponse]:
    """
    Transfer tokens from one wallet to another.
    
    Expects a TransferTokensRequestContainer, returns a list of TransferTokenResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[TransferTokenResponse] = await armor_client.transfer_tokens(transfer_tokens_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def create_dca_order(dca_order_requests: DCAOrderRequestContainer) -> List[DCAOrderResponse]:
    """
    Create a DCA order.
    
    Expects a DCAOrderRequestContainer, returns a list of DCAOrderResponse.
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
async def cancel_dca_order(cancel_dca_order_requests: CancelDCAOrderRequestContainer) -> List[CancelDCAOrderResponse]:
    """
    Create a DCA order.

    Note: Make a single or multiple dca_order_requests 
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List[CancelDCAOrderResponse] = await armor_client.cancel_dca_order(cancel_dca_order_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]
    

@mcp.tool()
async def create_order(create_order_requests: CreateOrderRequestContainer) -> CreateOrderResponseContainer:
    """
    Create a order. Can be a limit or stop loss order
    
    Expects a CreateOrderRequestContainer, returns a CreateOrderResponseContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: CreateOrderResponseContainer = await armor_client.create_order(create_order_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]
    

@mcp.tool()
async def cancel_order(cancel_order_requests: CancelOrderRequestContainer) -> CancelOrderResponseContainer:
    """
    Cancel a limit or stop loss order.
    
    Expects a CancelOrderRequestContainer, returns a CancelOrderResponseContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: CancelOrderResponseContainer = await armor_client.cancel_order(cancel_order_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]
    

@mcp.tool()
async def stake_quote(stake_quote_requests: StakeQuoteRequestContainer) -> SwapQuoteRequestContainer:
    """
    Retrieve a stake quote.
    
    Expects a StakeQuoteRequestContainer, returns a SwapQuoteRequestContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: StakeQuoteRequestContainer = await armor_client.stake_quote(stake_quote_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def unstake_quote(unstake_quote_requests: UnstakeQuoteRequestContainer) -> SwapQuoteRequestContainer:
    """
    Retrieve an unstake quote.

    Expects a UnstakeQuoteRequestContainer, returns a SwapQuoteRequestContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: UnstakeQuoteRequestContainer = await armor_client.unstake_quote(unstake_quote_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def stake_transaction(stake_transaction_requests: StakeTransactionRequestContainer) -> SwapTransactionRequestContainer:
    """
    Execute a stake transaction.
    
    Expects a StakeTransactionRequestContainer, returns a SwapTransactionRequestContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: SwapTransactionRequestContainer = await armor_client.stake_transaction(stake_transaction_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def unstake_transaction(unstake_transaction_requests: UnstakeTransactionRequestContainer) -> SwapTransactionRequestContainer:
    """
    Execute an unstake transaction.
    
    Expects a UnstakeTransactionRequestContainer, returns a SwapTransactionRequestContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: SwapTransactionRequestContainer = await armor_client.unstake_transaction(unstake_transaction_requests)
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
