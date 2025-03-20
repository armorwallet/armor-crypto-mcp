import logging
import logging.handlers
import os
import gzip
from typing import List, Optional, TypedDict, Literal, Any, Dict
# from typing_extensions import TypedDict
from mcp.server.fastmcp import FastMCP, Context, Image
from mcp.types import TextContent, ImageContent, EmbeddedResource
from armor_client import ArmorWalletAPIClient, WalletTokenPairs, ConversionRequest, SwapQuoteRequest, SwapTransactionRequest, TokenDetailsRequest, TransferTokensRequest, DCAOrderRequest, CancelDCAOrderRequest

# Set up logging
def setup_logging():
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logger = logging.getLogger("ArmorMCP")
    logger.setLevel(logging.INFO)

    # Create a rotating file handler that rotates logs every day and keeps 7 days of logs
    file_handler = logging.handlers.TimedRotatingFileHandler(
        os.path.join(log_directory, "armor_mcp.log"),
        when="midnight",
        interval=1,
        backupCount=7
    )
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Compress log files on rotation
    def namer(name):
        return name + ".gz"

    def rotator(source, dest):
        with open(source, "rb") as f_in:
            with gzip.open(dest, "wb") as f_out:
                f_out.writelines(f_in)
        os.remove(source)

    file_handler.rotator = rotator
    file_handler.namer = namer

    # Add a console handler for real-time logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = setup_logging()

# Initialize the FastMCP server
mcp = FastMCP("ArmorMCP")

# Initialize the ArmorWalletAPIClient
armor_client = None

@mcp.tool()
async def login(email: str, password: str, ctx: Context) -> str:
    """Log in to the wallet API."""
    global armor_client
    armor_client = ArmorWalletAPIClient("")
    result = await armor_client.login(email, password)
    return f"Logged in successfully. Access token: {result['access']}"

@mcp.tool()
async def get_wallet_token_balance(wallet_token_pairs: List[WalletTokenPairs], ctx: Context) -> str:
    """Get balances from a list of wallet and token pairs."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.get_wallet_token_balance(wallet_token_pairs)
    return str(result)

@mcp.tool()
async def conversion_api(conversion_request: List[ConversionRequest], ctx: Context) -> str:
    """Perform a token conversion."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.conversion_api(conversion_request)
    return str(result)

@mcp.tool()
async def swap_quote(swap_quote_requests: List[SwapQuoteRequest], ctx: Context) -> str:
    """Obtain a swap quote."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.swap_quote(swap_quote_requests)
    return str(result)

@mcp.tool()
async def swap_transaction(swap_transaction_requests: List[SwapTransactionRequest], ctx: Context) -> str:
    """Execute the swap transactions."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.swap_transaction(swap_transaction_requests)
    return str(result)

@mcp.resource("wallets://group/{group_name}")
async def get_wallets_from_group(group_name: str, ctx: Context) -> str:
    """Return the list of wallet names from the specified group."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.get_wallets_from_group(group_name)
    return str(result)

@mcp.resource("wallets://all")
async def get_all_wallets(ctx: Context) -> str:
    """Return all wallets with balances."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.get_all_wallets()
    return str(result)

@mcp.tool()
async def get_token_details(token_details_requests: List[TokenDetailsRequest], ctx: Context) -> str:
    """Retrieve token details."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.get_token_details(token_details_requests)
    return str(result)

@mcp.resource("groups://all")
async def list_groups(ctx: Context) -> str:
    """Return a list of wallet groups."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.list_groups()
    return str(result)

@mcp.resource("groups://{group_name}")
async def list_single_group(group_name: str, ctx: Context) -> str:
    """Return details for a single wallet group."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.list_single_group(group_name)
    return str(result)

@mcp.tool()
async def create_wallet(wallet_names_list: List[str], ctx: Context) -> str:
    """Create new wallets given a list of wallet names."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.create_wallet(wallet_names_list)
    return str(result)

@mcp.tool()
async def archive_wallets(wallet_names_list: List[str], ctx: Context) -> str:
    """Archive the wallets specified in the list."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.archive_wallets(wallet_names_list)
    return str(result)

@mcp.tool()
async def unarchive_wallets(wallet_names_list: List[str], ctx: Context) -> str:
    """Unarchive the wallets specified in the list."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.unarchive_wallets(wallet_names_list)
    return str(result)

@mcp.tool()
async def create_groups(group_names_list: List[str], ctx: Context) -> str:
    """Create new wallet groups given a list of group names."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.create_groups(group_names_list)
    return str(result)

@mcp.tool()
async def add_wallets_to_group(group_name: str, wallet_names_list: List[str], ctx: Context) -> str:
    """Add wallets to a specific group."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.add_wallets_to_group(group_name, wallet_names_list)
    return str(result)

@mcp.tool()
async def archive_wallet_group(group_names_list: List[str], ctx: Context) -> str:
    """Archive the specified wallet groups."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.archive_wallet_group(group_names_list)
    return str(result)

@mcp.tool()
async def unarchive_wallet_group(group_names_list: List[str], ctx: Context) -> str:
    """Unarchive the specified wallet groups."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.unarchive_wallet_group(group_names_list)
    return str(result)

@mcp.tool()
async def remove_wallets_from_group(group_name: str, wallet_names_list: List[str], ctx: Context) -> str:
    """Remove wallets from a group."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.remove_wallets_from_group(group_name, wallet_names_list)
    return str(result)

@mcp.resource("user://wallets_and_groups")
async def get_user_wallets_and_groups_list(ctx: Context) -> str:
    """Return user wallets and groups."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.get_user_wallets_and_groups_list()
    return str(result)

@mcp.tool()
async def transfer_tokens(transfer_tokens_requests: List[TransferTokensRequest], ctx: Context) -> str:
    """Transfer tokens from one wallet to another."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.transfer_tokens(transfer_tokens_requests)
    return str(result)

@mcp.tool()
async def create_dca_order(dca_order_requests: List[DCAOrderRequest], ctx: Context) -> str:
    """Create a DCA order."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.create_dca_order(dca_order_requests)
    return str(result)

@mcp.resource("dca_orders://all")
async def list_dca_orders(ctx: Context) -> str:
    """List all DCA orders."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.list_dca_orders()
    return str(result)

@mcp.tool()
async def cancel_dca_order(cancel_dca_order_requests: List[CancelDCAOrderRequest], ctx: Context) -> str:
    """Cancel a DCA order."""
    if armor_client is None:
        return "Please log in first."
    result = await armor_client.cancel_dca_order(cancel_dca_order_requests)
    return str(result)

if __name__ == "__main__":
    mcp.run(transport='stdio')
