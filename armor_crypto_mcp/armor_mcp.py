import asyncio
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from armor_client import (
    ArmorWalletAPIClient,
    calculate,
    WalletTokenBalanceContainer,
    ConversionResponseContainer,
    SwapQuoteResponse,
    BridgeQuoteResponse,
    BridgeTransactionRequest,
    SwapTransactionRequest,
    SwapTransactionResponse,
    BridgeTransactionResponse,
    WalletContainer,
    TokenDetailsResponseContainer,
    GroupInfoContainer,
    SingleGroupInfo,
    WalletArchiveOrUnarchiveResponseContainer,
    CreateGroupResponseContainer,
    AddWalletToGroupResponseContainer,
    GroupArchiveOrUnarchiveResponseContainer,
    RemoveWalletFromGroupResponseContainer,
    TransferTokenResponse,
    DCAOrderResponseContainer,
    CancelDCAOrderResponseContainer,
    ListSingleGroupRequest,
    TopTrendingTokensRequestSolana,
    TopTrendingTokensRequestCoinMarketCap,
    CandleStickRequest,
    ListWalletsRequest,
    ListSingleWalletRequest,
    ListDCAOrderRequest,
    ListOrderRequest,
    PrivateKeyRequest,
    TokenSearchPromptRequest,
    TokenSearchGraphQLQueryRequest,
    CreateWalletResponse,
    BridgeStatusResponse,
    BridgeStatusRequest,
    WalletTokenPairsContainer,
    ConversionRequestContainer,
    SwapQuoteRequest,
    SwapTransactionRequest,
    WrapUnwrapTokensRequest,
    ListChainRequest,
    BridgeQuoteRequest,
    TransferTokensRequest,
    TokenDetailsRequestContainer,
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
    RenameWalletRequestContainer,
    ListDCAOrderResponseContainer,
    ListOrderResponseContainer,
    ListChainsResponseContainer,
)

# Load environment variables (e.g. BASE_API_URL, etc.)
load_dotenv()

# Create an MCP server instance with FastMCP
mcp = FastMCP("Armor Crypto MCP")

# Global variable to hold the authenticated Armor API client
ACCESS_TOKEN = os.getenv("ARMOR_API_KEY") or os.getenv("ARMOR_ACCESS_TOKEN")
BASE_API_URL = os.getenv("ARMOR_API_URL") or "https://app.armorwallet.ai/api/v1"

armor_client = ArmorWalletAPIClient(
    ACCESS_TOKEN, base_api_url=BASE_API_URL
)  # , log_path='armor_client.log')

# Include version endpoint
from armor_crypto_mcp import __version__


@mcp.tool()
async def get_armor_mcp_version():
    """Get the current Armor Wallet version"""
    return {"armor_version": __version__}


@mcp.tool()
async def wait_a_moment(seconds: float):
    """Wait for some short amount of time, no more than 10 seconds"""
    await asyncio.sleep(seconds)
    return {"waited": seconds}


from datetime import datetime, timezone


@mcp.tool()
async def get_current_time() -> Dict:
    """Gets the current time and date"""
    return {"current_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")}


@mcp.tool()
async def calculator(expression: str, variables: dict[str, Any]):
    """
    Safely evaluates a mathematical or statistical expression string using Python syntax.

    Supports arithmetic operations (+, -, *, /, **, %, //), list expressions, and a range of math and statistics functions:
    abs, round, min, max, len, sum, mean, median, stdev, variance, sin, cos, tan, sqrt, log, exp, floor, ceil, etc.

    Custom variables can be passed via the 'variables' dict, including lists for time series data.
    """
    return {"result": calculate(expression, variables)}


@mcp.tool()
async def get_wallet_token_balance(
    wallet_token_pairs: WalletTokenPairsContainer,
) -> WalletTokenBalanceContainer | Any:
    """
    Get the balance for a list of wallet/token pairs.

    Expects a WalletTokenPairsContainer, returns a WalletTokenBalanceContainer.
    """
    if not armor_client:
        return {"error": "Not logged in"}
    try:
        result: WalletTokenBalanceContainer | Any = (
            await armor_client.get_wallet_token_balance(wallet_token_pairs)
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def calculate_token_conversion(
    conversion_requests: ConversionRequestContainer,
) -> ConversionResponseContainer | Any:
    """
    Perform token conversion quote between two tokens. Good for quickly calculating market prices and token conversions.

    Expects a ConversionRequestContainer, returns a ConversionResponseContainer.
    """
    if not armor_client:
        return {"error": "Not logged in"}
    try:
        result: ConversionResponseContainer | Any = await armor_client.conversion_api(
            conversion_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def swap_quote(
    swap_quote_requests: SwapQuoteRequest,
) -> SwapQuoteResponse | Any:
    """
    Retrieve a swap quote.

    Expects a SwapQuoteRequest, returns a SwapQuoteResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: SwapQuoteResponse | Any = await armor_client.swap_quote(
            swap_quote_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def swap_transaction(
    swap_transaction_requests: SwapTransactionRequest,
) -> SwapTransactionResponse | Any:
    """
    Execute a swap transaction.

    Expects a SwapTransactionRequest, returns a SwapTransactionResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: SwapTransactionResponse | Any = await armor_client.swap_transaction(
            swap_transaction_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def bridge_quote(
    bridge_quote_requests: BridgeQuoteRequest,
) -> BridgeQuoteResponse | Any:
    """
    Retrieve a bridge quote.

    Expects a BridgeQuoteRequest, returns a BridgeQuoteResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: BridgeQuoteResponse | Any = await armor_client.bridge_quote(
            bridge_quote_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def bridge_transaction(
    bridge_transaction_requests: BridgeTransactionRequest,
) -> BridgeTransactionResponse | Any:
    """
    Execute a bridge transaction.

    Expects a BridgeTransactionRequest, returns a BridgeTransactionResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: BridgeTransactionResponse | Any = await armor_client.bridge_transaction(
            bridge_transaction_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_bridge_transaction_status(
    bridge_status_request: BridgeStatusRequest,
) -> BridgeStatusResponse | Any:
    """
    Get the status of a bridge transaction.

    Expects a BridgeStatusResponse, returns a BridgeStatusResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: BridgeStatusResponse | Any = (
            await armor_client.get_bridge_transaction_status(bridge_status_request)
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_all_wallets(
    get_all_wallets_requests: ListWalletsRequest,
) -> WalletContainer | Any:
    """
    Retrieve all wallets with balances. For single wallet details, always use get_single_wallet_details.

    Returns a WalletContainer with Wallets and assets
    """
    if not armor_client:
        return {"error": "Not logged in"}
    try:
        result: WalletContainer | Any = await armor_client.get_all_wallets(
            get_all_wallets_requests
        )
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def get_single_wallet_details(
    get_single_wallet_details_requests: ListSingleWalletRequest,
) -> WalletContainer | Any:
    """
    Retrieve details for a single wallet

    Expects a ListSingleWalletRequest, returns a WalletContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: WalletContainer | Any = await armor_client.get_single_wallet_details(
            get_single_wallet_details_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_all_orders(
    get_all_orders_requests: ListOrderRequest,
) -> ListOrderResponseContainer | Any:
    """
    Retrieve all limit, take profit and stop loss orders.

    Returns a list of orders.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: ListOrderResponseContainer | Any = await armor_client.list_orders(
            get_all_orders_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def list_chains(
    list_chains_requests: ListChainRequest,
) -> ListChainsResponseContainer | Any:
    """
    List chains along with their chain id and gas token.
    Try to enter the chain name or slug to get details of only specific chains.
    Only get data of all chains if needed.

    Expects a ListChainRequest, returns a ListChainsResponseContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: ListChainsResponseContainer | Any = await armor_client.list_chains(
            list_chains_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def search_official_token_address(
    token_details_requests: TokenDetailsRequestContainer,
) -> TokenDetailsResponseContainer | Any:
    """
    Get the official token address and symbol for a token symbol or token address.
    Try to use this first to get address and symbol of coin. If not found, use search_token_details to get details.
    If user has not provided a chain id, use this tool without the chain id as it will return a reliable token.

    Expects a TokenDetailsRequestContainer, returns a TokenDetailsResponseContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: TokenDetailsResponseContainer | Any = (
            await armor_client.get_official_token_address(token_details_requests)
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_instructions_to_generate_graphql_query_token_search(
    token_search_prompt_request: TokenSearchPromptRequest,
) -> Dict | Any:
    """
    Get instructions to generate a graphql query for a token search.

    Expects a TokenSearchPromptRequest, returns a dictionary with the instructions.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        with open(
            os.path.join(os.path.dirname(__file__), "instructions/filter_tokens.md"),
            "r",
        ) as f:
            prompt = f.read().replace("{user_query}", token_search_prompt_request.query)
        return {"graphql_query_generation_instructions": prompt}
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def search_token_details(
    token_search_graphql_query: TokenSearchGraphQLQueryRequest,
) -> Dict | Any:
    """
    Search and retrieve details about single token.
    If only address or symbol is needed, use get_official_token_address first.

    Expects a TokenSearchGraphQLQueryRequest, returns a Dict.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: Dict | Any = await armor_client.search_token(token_search_graphql_query)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def list_groups() -> GroupInfoContainer | Any:
    """
    List all wallet groups.

    Returns a GroupInfoContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: GroupInfoContainer | Any = await armor_client.list_groups()
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def list_single_group(
    list_single_group_requests: ListSingleGroupRequest,
) -> SingleGroupInfo | Any:
    """
    Retrieve details for a single wallet group.

    Expects the group name as a parameter, returns SingleGroupInfo.
    """
    if not armor_client:
        return {"error": "Not logged in"}
    try:
        result: SingleGroupInfo | Any = await armor_client.list_single_group(
            list_single_group_requests
        )
        return result
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def create_wallet(
    create_wallet_requests: CreateWalletRequestContainer,
) -> CreateWalletResponse | Any:
    """
    Create new wallets.

    Expects a list of wallet names, returns a CreateWalletResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: CreateWalletResponse | Any = await armor_client.create_wallet(
            create_wallet_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def archive_wallets(
    archive_wallet_requests: ArchiveWalletsRequestContainer,
) -> WalletArchiveOrUnarchiveResponseContainer | Any:
    """
    Archive wallets.

    Expects a list of wallet names, returns a WalletArchiveOrUnarchiveResponseContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: WalletArchiveOrUnarchiveResponseContainer | Any = (
            await armor_client.archive_wallets(archive_wallet_requests)
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def unarchive_wallets(
    unarchive_wallet_requests: UnarchiveWalletRequestContainer,
) -> WalletArchiveOrUnarchiveResponseContainer | Any:
    """
    Unarchive wallets.

    Expects a list of wallet names, returns a WalletArchiveOrUnarchiveResponseContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: WalletArchiveOrUnarchiveResponseContainer | Any = (
            await armor_client.unarchive_wallets(unarchive_wallet_requests)
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def create_groups(
    create_groups_requests: CreateGroupsRequestContainer,
) -> CreateGroupResponseContainer | Any:
    """
    Create new wallet groups.

    Expects a list of group names, returns a CreateGroupResponseContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: CreateGroupResponseContainer | Any = await armor_client.create_groups(
            create_groups_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def add_wallets_to_group(
    add_wallet_to_group_requests: AddWalletToGroupRequestContainer,
) -> AddWalletToGroupResponseContainer | Any:
    """
    Add wallets to a specified group.

    Expects the group name and a list of wallet names, returns an AddWalletToGroupResponseContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: AddWalletToGroupResponseContainer | Any = (
            await armor_client.add_wallets_to_group(add_wallet_to_group_requests)
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def archive_wallet_group(
    archive_wallet_group_requests: ArchiveWalletGroupRequestContainer,
) -> GroupArchiveOrUnarchiveResponseContainer | Any:
    """
    Archive wallet groups.

    Expects a list of group names, returns a GroupArchiveOrUnarchiveResponseContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: GroupArchiveOrUnarchiveResponseContainer | Any = (
            await armor_client.archive_wallet_group(archive_wallet_group_requests)
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def unarchive_wallet_group(
    unarchive_wallet_group_requests: UnarchiveWalletGroupRequestContainer,
) -> GroupArchiveOrUnarchiveResponseContainer | Any:
    """
    Unarchive wallet groups.

    Expects a list of group names, returns a GroupArchiveOrUnarchiveResponseContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: GroupArchiveOrUnarchiveResponseContainer | Any = (
            await armor_client.unarchive_wallet_group(unarchive_wallet_group_requests)
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def remove_wallets_from_group(
    remove_wallets_from_group_requests: RemoveWalletsFromGroupRequestContainer,
) -> RemoveWalletFromGroupResponseContainer | Any:
    """
    Remove wallets from a specified group.

    Expects the group name and a list of wallet names, returns a RemoveWalletFromGroupResponseContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: RemoveWalletFromGroupResponseContainer | Any = (
            await armor_client.remove_wallets_from_group(
                remove_wallets_from_group_requests
            )
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def transfer_tokens(
    transfer_tokens_requests: TransferTokensRequest,
) -> TransferTokenResponse | Any:
    """
    Transfer tokens from one wallet to another.

    Expects a TransferTokensRequestContainer, returns a list of TransferTokenResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: TransferTokenResponse | Any = await armor_client.transfer_tokens(
            transfer_tokens_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def create_dca_order(
    dca_order_requests: DCAOrderRequestContainer,
) -> DCAOrderResponseContainer | Any:
    """
    Create a DCA order.
    Only add watch_field if the user specifies a conditional DCA.
    Make sure you enter the correct token amount. Use `calculate_token_conversion` to do the necessary conversions if necessary.

    Expects a DCAOrderRequestContainer, returns a DCAOrderResponseContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: DCAOrderResponseContainer | Any = await armor_client.create_dca_order(
            dca_order_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def list_dca_orders(
    list_dca_order_requests: ListDCAOrderRequest,
) -> ListDCAOrderResponseContainer | Any:
    """
    List all DCA orders.

    Returns a list of DCAOrderResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: ListDCAOrderResponseContainer | Any = (
            await armor_client.list_dca_orders(list_dca_order_requests)
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def cancel_dca_order(
    cancel_dca_order_requests: CancelDCAOrderRequestContainer,
) -> CancelDCAOrderResponseContainer | Any:
    """
    Create a DCA order.

    Note: Make a single or multiple dca_order_requests
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: CancelDCAOrderResponseContainer | Any = (
            await armor_client.cancel_dca_order(cancel_dca_order_requests)
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def create_order(
    create_order_requests: CreateOrderRequestContainer,
) -> CreateOrderResponseContainer | Any:
    """
    Create a order. Can be a limit, take profit, stop loss, trailing stop, trailing buy or Low Base Breakout Buy-LBBB(always a trailing buy order).

    Expects a CreateOrderRequestContainer, returns a CreateOrderResponseContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: CreateOrderResponseContainer | Any = await armor_client.create_order(
            create_order_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def cancel_order(
    cancel_order_requests: CancelOrderRequestContainer,
) -> CancelOrderResponseContainer | Any:
    """
    Cancel a limit, take profit or stop loss order.

    Expects a CancelOrderRequestContainer, returns a CancelOrderResponseContainer.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: CancelOrderResponseContainer | Any = await armor_client.cancel_order(
            cancel_order_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_top_trending_tokens_for_solana(
    top_trending_tokens_requests: TopTrendingTokensRequestSolana,
) -> List | Any:
    """
    Get the top trending tokens in a particular time frame for the solana/SVM chain. Great for comparing market cap or volume.

    Expects a TopTrendingTokensRequest, returns a list of tokens with their details.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List | Any = await armor_client.top_trending_tokens_for_solana(
            top_trending_tokens_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_top_trending_tokens_coinmarketcap(
    top_trending_tokens_requests: TopTrendingTokensRequestCoinMarketCap,
) -> List | Any:
    """
    Get the top trending tokens in a particular time frame for CoinMarketCap. Great for comparing market cap or volume.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List | Any = await armor_client.top_trending_tokens_for_coinmarketcap(
            top_trending_tokens_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def rename_wallets(
    rename_wallet_requests: RenameWalletRequestContainer,
) -> List | Any:
    """
    Rename wallets.

    Expects a RenameWalletRequestContainer, returns a list.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List | Any = await armor_client.rename_wallet(rename_wallet_requests)
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def get_token_candle_data(
    candle_stick_requests: CandleStickRequest,
) -> List | Any:
    """
    Get candle data about any token for analysis.

    Expects a CandleStickRequest, returns a list of candle sticks.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: List | Any = await armor_client.get_market_candle_data(
            candle_stick_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def wrap_quote(
    wrap_tokens_requests: WrapUnwrapTokensRequest,
) -> SwapQuoteResponse | Any:
    """
    Generates a quote for wrapping the tokens. Converts the gas token to the wrapped token.

    Expects a WrapUnwrapTokensRequest, returns SwapQuoteResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: SwapQuoteResponse | Any = await armor_client.wrap_tokens(
            wrap_tokens_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def unwrap_quote(
    unwrap_tokens_requests: WrapUnwrapTokensRequest,
) -> SwapQuoteResponse | Any:
    """
    Generates a quote for unwrapping the tokens. Converts the wrapped tokens to the gas token.

    Expects a WrapUnwrapTokensRequest, returns SwapQuoteResponse.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: SwapQuoteResponse | Any = await armor_client.unwrap_tokens(
            unwrap_tokens_requests
        )
        return result
    except Exception as e:
        return [{"error": str(e)}]


@mcp.prompt()
def login_prompt(email: str) -> str:
    """
    A sample prompt to ask the user for their access token after providing an email.
    """
    return f"Please enter the Access token for your account {email}."


@mcp.tool()
async def send_key_to_telegram(private_key_request: PrivateKeyRequest) -> Dict:
    """
    Send the mnemonic or private key to telegram.
    """
    if not armor_client:
        return [{"error": "Not logged in"}]
    try:
        result: Dict = await armor_client.send_key_to_telegram(private_key_request)
        return result
    except Exception as e:
        return [{"error": str(e)}]


def main():
    mcp.run()


if __name__ == "__main__":
    main()
