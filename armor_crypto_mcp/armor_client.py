import json
import os
from pydantic import BaseModel, Field
from typing_extensions import List, Optional, Literal, Dict, Any, Union
from uuid import UUID
import httpx
from dotenv import load_dotenv


import ast
import operator
import math
import statistics

load_dotenv()
BASE_API_URL = os.getenv("BASE_API_URL")

# ------------------------------
# BaseModel Definitions
# ------------------------------


class WalletTokenPairs(BaseModel):
    name: str = Field(description="The name of wallet")
    token: str = Field(
        description="public address of token. To get the address from a token symbol use `get_token_details`"
    )
    chain_id: Optional[UUID] = Field(
        description="chain id of the wallet. If not provided, wallets on all chains will be returned. \
            If you want to get wallets on a specific chain, you can use the chain id from `list_chains`"
    )


class WalletTokenBalance(BaseModel):
    wallet: str = Field(description="name of wallet")
    token: str = Field(description="public address of token")
    balance: float = Field(description="balance of token")


class ConversionRequest(BaseModel):
    chain_id: UUID = Field(
        description="chain id to generate the conversion quote on. Use `list_chains` to get the chain id."
    )
    input_amount: float = Field(description="input amount to convert")
    input_token_address: str = Field(description="public address of input token")
    output_token_address: str = Field(description="public address of output token")


class ConversionResponse(BaseModel):
    input_amount: float = Field(description="input amount before conversion")
    input_token_address: str = Field(description="public address of input token")
    output_token_address: str = Field(description="public address of output token")
    output_amount: float = Field(description="output amount after conversion")


class SwapQuoteRequest(BaseModel):
    wallet: str = Field(description="The name of the wallet that input_token is in.")
    input_chain_id: UUID = Field(
        description="chain id to generate the swap quote on. Use `list_chains` to get the chain id."
    )
    input_token: str = Field(
        description="token address of input token. To get the address from a token symbol use `get_token_details`"
    )
    output_token: str = Field(
        description="token address of output token. To get the address from a token symbol use `get_token_details`"
    )
    input_amount: float = Field(description="input amount to swap")
    slippage: Optional[float] = Field(
        default=None,
        description="only include slippage in the request if user specifies. never add slippage by yourself.",
    )


class BridgeQuoteRequest(BaseModel):
    wallet: str = Field(description="The name of the wallet that input_token is in.")
    input_chain_id: UUID = Field(
        description="chain id of the input token. Use `list_chains` to get the chain id."
    )
    output_chain_id: UUID = Field(
        description="chain id of the output token. Use `list_chains` to get the chain id."
    )
    input_token: str = Field(
        description="token address of input token. To get the address from a token symbol use `get_token_details`"
    )
    output_token: str = Field(
        description="token address of output token. To get the address from a token symbol use `get_token_details`"
    )
    input_amount: float = Field(description="input amount to bridge")
    slippage: Optional[float] = Field(
        description="only include slippage in the request if user specifies. never add slippage by yourself."
    )


class SwapQuoteResponse(BaseModel):
    id: str = Field(description="unique id of the generated swap quote")
    wallet_address: str = Field(description="public address of the wallet")
    input_token_symbol: str = Field(description="symbol of the input token")
    input_token_address: str = Field(description="public address of the input token")
    output_token_symbol: str = Field(description="symbol of the output token")
    output_token_address: str = Field(description="public address of the output token")
    input_amount: float = Field(description="input amount in input token")
    output_amount: float = Field(description="output amount in output token")
    slippage: float = Field(description="slippage percentage.")


class BridgeQuoteResponse(BaseModel):
    id: str = Field(description="unique id of the generated bridge quote")
    wallet_address: str = Field(description="public address of the wallet")
    input_token_symbol: str = Field(description="symbol of the input token")
    input_token_address: str = Field(description="public address of the input token")
    output_token_symbol: str = Field(description="symbol of the output token")
    output_token_address: str = Field(description="public address of the output token")
    input_amount: float = Field(description="input amount in input token")
    output_amount: float = Field(description="output amount in output token")
    slippage: float = Field(description="slippage percentage.")


class BridgeTransactionRequest(BaseModel):
    transaction_id: str = Field(description="unique id of the generated bridge quote")


class SwapTransactionRequest(BaseModel):
    transaction_id: str = Field(description="unique id of the generated swap quote")


class SwapTransactionResponse(BaseModel):
    id: str = Field(description="unique id of the swap transaction")
    transaction_error: Optional[str] = Field(
        description="error message if the transaction fails"
    )
    transaction_url: str = Field(description="public url of the transaction")
    input_amount: float = Field(description="input amount in input token")
    output_amount: float = Field(description="output amount in output token")
    status: str = Field(description="status of the transaction")


class BridgeTransactionResponse(BaseModel):
    id: str = Field(description="unique id of the bridge transaction")
    transaction_error: Optional[str] = Field(
        description="error message if the transaction fails"
    )
    transaction_url: str = Field(description="public url of the transaction")
    input_amount: float = Field(description="input amount in input token")
    output_amount: float = Field(description="output amount in output token")
    status: str = Field(description="status of the transaction")


class ListWalletsRequest(BaseModel):
    chain_ids: Optional[List[UUID]] = Field(
        description="list of chain ids to get wallets for. \
            If chain_ids is not provided, wallets on all chains will be returned. \
            If you want to get wallets on a specific chain, you can use the chain id from `list_chains`."
    )
    show_archive: bool = Field(
        default=False,
        description="if True, only archived wallets will be returned. If False, only non-archived wallets will be returned.",
    )


class ListSingleWalletRequest(BaseModel):
    name: str = Field(description="name of the wallet to get details for")
    chain_id: UUID = Field(
        description="chain id of the wallet. If not provided, wallets on all chains will be returned. \
            If you want to get wallets on a specific chain, you can use the chain id from `list_chains`"
    )


class WalletBalance(BaseModel):
    mint_address: str = Field(
        description="token address of output token. To get the address from a token symbol use `get_token_details`"
    )
    name: str = Field(description="name of the token")
    symbol: str = Field(description="symbol of the token")
    decimals: int = Field(description="number of decimals of the token")
    amount: float = Field(description="balance of the token")
    usd_price: str = Field(description="price of the token in USD")
    usd_amount: float = Field(description="balance of the token in USD")


class WalletInfo(BaseModel):
    id: str = Field(description="wallet id")
    name: str = Field(description="wallet name")
    is_archived: bool = Field(description="whether the wallet is archived")
    public_address: str = Field(description="public address of the wallet")


class TokenInfo(BaseModel):
    name: str
    symbol: str


class TokenBalance(BaseModel):
    balanceUsd: Union[float, str]
    tokenPriceUsd: Union[float, str]
    tokenAddress: str
    shiftedBalance: float
    token: TokenInfo
    networkId: Optional[int] = None
    isGasToken: bool = Field(description="whether the token is the gas token")


class ChainWalletBalance(BaseModel):
    is_archived: bool = Field(description="whether the wallet is archived")
    public_address: str = Field(description="public address of the wallet")
    chain_type: str = Field(description="type of the chain")
    balances: Dict[str, List[TokenBalance]] = Field(
        description="balances of the wallet"
    )


class Wallet(BaseModel):
    balances: Dict[str, List[ChainWalletBalance]]


class TokenDetailsRequest(BaseModel):
    query: str = Field(description="token symbol or address")
    chain_id: Optional[UUID] = Field(
        description="chain id of the token. Always use your context or `list_chains` to get the chain id."
    )


class TokenDetailsResponse(BaseModel):
    symbol: str = Field(description="symbol of the token")
    mint_address: str = Field(description="token address of the token")
    image_url: str = Field(description="image url of the token")
    chain: str = Field(description="chain of the token")


class GroupInfo(BaseModel):
    id: str = Field(description="id of the group")
    name: str = Field(description="name of the group")
    is_archived: bool = Field(description="whether the group is archived")


class SingleGroupInfo(GroupInfo):
    wallets: List[WalletInfo] = Field(description="list of wallets in the group")


class WalletArchiveOrUnarchiveResponse(BaseModel):
    wallet_name: str = Field(description="name of the wallet")
    message: str = Field(
        description="message of the operation showing if wallet was archived or unarchived"
    )


class CreateGroupResponse(BaseModel):
    id: str = Field(description="id of the group")
    name: str = Field(description="name of the group")
    is_archived: bool = Field(description="whether the group is archived")


class AddWalletToGroupResponse(BaseModel):
    wallet_name: str = Field(description="name of the wallet to add to the group")
    group_name: str = Field(description="name of the group to add the wallet to")
    message: str = Field(
        description="message of the operation showing if wallet was added to the group"
    )


class GroupArchiveOrUnarchiveResponse(BaseModel):
    group: str = Field(description="name of the group")


class RemoveWalletFromGroupResponse(BaseModel):
    wallet: str = Field(description="name of the wallet to remove from the group")
    group: str = Field(description="name of the group to remove the wallet from")


class UserWalletsAndGroupsResponse(BaseModel):
    id: str = Field(description="id of the user")
    email: str = Field(description="email of the user")
    first_name: str = Field(description="first name of the user")
    last_name: str = Field(description="last name of the user")
    slippage: float = Field(description="slippage set by the user")
    wallet_groups: List[GroupInfo] = Field(description="list of user's wallet groups")
    wallets: List[WalletInfo] = Field(description="list of user's wallets")


class TransferTokensRequest(BaseModel):
    wallet: str = Field(description="name of the wallet to transfer tokens from")
    to_wallet_address: str = Field(
        description="public address of the wallet to transfer tokens to"
    )
    token: str = Field(
        description="public contract address of the token to transfer. To get the address from a token symbol use `get_token_details`"
    )
    amount: float = Field(description="amount of tokens to transfer")
    chain: Optional[UUID] = Field(
        description="chain id of the token. Always use your context or `list_chains` to get the chain id."
    )


class TransferTokenResponse(BaseModel):
    amount: float = Field(description="amount of tokens transferred")
    from_wallet_address: str = Field(
        description="public address of the wallet tokens were transferred from"
    )
    to_wallet_address: str = Field(
        description="public address of the wallet tokens were transferred to"
    )
    token_address: str = Field(description="public address of the token transferred")
    transaction_url: str = Field(description="public url of the transaction")
    message: str = Field(
        description="message of the operation showing if tokens were transferred"
    )


class ListDCAOrderRequest(BaseModel):
    status: Optional[Literal["COMPLETED", "OPEN", "CANCELLED"]] = Field(
        description="status of the DCA orders, if specified filters the results."
    )
    limit: Optional[int] = Field(
        default=30, description="number of most recent results to return"
    )


class DCAOrderRequest(BaseModel):
    wallet: str = Field(description="public address of the wallet")
    input_token: str = Field(
        description="public address of the input token you want to sell. To get the address from a token symbol use `get_token_details`"
    )
    output_token: str = Field(
        description="public address of the output token you want to buy. To get the address from a token symbol use `get_token_details`"
    )
    input_chain_id: UUID = Field(description="chain id of the input token")
    output_chain_id: UUID = Field(description="chain id of the output token")
    total_amount: float = Field(
        description="total amount of input token to invest. Make sure you enter the correct amount. Use `calculate_token_conversion` to do the necessary conversions."
    )
    cron_expression: Optional[str] = Field(
        description="cron expression for the DCA worker execution frequency. If you are using order_time_interval and number_of_orders, this field should be None"
    )
    interval_time: Optional[int] = Field(
        description="amount of time between each order. If you are using cron_expression, this field should be None"
    )
    interval_time_unit: Optional[Literal["DAY", "HOUR", "MINUTE", "SECOND"]] = Field(
        description="interval time unit for the DCA order. If you are using cron_expression, this field should be None"
    )
    order_amount: Optional[float] = Field(
        description="amount of input token to invest per order."
    )
    strategy_duration_unit: Literal[
        "MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "YEAR"
    ] = Field(description="unit of the duration of the DCA order")
    strategy_duration: int = Field(
        description="Total running time of the DCA order given in strategy duration units, should be more than 0"
    )
    execution_type: Literal["MULTIPLE", "SINGLE"] = Field(
        description="set to SINGLE only if the user is asking for a single scheduled order, MULTIPLE if it is a true DCA"
    )
    token_address_watcher: Optional[str] = Field(
        description="If the DCA is conditional, public address of the token to watch."
    )
    token_watcher_chain_id: Optional[UUID] = Field(
        description="chain id of the token to watch"
    )
    watch_field: Optional[Literal["liquidity", "marketCap", "price"]] = Field(
        description="If the DCA is conditional, field to watch for the condition"
    )
    delta_type: Optional[
        Literal["INCREASE", "DECREASE", "MOVE", "MOVE_DAILY", "AVERAGE_MOVE"]
    ] = Field(
        description="If the DCA is conditional, the operator of the watch field in the conditional statement"
    )
    delta_percentage: Optional[float] = Field(
        description="If the DCA is conditional, percentage of the change to watch for given the delta_type"
    )
    time_zone: Optional[str] = Field(description="user's time zone. Defaults to UTC")


class DCAWatcher(BaseModel):
    watch_field: Literal["liquidity", "marketCap", "price"] = Field(
        description="field to watch for the DCA order"
    )
    delta_type: Literal[
        "INCREASE", "DECREASE", "MOVE", "MOVE_DAILY", "AVERAGE_MOVE"
    ] = Field(description="type of the delta")
    initial_value: float = Field(description="initial value of the delta")
    delta_percentage: float = Field(description="percentage of the delta")


class TokenData(BaseModel):
    name: str = Field(description="name of the token")
    symbol: str = Field(description="symbol of the token")
    mint_address: str = Field(description="token address of the token")


class DCAOrderResponse(BaseModel):
    id: str = Field(description="id of the DCA order")
    amount: float = Field(description="amount of tokens to invest")
    investment_per_order: float = Field(
        description="amount of tokens to invest per order"
    )
    orders_completed: int = Field(description="number of orders completed")
    total_orders: int = Field(description="total number of orders")
    human_readable_expiry: str = Field(
        description="human readable expiry date of the DCA order"
    )
    status: str = Field(description="status of the DCA order")
    input_token_data: TokenData = Field(description="details of the input token")
    output_token_data: TokenData = Field(description="details of the output token")
    wallet_name: str = Field(description="name of the wallet")
    watchers: List[DCAWatcher] = Field(description="list of watchers for the DCA order")
    dca_transactions: List[dict] = Field(
        description="list of DCA transactions"
    )  # Can be further typed if structure is known
    created: str = Field(description="Linux timestamp of the creation of the order")


class ListOrderRequest(BaseModel):
    status: Optional[
        Literal["OPEN", "CANCELLED", "EXPIRED", "COMPLETED", "FAILED", "IN_PROCESS"]
    ] = Field(description="status of the orders, if specified filters results.")
    limit: Optional[int] = Field(
        default=30, description="number of most recent results to return"
    )


class CreateOrderRequest(BaseModel):
    wallet: str = Field(description="name of the wallet")
    input_token: str = Field(
        description="public address of the input token. Always different from output token."
    )
    output_token: str = Field(
        description="public address of the output token. Always different from input token."
    )
    input_chain_id: UUID = Field(description="chain id of the input token")
    output_chain_id: UUID = Field(description="chain id of the output token")
    amount: float = Field(description="amount of input token to invest")
    strategy_duration: int = Field(description="duration of the order")
    strategy_duration_unit: Literal[
        "MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "YEAR"
    ] = Field(description="unit of the duration of the order")
    watch_field: Literal["liquidity", "marketCap", "price"] = Field(
        description="field to watch to execute the order. Can be price, marketCap or liquidity"
    )
    direction: Literal["ABOVE", "BELOW"] = Field(
        description="whether or not the order is above or below current market value. Direction is always below for trailing buy/stop and above for LBBB."
    )
    token_address_watcher: str = Field(
        description="public address of the token to watch. should be output token for limit orders and input token for stop loss and take profit orders"
    )
    token_watcher_chain_id: UUID = Field(description="chain id of the token to watch")
    target_value: Optional[float] = Field(
        description="target value to execute the order. You must always specify a target value or delta percentage for non trailing orders. Field should be None for trailing orders."
    )
    delta_percentage: Optional[float] = Field(
        description="delta percentage to execute the order. You must always specify a target value or delta percentage for non trailing orders. Field should be None for trailing orders."
    )
    trailing_offset_value: Optional[float] = Field(
        description="trailing offset value of token address watcher to execute the trailing order. You must always specify a offset target value or offset delta percent for trailing orders. Field should be None for non trailing orders."
    )
    trailing_offset_percentage: Optional[float] = Field(
        description="trailing offset percentage of token address watcher to execute the trailing order. You must always specify a offset target value or offset delta percent for trailing orders. Field should be None for non trailing orders."
    )


class OrderWatcher(BaseModel):
    watch_field: Literal["liquidity", "marketCap", "price"] = Field(
        description="field being watched for a delta"
    )
    delta_type: Literal[
        "INCREASE", "DECREASE", "MOVE", "MOVE_DAILY", "AVERAGE_MOVE"
    ] = Field(description="type of delta change")
    initial_value: float = Field(description="initial value when watcher was created")
    delta_percentage: float = Field(description="percentage for delta change")
    watcher_type: Literal["LIMIT", "STOP_LOSS"] = Field(description="type of watcher")
    buying_price: Optional[float] = Field(
        description="price at which to buy", default=None
    )


class OrderResponse(BaseModel):
    id: str = Field(description="unique identifier of the order")
    amount: float = Field(description="amount of tokens to invest")
    status: str = Field(description="current status of the order")
    input_token_data: TokenData = Field(description="details of the input token")
    output_token_data: TokenData = Field(description="details of the output token")
    wallet_name: str = Field(description="name of the wallet")
    execution_type: Literal["LIMIT", "STOP_LOSS", "TAKE_PROFIT"] = Field(
        description="type of the order"
    )
    expiry_time: str = Field(description="expiry time of the order in ISO format")
    watchers: List[OrderWatcher] = Field(description="list of watchers for the order")
    transaction: Optional[dict] = Field(
        description="transaction details if any", default=None
    )
    created: str = Field(description="ISO 8601 timestamp of the creation of the order")


class CancelOrderRequest(BaseModel):
    order_id: str = Field(description="id of the limit order")


class CancelOrderResponse(BaseModel):
    order_id: str = Field(description="id of the limit order")
    status: str = Field(description="status of the limit order")


class CancelDCAOrderRequest(BaseModel):
    dca_order_id: str = Field(description="id of the DCA order")


class CancelDCAOrderResponse(BaseModel):
    dca_order_id: str = Field(description="id of the DCA order")
    status: str = Field(description="status of the DCA order")


class ListSingleGroupRequest(BaseModel):
    group_name: str = Field(description="Name of the group to retrieve details for")


class CreateWalletRequest(BaseModel):
    name: str = Field(description="Name of the wallet to create")


class ChainDetails(BaseModel):
    chain_id: str = Field(description="chain id")
    chain_name: str = Field(description="chain name")


class ChainWalletDetails(BaseModel):
    address: str = Field(description="wallet address")
    chains: List[ChainDetails] = Field(description="List of chains the wallet is on")


class CreateWalletResponse(BaseModel):
    chains: Dict[str, ChainWalletDetails] = Field(
        description="Mapping of chain name to wallet details for each chain"
    )


class ArchiveWalletsRequest(BaseModel):
    wallet: str = Field(description="Name of the wallet to archive")


class UnarchiveWalletsRequest(BaseModel):
    wallet: str = Field(description="Name of the wallet to unarchive")


class CreateGroupsRequest(BaseModel):
    name: str = Field(description="Name of the group to create")


class AddWalletToGroupRequest(BaseModel):
    group: str = Field(description="Name of the group to add wallets to")
    wallet: str = Field(description="Name of the wallet to add to the group")


class ArchiveWalletGroupRequest(BaseModel):
    group: str = Field(description="Name of the group to archive")


class UnarchiveWalletGroupRequest(BaseModel):
    group: str = Field(description="Name of the group to unarchive")


class RemoveWalletsFromGroupRequest(BaseModel):
    group: str = Field(description="Name of the group to remove wallets from")
    wallet: str = Field(description="Name of the wallet to remove from the group")


class TopTrendingTokensRequestSolana(BaseModel):
    time_frame: Literal[
        "5m", "15m", "30m", "1h", "2h", "3h", "4h", "5h", "6h", "12h", "24h"
    ] = Field(default="24h", description="Time frame to get the top trending tokens")


class TopTrendingTokensRequestCoinMarketCap(BaseModel):
    time_frame: Literal["24h", "7d", "30d"] = Field(
        default="24h", description="Time frame to get the top trending tokens"
    )
    limit: int = Field(
        default=10, description="Number of top trending tokens to return"
    )


class StakeBalanceResponse(BaseModel):
    total_stake_amount: float = Field(description="Total stake balance in jupSol")
    total_stake_amount_in_usd: float = Field(description="Total stake balance in USD")


class RenameWalletRequest(BaseModel):
    wallet: str = Field(description="Name of the wallet to rename")
    new_name: str = Field(description="New name of the wallet")


class CandleStickRequest(BaseModel):
    token_address: str = Field(
        description="token address. To get the address from a token symbol use `get_token_details`"
    )
    chain_id: UUID = Field(
        description="chain id to generate the conversion quote on. Use `list_chains` to get the chain id."
    )
    time_interval: Literal[
        "1S",
        "5S",
        "15S",
        "1",
        "5",
        "15",
        "30",
        "60",
        "240",
        "720",
        "1D",
        "7D",
    ] = Field(
        default="1",
        description="Time frame to get the candle sticks. 5S means 5 seconds, 5 means 5 minutes, 7D means 7 days. Use larger candle time frames over larger time windows to keep returned candles minimal",
    )
    time_from: str = Field(
        description="The time from which to start the candle data in ISO 8601 format. Attempt to change this to keep number of candles returned under 64."
    )
    time_to: Optional[str] = Field(
        default=None,
        description="The time to end the candle data in ISO 8601 format. Use only for historic analysis.",
    )
    market_cap: Optional[bool] = Field(
        default=False,
        description="Whether to return the marketcap of the token instead of the price",
    )


class PrivateKeyRequest(BaseModel):
    wallet: str = Field(
        description="Name of the wallet to get the mnemonic or private key for"
    )
    key_type: Literal["PRIVATE_KEY", "MNEMONIC"] = Field(
        description="Whether to return the private or mnemonic key"
    )


class TokenSearchPromptRequest(BaseModel):
    query: str = Field(
        description="The token search query from user to generate a graphql query for"
    )


class TokenSearchGraphQLQueryRequest(BaseModel):
    query: str = Field(description="The graphql query to search for tokens")


class ChainMetadata(BaseModel):
    matadata: Dict[str, str] | None = Field(description="gas token of the chain")


class ChainInfo(BaseModel):
    id: str = Field(description="id of the chain")
    name: str = Field(description="name of the chain")
    slug: str = Field(description="slug of the chain")
    icon: str = Field(description="icon url of the chain")
    metadata: ChainMetadata = Field(description="metadata of the chain")


class ListChainRequest(BaseModel):
    queries: Optional[List[str]] = Field(
        description="name or slugs of the chains to get details for. otherwise, data of all chains will be returned."
    )


class BridgeStatusRequest(BaseModel):
    transaction_id: str = Field(
        description="id of the bridge transaction to get status for"
    )


class BridgeStatusResponse(BaseModel):
    transaction_id: str = Field(description="id of the bridge transaction")
    status: str = Field(description="status of the bridge transaction")
    transaction_url: str = Field(description="public url of the transaction")


class WrapUnwrapTokensRequest(BaseModel):
    wallet: str = Field(description="name of the wallet")
    chain_id: UUID = Field(description="chain id of the token")
    amount: float = Field(description="amount of token to wrap")


# ------------------------------
# Container Models for List Inputs
# ------------------------------


class RemoveWalletsFromGroupRequestContainer(BaseModel):
    remove_wallets_from_group_requests: List[RemoveWalletsFromGroupRequest]


class AddWalletToGroupRequestContainer(BaseModel):
    add_wallet_to_group_requests: List[AddWalletToGroupRequest]


class CreateWalletRequestContainer(BaseModel):
    create_wallet_requests: List[CreateWalletRequest]


class ArchiveWalletsRequestContainer(BaseModel):
    archive_wallet_requests: List[ArchiveWalletsRequest]


class UnarchiveWalletRequestContainer(BaseModel):
    unarchive_wallet_requests: List[UnarchiveWalletsRequest]


class ArchiveWalletGroupRequestContainer(BaseModel):
    archive_wallet_group_requests: List[ArchiveWalletGroupRequest]


class UnarchiveWalletGroupRequestContainer(BaseModel):
    unarchive_wallet_group_requests: List[UnarchiveWalletGroupRequest]


class WalletTokenPairsContainer(BaseModel):
    wallet_token_pairs: List[WalletTokenPairs]


class CreateGroupsRequestContainer(BaseModel):
    create_groups_requests: List[CreateGroupsRequest]


class ConversionRequestContainer(BaseModel):
    conversion_requests: List[ConversionRequest]


class SwapTransactionRequestContainer(BaseModel):
    swap_transaction_requests: List[SwapTransactionRequest]


class BridgeTransactionRequestContainer(BaseModel):
    bridge_transaction_requests: List[BridgeTransactionRequest]


class TokenDetailsRequestContainer(BaseModel):
    token_details_requests: List[TokenDetailsRequest]


class TokenDetailsResponseContainer(BaseModel):
    token_details_responses: List[TokenDetailsResponse]


class TransferTokensRequestContainer(BaseModel):
    transfer_tokens_requests: List[TransferTokensRequest]


class DCAOrderRequestContainer(BaseModel):
    dca_order_requests: List[DCAOrderRequest]


class CancelDCAOrderRequestContainer(BaseModel):
    cancel_dca_order_requests: List[CancelDCAOrderRequest]


class CreateOrderRequestContainer(BaseModel):
    create_order_requests: List[CreateOrderRequest]


class CreateOrderResponseContainer(BaseModel):
    create_order_responses: List[OrderResponse]


class CancelOrderRequestContainer(BaseModel):
    cancel_order_requests: List[CancelOrderRequest]


class CancelOrderResponseContainer(BaseModel):
    cancel_order_responses: List[CancelOrderResponse]


class RenameWalletRequestContainer(BaseModel):
    rename_wallet_requests: List[RenameWalletRequest]


class ListDCAOrderResponseContainer(BaseModel):
    list_dca_order_responses: List[DCAOrderResponse]


class ListOrderResponseContainer(BaseModel):
    list_order_responses: List[OrderResponse]


class ListChainsResponseContainer(BaseModel):
    list_chains_responses: List[ChainInfo]


class WalletTokenBalanceContainer(BaseModel):
    wallet_token_balances: List[WalletTokenBalance]


class ConversionResponseContainer(BaseModel):
    conversion_responses: List[ConversionResponse]


class SwapTransactionResponseContainer(BaseModel):
    swap_transaction_responses: List[SwapTransactionResponse]


class BridgeTransactionResponseContainer(BaseModel):
    bridge_transaction_responses: List[BridgeTransactionResponse]


class WalletContainer(BaseModel):
    wallets: List[Wallet]


class GroupInfoContainer(BaseModel):
    group_infos: List[GroupInfo]


class WalletArchiveOrUnarchiveResponseContainer(BaseModel):
    wallet_archive_or_unarchive_responses: List[WalletArchiveOrUnarchiveResponse]


class CreateGroupResponseContainer(BaseModel):
    create_group_responses: List[CreateGroupResponse]


class AddWalletToGroupResponseContainer(BaseModel):
    add_wallet_to_group_responses: List[AddWalletToGroupResponse]


class GroupArchiveOrUnarchiveResponseContainer(BaseModel):
    group_archive_or_unarchive_responses: List[GroupArchiveOrUnarchiveResponse]


class RemoveWalletFromGroupResponseContainer(BaseModel):
    remove_wallet_from_group_responses: List[RemoveWalletFromGroupResponse]


class TransferTokenResponseContainer(BaseModel):
    transfer_token_responses: List[TransferTokenResponse]


class DCAOrderResponseContainer(BaseModel):
    dca_order_responses: List[DCAOrderResponse]


class CancelDCAOrderResponseContainer(BaseModel):
    cancel_dca_order_responses: List[CancelDCAOrderResponse]


# ------------------------------
# API Client
# ------------------------------

# Setup logger for the module
import logging
import traceback


class ArmorWalletAPIClient:
    def __init__(
        self,
        access_token: str,
        base_api_url: str = "https://app.armorwallet.ai/api/v1",
        logger=None,
    ):
        self.base_api_url = base_api_url
        self.access_token = access_token
        self.logger = logger

    async def _api_call(self, method: str, endpoint: str, payload: str = None) -> dict:
        """Utility function for API calls to the wallet.
        It sets common headers and raises errors on non-2xx responses.
        """
        url = f"{self.base_api_url}/{endpoint}"
        payload = json.dumps(payload)
        if self.logger is not None:
            self.logger.debug(f"Request: {method} {url} Payload: {payload}")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.request(
                    method, url, headers=headers, data=payload, follow_redirects=False
                )

                if self.logger is not None:
                    self.logger.debug(
                        f"Response status: {response.status_code} Response: {response.text}"
                    )
            if response.status_code >= 400:
                if self.logger is not None:
                    self.logger.error(
                        f"API Error {response.status_code}: {response.text}"
                    )
                raise Exception(f"API Error {response.status_code}: {response.text}")
            try:
                return response.json()
            except Exception:
                if self.logger is not None:
                    self.logger.error(f"JSON Parsing: {response.text}")
                return {"text": response.text}
        except Exception as e:
            traceback.print_exc()
            if self.logger is not None:
                self.logger.error(f"{e}")
            return {"text": str(e)}

    async def get_wallet_token_balance(
        self, data: WalletTokenPairsContainer
    ) -> WalletTokenBalanceContainer | Any:
        """Get balances from a list of wallet and token pairs."""
        payload = data.model_dump(exclude_none=True, mode="json")["wallet_token_pairs"]
        return await self._api_call("POST", "v1/tokens/wallet-token-balance/", payload)

    async def conversion_api(
        self, data: ConversionRequestContainer
    ) -> ConversionResponseContainer | Any:
        """Perform a token conversion."""
        payload = data.model_dump(exclude_none=True, mode="json")["conversion_requests"]
        return await self._api_call(
            "POST", "v2/tokens/token-price-conversion/", payload
        )

    async def swap_quote(self, data: SwapQuoteRequest) -> SwapQuoteResponse | Any:
        """Obtain a swap quote."""
        payload = data.model_dump(exclude_none=True, mode="json")
        return await self._api_call("POST", "v2/transactions/quote/", payload)

    async def bridge_quote(self, data: BridgeQuoteRequest) -> BridgeQuoteResponse | Any:
        """Obtain a bridge quote."""
        payload = data.model_dump(exclude_none=True, mode="json")
        return await self._api_call("POST", "v2/transactions/quote/", payload)

    async def swap_transaction(
        self, data: SwapTransactionRequest
    ) -> SwapTransactionResponse | Any:
        """Execute the swap transactions."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", "v2/transactions/swap/", payload)

    async def bridge_transaction(
        self, data: BridgeTransactionRequest
    ) -> BridgeTransactionResponse | Any:
        """Execute the bridge transactions."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", "v2/transactions/swap/", payload)

    async def get_all_wallets(self, data: ListWalletsRequest) -> WalletContainer | Any:
        """Return all wallets with balances."""
        payload = data.model_dump(exclude_none=True, mode="json")
        return await self._api_call("POST", "v2/wallets/", payload)

    async def get_single_wallet_details(
        self, data: ListSingleWalletRequest
    ) -> WalletContainer | Any:
        """Return details for a single wallet."""
        payload = data.model_dump(exclude_none=True, mode="json")
        return await self._api_call("POST", "v2/wallets/detail/", payload)

    async def search_token(self, data: TokenSearchGraphQLQueryRequest) -> Dict | Any:
        """Get details of a token."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", "v2/tokens/search-token/", payload)

    async def get_official_token_address(
        self, data: TokenDetailsRequestContainer
    ) -> TokenDetailsResponseContainer | Any:
        """Retrieve the token address."""
        payload = data.model_dump(exclude_none=True, mode="json")[
            "token_details_requests"
        ]
        return await self._api_call("POST", "v2/tokens/official-token-detail/", payload)

    async def list_groups(self) -> GroupInfoContainer | Any:
        """Return a list of wallet groups."""
        return await self._api_call("GET", "v1/wallets/groups/")

    async def list_single_group(
        self, data: ListSingleGroupRequest
    ) -> SingleGroupInfo | Any:
        """Return details for a single wallet group."""
        return await self._api_call("GET", f"v1/wallets/groups/{data.group_name}/")

    async def create_wallet(
        self, data: CreateWalletRequestContainer
    ) -> CreateWalletResponse | Any:
        """Create new wallets given a list of wallet names."""
        payload = data.model_dump(exclude_none=True)["create_wallet_requests"]
        return await self._api_call("POST", "v1/wallets/", payload)

    async def archive_wallets(
        self, data: ArchiveWalletsRequestContainer
    ) -> WalletArchiveOrUnarchiveResponseContainer:
        """Archive the wallets specified in the list."""
        payload = data.model_dump(exclude_none=True)["archive_wallet_requests"]
        return await self._api_call("POST", "v1/wallets/archive/", payload)

    async def unarchive_wallets(
        self, data: UnarchiveWalletRequestContainer
    ) -> WalletArchiveOrUnarchiveResponseContainer | Any:
        """Unarchive the wallets specified in the list."""
        payload = data.model_dump(exclude_none=True)["unarchive_wallet_requests"]
        return await self._api_call("POST", "v1/wallets/unarchive/", payload)

    async def create_groups(
        self, data: CreateGroupsRequestContainer
    ) -> CreateGroupResponseContainer | Any:
        """Create new wallet groups given a list of group names."""
        payload = data.model_dump(exclude_none=True)["create_groups_requests"]
        return await self._api_call("POST", "v1/wallets/groups/", payload)

    async def add_wallets_to_group(
        self, data: AddWalletToGroupRequestContainer
    ) -> AddWalletToGroupResponseContainer | Any:
        """Add wallets to a specific group."""
        payload = data.model_dump(exclude_none=True)["add_wallet_to_group_requests"]
        return await self._api_call("POST", "v1/wallets/add-wallet-to-group/", payload)

    async def archive_wallet_group(
        self, data: ArchiveWalletGroupRequestContainer
    ) -> GroupArchiveOrUnarchiveResponseContainer | Any:
        """Archive the specified wallet groups."""
        payload = data.model_dump(exclude_none=True)["archive_wallet_group_requests"]
        return await self._api_call("POST", "v1/wallets/group-archive/", payload)

    async def unarchive_wallet_group(
        self, data: UnarchiveWalletGroupRequestContainer
    ) -> GroupArchiveOrUnarchiveResponseContainer | Any:
        """Unarchive the specified wallet groups."""
        payload = data.model_dump(exclude_none=True)["unarchive_wallet_group_requests"]
        return await self._api_call("POST", "v1/wallets/group-unarchive/", payload)

    async def remove_wallets_from_group(
        self, data: RemoveWalletsFromGroupRequestContainer
    ) -> RemoveWalletFromGroupResponseContainer | Any:
        """Remove wallets from a group."""
        payload = data.model_dump(exclude_none=True)[
            "remove_wallets_from_group_requests"
        ]
        return await self._api_call(
            "POST", "v1/wallets/remove-wallet-from-group/", payload
        )

    async def transfer_tokens(
        self, data: TransferTokensRequest
    ) -> TransferTokenResponseContainer | Any:
        """Transfer tokens from one wallet to another."""
        payload = data.model_dump(exclude_none=True, mode="json")
        return await self._api_call("POST", "v2/transfers/transfer/", payload)

    async def create_dca_order(
        self, data: DCAOrderRequestContainer
    ) -> DCAOrderResponseContainer | Any:
        """Create a DCA order."""
        payload = data.model_dump(exclude_none=True, mode="json")["dca_order_requests"]
        return await self._api_call(
            "POST", "v1/transactions/dca-order/create/", payload
        )

    async def list_dca_orders(
        self, data: ListDCAOrderRequest
    ) -> ListDCAOrderResponseContainer | Any:
        """List all DCA orders."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", f"v1/transactions/dca-order/", payload)

    async def cancel_dca_order(
        self, data: CancelDCAOrderRequestContainer
    ) -> CancelDCAOrderResponseContainer | Any:
        """Cancel a DCA order."""
        payload = data.model_dump(exclude_none=True)["cancel_dca_order_requests"]
        return await self._api_call(
            "POST", "v1/transactions/dca-order/cancel/", payload
        )

    async def create_order(
        self, data: CreateOrderRequestContainer
    ) -> CreateOrderResponseContainer | Any:
        """Create a order."""
        payload = data.model_dump(exclude_none=True, mode="json")[
            "create_order_requests"
        ]
        return await self._api_call("POST", "v1/transactions/order/create/", payload)

    async def list_orders(
        self, data: ListOrderRequest
    ) -> ListOrderResponseContainer | Any:
        """List all orders."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", f"v1/transactions/order/", payload)

    async def cancel_order(
        self, data: CancelOrderRequestContainer
    ) -> CancelOrderResponseContainer | Any:
        """Cancel a order."""
        payload = data.model_dump(exclude_none=True)["cancel_order_requests"]
        return await self._api_call("POST", "v1/transactions/order/cancel/", payload)

    async def top_trending_tokens_for_solana(
        self, data: TopTrendingTokensRequestSolana
    ) -> List | Any:
        """Get the top trending tokens."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", f"v1/tokens/trending/", payload)

    async def top_trending_tokens_for_coinmarketcap(
        self, data: TopTrendingTokensRequestCoinMarketCap
    ) -> List | Any:
        """Get the top trending tokens."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", f"v2/tokens/trending/", payload)

    async def get_stake_balances(self) -> StakeBalanceResponse | Any:
        """Get the stake balances."""
        return await self._api_call("GET", "v1/frontend/wallets/stake/balance/")

    async def rename_wallet(self, data: RenameWalletRequestContainer) -> List | Any:
        """Rename a wallet."""
        payload = data.model_dump(exclude_none=True)["rename_wallet_requests"]
        return await self._api_call("POST", "v1/wallets/rename/", payload)

    async def get_market_candle_data(self, data: CandleStickRequest) -> Dict | Any:
        """Get the candle sticks."""
        payload = data.model_dump(exclude_none=True, mode="json")
        return await self._api_call("POST", f"v2/tokens/candles/", payload)

    async def send_key_to_telegram(self, data: PrivateKeyRequest) -> Dict | Any:
        """Send the mnemonic or private key to telegram."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", f"v1/users/telegram/send-message/", payload)

    async def list_chains(
        self, data: ListChainRequest
    ) -> ListChainsResponseContainer | Any:
        """List all chains along with their chain id."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", "v2/tokens/chains/", payload)

    async def get_bridge_transaction_status(
        self, data: BridgeStatusRequest
    ) -> BridgeStatusResponse | Any:
        """Get the status of a bridge transaction."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", "v2/transactions/swap/status/", payload)

    async def wrap_tokens(
        self, data: WrapUnwrapTokensRequest
    ) -> SwapQuoteResponse | Any:
        """Wrap tokens."""
        payload = data.model_dump(exclude_none=True, mode="json")
        payload["wrap_type"] = "WRAP"
        return await self._api_call(
            "POST", "v2/transactions/quote/wrap-unwrap/", payload
        )

    async def unwrap_tokens(
        self, data: WrapUnwrapTokensRequest
    ) -> SwapQuoteResponse | Any:
        """Unwrap tokens."""
        payload = data.model_dump(exclude_none=True, mode="json")
        payload["wrap_type"] = "UNWRAP"
        return await self._api_call(
            "POST", "v2/transactions/quote/wrap-unwrap/", payload
        )


# ------------------------------
# Utility Functions
# ------------------------------


def calculate(expr: str, variables: dict = None) -> float:
    """
    Evaluate a math/stat expression with support for variables and common functions.
    """
    variables = variables or {}
    # Allowed names from math and statistics
    safe_names = {k: v for k, v in vars(math).items() if not k.startswith("__")}
    safe_names.update(
        {
            "mean": statistics.mean,
            "median": statistics.median,
            "stdev": statistics.stdev,
            "variance": statistics.variance,
            "sum": sum,
            "min": min,
            "max": max,
            "len": len,
            "abs": abs,
            "round": round,
        }
    )

    # Safe operators
    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }

    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.BinOp):
            return ops[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return ops[type(node.op)](_eval(node.operand))
        elif isinstance(node, ast.Name):
            if node.id in variables:
                return variables[node.id]
            elif node.id in safe_names:
                return safe_names[node.id]
            else:
                raise NameError(f"Unknown variable or function: {node.id}")
        elif isinstance(node, ast.Call):
            func = _eval(node.func)
            args = [_eval(arg) for arg in node.args]
            return func(*args)
        elif isinstance(node, ast.List):
            return [_eval(elt) for elt in node.elts]
        else:
            raise TypeError(f"Unsupported expression type: {type(node)}")

    parsed = ast.parse(expr, mode="eval")
    return _eval(parsed.body)
