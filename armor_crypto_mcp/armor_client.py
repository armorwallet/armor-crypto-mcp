import json
import os
from pydantic import BaseModel, Field
from typing_extensions import List, Optional, Literal, Dict
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
    wallet: str = Field(description="The name of wallet. To get wallet names use `get_user_wallets_and_groups_list`")
    token: str = Field(description="public address of token. To get the address from a token symbol use `get_token_details`")


class WalletTokenBalance(BaseModel):
    wallet: str = Field(description="name of wallet")
    token: str = Field(description="public address of token")
    balance: float = Field(description="balance of token")


class ConversionRequest(BaseModel):
    input_amount: float = Field(description="input amount to convert")
    input_token: str = Field(description="public address of input token")
    output_token: str = Field(description="public address of output token")


class ConversionResponse(BaseModel):
    input_amount: float = Field(description="input amount before conversion")
    input_token: str = Field(description="public address of input token")
    output_token: str = Field(description="public address of output token")
    output_amount: float = Field(description="output amount after conversion")


class SwapQuoteRequest(BaseModel):
    from_wallet: str = Field(description="The name of the wallet that input_token is in.")
    input_token: str = Field(description="public mint address of input token. To get the address from a token symbol use `get_token_details`")
    output_token: str = Field(description="public mint address of output token. To get the address from a token symbol use `get_token_details`")
    input_amount: float = Field(description="input amount to swap")
    slippage: float = Field("slippage percentage. To estimate slippage based on liquidity see `get_token_details` for the input_token_symbol. 1.0 for high liquidity and near 20.0 for lower liquidity.")


class StakeQuoteRequest(BaseModel):
    from_wallet: str = Field(description="The name of the wallet that input_token is in.")
    input_token: str = "So11111111111111111111111111111111111111112"  # Hardcoded SOL token address
    output_token: str = Field(description="the public mint address of the output liquid staking derivative token to stake.") # "jupSoLaHXQiZZTSfEWMTRRgpnyFm8f6sZdosWBjx93v"
    input_amount: float = Field(description="input amount to swap")


class UnstakeQuoteRequest(BaseModel):
    from_wallet: str = Field(description="The name of the wallet that input_token is in.")
    input_token: str = Field(description="the public mint address of the input liquid staking derivative token to unstake.") # "jupSoLaHXQiZZTSfEWMTRRgpnyFm8f6sZdosWBjx93v"
    output_token: str = "So11111111111111111111111111111111111111112"
    input_amount: float = Field(description="input amount to swap")


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


class SwapTransactionRequest(BaseModel):
    transaction_id: str = Field(description="unique id of the generated swap quote")


class StakeTransactionRequest(BaseModel):
    transaction_id: str = Field(description="unique id of the generated stake quote")


class UnstakeTransactionRequest(BaseModel):
    transaction_id: str = Field(description="unique id of the generated unstake quote")


class SwapTransactionResponse(BaseModel):
    id: str = Field(description="unique id of the swap transaction")
    transaction_error: Optional[str] = Field(description="error message if the transaction fails")
    transaction_url: str = Field(description="public url of the transaction")
    input_amount: float = Field(description="input amount in input token")
    output_amount: float = Field(description="output amount in output token")
    status: str = Field(description="status of the transaction")


class ListWalletsRequest(BaseModel):
    is_archived: bool = Field(default=False, description="whether to include archived wallets")


class WalletBalance(BaseModel):
    mint_address: str = Field(description="public mint address of output token. To get the address from a token symbol use `get_token_details`")
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


class Wallet(WalletInfo):
    balances: List[WalletBalance] = Field(description="list of balances of the wallet")


class TokenDetailsRequest(BaseModel):
    query: str = Field(description="token symbol or address")


class TokenDetailsResponse(BaseModel):
    symbol: str = Field(description="symbol of the token")
    mint_address: str = Field(description="mint address of the token")


class TokenSearchRequest(BaseModel):
    query: str = Field(description="token symbol or address")
    sort_by: Optional[Literal['decimals', 'holders', 'jupiter', 'verified', 'liquidityUsd', 'marketCapUsd', 'priceUsd', 'totalBuys', 'totalSells', 'totalTransactions', 'volume_5m', 'volume', 'volume_15m', 'volume_30m', 'volume_1h', 'volume_6h', 'volume_12h', 'volume_24h']] = Field(description="Sort token data results by this field")
    sort_order: Optional[Literal['asc', 'desc']] = Field(default='desc', description="The order of the sorted results")
    limit: Optional[int] = Field(default=10, description="The number of results to return from the search. Use default unless specified. Should not be over 30 if looking up multiple tokens.")

class TokenSearchResponse(BaseModel):
    name: str = Field(description="name of the token")
    symbol: str = Field(description="symbol of the token")
    mint_address: Optional[str] = Field(description="mint address of the token")
    decimals: Optional[int] = Field(description="number of decimals of the token, returns only if include_details is True")
    image: Optional[str] = Field(description="image url of the token, returns only if include_details is True")
    holders: Optional[int] = Field(description="number of holders of the token, returns only if include_details is True")
    jupiter: Optional[bool] = Field(description="whether the token is supported by Jupiter, returns only if include_details is True")
    verified: Optional[bool] = Field(description="whether the token is verified, returns only if include_details is True")
    liquidityUsd: Optional[float] = Field(description="liquidity of the token in USD, returns only if include_details is True")
    marketCapUsd: Optional[float] = Field(description="market cap of the token in USD, returns only if include_details is True")
    priceUsd: Optional[float] = Field(description="price of the token in USD, returns only if include_details is True")
    lpBurn: Optional[float] = Field(description="lp burn of the token, returns only if include_details is True")
    market: Optional[str] = Field(description="market of the token, returns only if include_details is True")
    freezeAuthority: Optional[str] = Field(description="freeze authority of the token, returns only if include_details is True")
    mintAuthority: Optional[str] = Field(description="mint authority of the token, returns only if include_details is True")
    poolAddress: Optional[str] = Field(description="pool address of the token, returns only if include_details is True")
    totalBuys: Optional[int] = Field(description="total number of buys of the token, returns only if include_details is True")
    totalSells: Optional[int] = Field(description="total number of sells of the token, returns only if include_details is True")
    totalTransactions: Optional[int] = Field(description="total number of transactions of the token, returns only if include_details is True")
    volume: Optional[float] = Field(description="volume of the token, returns only if include_details is True")
    volume_5m: Optional[float] = Field(description="volume of the token in the last 5 minutes, returns only if include_details is True")
    volume_15m: Optional[float] = Field(description="volume of the token in the last 15 minutes, returns only if include_details is True")
    volume_30m: Optional[float] = Field(description="volume of the token in the last 30 minutes, returns only if include_details is True")
    volume_1h: Optional[float] = Field(description="volume of the token in the last 1 hour, returns only if include_details is True")
    volume_6h: Optional[float] = Field(description="volume of the token in the last 6 hours, returns only if include_details is True")
    volume_12h: Optional[float] = Field(description="volume of the token in the last 12 hours, returns only if include_details is True")
    volume_24h: Optional[float] = Field(description="volume of the token in the last 24 hours, returns only if include_details is True")


class GroupInfo(BaseModel):
    id: str = Field(description="id of the group")
    name: str = Field(description="name of the group")
    is_archived: bool = Field(description="whether the group is archived")


class SingleGroupInfo(GroupInfo):
    wallets: List[WalletInfo] = Field(description="list of wallets in the group")


class WalletArchiveOrUnarchiveResponse(BaseModel):
    wallet_name: str = Field(description="name of the wallet")
    message: str = Field(description="message of the operation showing if wallet was archived or unarchived")


class CreateGroupResponse(BaseModel):
    id: str = Field(description="id of the group")
    name: str = Field(description="name of the group")
    is_archived: bool = Field(description="whether the group is archived")


class AddWalletToGroupResponse(BaseModel):
    wallet_name: str = Field(description="name of the wallet to add to the group")
    group_name: str = Field(description="name of the group to add the wallet to")
    message: str = Field(description="message of the operation showing if wallet was added to the group")


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
    from_wallet: str = Field(description="name of the wallet to transfer tokens from")
    to_wallet_address: str = Field(description="public address of the wallet to transfer tokens to. Use `get_user_wallets_and_group_list` if you only have a wallet name")
    token: str = Field(description="public contract address of the token to transfer. To get the address from a token symbol use `get_token_details`")
    amount: float = Field(description="amount of tokens to transfer")


class TransferTokenResponse(BaseModel):
    amount: float = Field(description="amount of tokens transferred")
    from_wallet_address: str = Field(description="public address of the wallet tokens were transferred from")
    to_wallet_address: str = Field(description="public address of the wallet tokens were transferred to")
    token_address: str = Field(description="public address of the token transferred")
    transaction_url: str = Field(description="public url of the transaction")
    message: str = Field(description="message of the operation showing if tokens were transferred")

class ListDCAOrderRequest(BaseModel):
    status: Optional[Literal["COMPLETED", "OPEN", "CANCELLED"]] = Field(description="status of the DCA orders, if specified filters the results.")
    limit: Optional[int] = Field(default=30, description="number of mostrecent results to return")

class DCAOrderRequest(BaseModel):
    wallet: str = Field(description="name of the wallet")
    input_token: str = Field(description="public address of the input token. To get the address from a token symbol use `get_token_details`")
    output_token: str = Field(description="public address of the output token. To get the address from a token symbol use `get_token_details`")
    amount: float = Field(description="total amount of input token to invest")
    cron_expression: str = Field(description="cron expression for the DCA worker execution frequency")
    strategy_duration_unit: Literal["MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "YEAR"] = Field(description="unit of the duration of the DCA order")
    strategy_duration: int = Field(description="Total running time of the DCA order given in strategy duration units, should be more than 0")
    execution_type: Literal["MULTIPLE", "SINGLE"] = Field(description="set to SINGLE only if the user is asking for a single scheduled order, MULTIPLE if it is a true DCA")
    token_address_watcher: Optional[str] = Field(description="If the DCA is conditional, public address of the token to watch.")
    watch_field: Optional[Literal["liquidity", "marketCap", "price"]] = Field(description="If the DCA is conditional, field to watch for the condition")
    delta_type: Optional[Literal["INCREASE", "DECREASE", "MOVE", "MOVE_DAILY", "AVERAGE_MOVE"]] = Field(description="If the DCA is conditional, the operator of the watch field in the conditional statement")
    delta_percentage: Optional[float] = Field(description="If the DCA is conditional, percentage of the change to watch for given the delta_type")
    time_zone: Optional[str] = Field(description="user's time zone. Defaults to UTC")


class DCAWatcher(BaseModel):
    watch_field: Literal["liquidity", "marketCap", "price"] = Field(description="field to watch for the DCA order")
    delta_type: Literal["INCREASE", "DECREASE", "MOVE", "MOVE_DAILY", "AVERAGE_MOVE"] = Field(description="type of the delta")
    initial_value: float = Field(description="initial value of the delta")
    delta_percentage: float = Field(description="percentage of the delta")


class TokenData(BaseModel):
    name: str = Field(description="name of the token")
    symbol: str = Field(description="symbol of the token")
    mint_address: str = Field(description="mint address of the token")


class DCAOrderResponse(BaseModel):
    id: str = Field(description="id of the DCA order")
    amount: float = Field(description="amount of tokens to invest")
    investment_per_cycle: float = Field(description="amount of tokens to invest per cycle")
    cycles_completed: int = Field(description="number of cycles completed")
    total_cycles: int = Field(description="total number of cycles")
    human_readable_expiry: str = Field(description="human readable expiry date of the DCA order")
    status: str = Field(description="status of the DCA order")
    input_token_data: TokenData = Field(description="details of the input token")
    output_token_data: TokenData = Field(description="details of the output token")
    wallet_name: str = Field(description="name of the wallet")
    watchers: List[DCAWatcher] = Field(description="list of watchers for the DCA order")
    dca_transactions: List[dict] = Field(description="list of DCA transactions")  # Can be further typed if structure is known
    created: str = Field(description="Linux timestamp of the creation of the order")


class ListOrderRequest(BaseModel):
    status: Optional[Literal["OPEN", "CANCELLED", "EXPIRED", "COMPLETED", "FAILED", "IN_PROCESS"]] = Field(description="status of the orders, if specified filters results.")
    limit: Optional[int] = Field(default=30, description="number of most recent results to return")


class CreateOrderRequest(BaseModel):
    wallet: str = Field(description="name of the wallet")
    input_token: str = Field(description="public address of the input token")
    output_token: str = Field(description="public address of the output token")
    amount: float = Field(description="amount of input token to invest")
    strategy_duration: int = Field(description="duration of the order")
    strategy_duration_unit: Literal["MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "YEAR"] = Field(description="unit of the duration of the order")
    watch_field: Literal["liquidity", "marketCap", "price"] = Field(description="field to watch to execute the order. Can be price, marketCap or liquidity")
    direction: Literal["ABOVE", "BELOW"] = Field(description="whether or not the order is above or below current market value")
    token_address_watcher: str = Field(description="public address of the token to watch. should be output token for limit orders and input token for stop loss and take profit orders")
    target_value: Optional[float] = Field(description="target value to execute the order. You must always specify a target value or delta percentage.")
    delta_percentage: Optional[float] = Field(description="delta percentage to execute the order. You must always specify a target value or delta percentage.")

class OrderWatcher(BaseModel):
    watch_field: Literal["liquidity", "marketCap", "price"] = Field(description="field being watched for a delta")
    delta_type: Literal["INCREASE", "DECREASE", "MOVE", "MOVE_DAILY", "AVERAGE_MOVE"] = Field(description="type of delta change")
    initial_value: float = Field(description="initial value when watcher was created")
    delta_percentage: float = Field(description="percentage for delta change")
    watcher_type: Literal["LIMIT", "STOP_LOSS"] = Field(description="type of watcher")
    buying_price: Optional[float] = Field(description="price at which to buy", default=None)


class OrderResponse(BaseModel):
    id: str = Field(description="unique identifier of the order")
    amount: float = Field(description="amount of tokens to invest")
    status: str = Field(description="current status of the order")
    input_token_data: TokenData = Field(description="details of the input token")
    output_token_data: TokenData = Field(description="details of the output token")
    wallet_name: str = Field(description="name of the wallet")
    execution_type: Literal["LIMIT", "STOP_LOSS", "TAKE_PROFIT"] = Field(description="type of the order")
    expiry_time: str = Field(description="expiry time of the order in ISO format")
    watchers: List[OrderWatcher] = Field(description="list of watchers for the order")
    transaction: Optional[dict] = Field(description="transaction details if any", default=None)
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
    group_name: str = Field(description="Name of the group to archive")

class UnarchiveWalletGroupRequest(BaseModel):
    group_name: str = Field(description="Name of the group to unarchive")

class RemoveWalletsFromGroupRequest(BaseModel):
    group: str = Field(description="Name of the group to remove wallets from")
    wallet: str = Field(description="List of wallet names to remove from the group")

class TopTrendingTokensRequest(BaseModel):
    time_frame: Literal["5m", "15m", "30m", "1h", "2h", "3h", "4h", "5h", "6h", "12h", "24h"] = Field(default="24h", description="Time frame to get the top trending tokens")

class StakeBalanceResponse(BaseModel):
    total_stake_amount: float = Field(description="Total stake balance in jupSol")
    total_stake_amount_in_usd: float = Field(description="Total stake balance in USD")


class RenameWalletRequest(BaseModel):
    wallet: str = Field(description="Name of the wallet to rename")
    new_name: str = Field(description="New name of the wallet")


class CandleStickRequest(BaseModel):
    token_address: str = Field(description="Public mint address of the token. To get the address from a token symbol use `get_token_details`")
    time_interval: Literal["1s", "5s", "15s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1mn"] = Field(default="1h", description="Time frame to get the candle sticks. Use larger candle time frames over larger time windows to keep returned candles minimal")
    time_from: str = Field(description="The time from which to start the candle data in ISO 8601 format. Attempt to change this to keep number of candles returned under 64.")
    time_to: Optional[str] = Field(default=None, description="The time to end the candle data in ISO 8601 format. Use only for historic analysis.")
    market_cap: Optional[bool] = Field(default=False, description="Whether to return the marketcap of the token instead of the price")
    
class PrivateKeyRequest(BaseModel):
    wallet: str = Field(description="Name of the wallet to get the mnemonic or private key for")
    key_type: Literal['PRIVATE_KEY', 'MNEMONIC'] = Field(description="Whether to return the private or mnemonic key")

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


class SwapQuoteRequestContainer(BaseModel):
    swap_quote_requests: List[SwapQuoteRequest]


class StakeQuoteRequestContainer(BaseModel):
    stake_quote_requests: List[StakeQuoteRequest]


class UnstakeQuoteRequestContainer(BaseModel):
    unstake_quote_requests: List[UnstakeQuoteRequest]


class SwapTransactionRequestContainer(BaseModel):
    swap_transaction_requests: List[SwapTransactionRequest]


class StakeTransactionRequestContainer(BaseModel):
    stake_transaction_requests: List[StakeTransactionRequest]


class UnstakeTransactionRequestContainer(BaseModel):
    unstake_transaction_requests: List[UnstakeTransactionRequest]


class TokenSearchResponseContainer(BaseModel):
    token_search_responses: List[TokenSearchResponse]


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

# ------------------------------
# API Client
# ------------------------------

# Setup logger for the module
import logging
import traceback

class ArmorWalletAPIClient:
    def __init__(self, access_token: str, base_api_url: str = 'https://app.armorwallet.ai/api/v1', logger=None):
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
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.request(method, url, headers=headers, data=payload, follow_redirects=False)
                
                if self.logger is not None:
                    self.logger.debug(f"Response status: {response.status_code} Response: {response.text}")
            if response.status_code >= 400:
                if self.logger is not None:
                    self.logger.error(f"API Error {response.status_code}: {response.text}")
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

    async def get_wallet_token_balance(self, data: WalletTokenPairsContainer) -> List[WalletTokenBalance]:
        """Get balances from a list of wallet and token pairs."""
        # payload = [v.model_dump() for v in data.wallet_token_pairs]
        payload = data.model_dump(exclude_none=True)['wallet_token_pairs']
        return await self._api_call("POST", "tokens/wallet-token-balance/", payload)

    async def conversion_api(self, data: ConversionRequestContainer) -> List[ConversionResponse]:
        """Perform a token conversion."""
        # payload = [v.model_dump() for v in data.conversion_requests]
        payload = data.model_dump(exclude_none=True)['conversion_requests']
        return await self._api_call("POST", "tokens/token-price-conversion/", payload)

    async def swap_quote(self, data: SwapQuoteRequestContainer) -> List[SwapQuoteResponse]:
        """Obtain a swap quote."""
        # payload = [v.model_dump() for v in data.swap_quote_requests]
        payload = data.model_dump(exclude_none=True)['swap_quote_requests']
        return await self._api_call("POST", "transactions/quote/", payload)

    async def stake_quote(self, data: StakeQuoteRequestContainer) -> StakeQuoteRequestContainer:
        """Obtain a stake quote."""
        payload = data.model_dump(exclude_none=True)['stake_quote_requests']
        return await self._api_call("POST", "transactions/quote/", payload)
    
    async def unstake_quote(self, data: UnstakeQuoteRequestContainer) -> UnstakeQuoteRequestContainer:
        """Obtain an unstake quote."""
        payload = data.model_dump(exclude_none=True)['unstake_quote_requests']
        return await self._api_call("POST", "transactions/quote/", payload)

    async def swap_transaction(self, data: SwapTransactionRequestContainer) -> List[SwapTransactionResponse]:
        """Execute the swap transactions."""
        # payload = [v.model_dump() for v in data.swap_transaction_requests]
        payload = data.model_dump(exclude_none=True)['swap_transaction_requests']
        return await self._api_call("POST", "transactions/swap/", payload)
    
    async def stake_transaction(self, data: StakeTransactionRequestContainer) -> StakeTransactionRequestContainer:
        """Execute the stake transactions."""
        payload = data.model_dump(exclude_none=True)['stake_transaction_requests']
        return await self._api_call("POST", "transactions/swap/", payload)
    
    async def unstake_transaction(self, data: UnstakeTransactionRequestContainer) -> UnstakeTransactionRequestContainer:
        """Execute the unstake transactions."""
        payload = data.model_dump(exclude_none=True)['unstake_transaction_requests']
        return await self._api_call("POST", "transactions/swap/", payload)

    async def get_all_wallets(self, data: ListWalletsRequest) -> List[Wallet]:
        """Return all wallets with balances."""
        return await self._api_call("GET", f"wallets/?is_archived={data.is_archived}")
    
    async def search_token(self, data: TokenSearchRequest) -> TokenSearchResponseContainer:
        """Get details of a token."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", "tokens/search-token/", payload)

    async def get_official_token_address(self, data: TokenDetailsRequestContainer) -> TokenDetailsResponseContainer:
        """Retrieve the mint address of token."""
        payload = data.model_dump(exclude_none=True)['token_details_requests']
        return await self._api_call("POST", "tokens/official-token-detail/", payload)

    async def list_groups(self) -> List[GroupInfo]:
        """Return a list of wallet groups."""
        return await self._api_call("GET", "wallets/groups/")

    async def list_single_group(self, data: ListSingleGroupRequest) -> SingleGroupInfo:
        """Return details for a single wallet group."""
        return await self._api_call("GET", f"wallets/groups/{data.group_name}/")

    async def create_wallet(self, data: CreateWalletRequestContainer) -> List[WalletInfo]:
        """Create new wallets given a list of wallet names."""
        # payload = json.dumps([{"name": wallet_name} for wallet_name in data.wallet_names])
        payload = data.model_dump(exclude_none=True)['create_wallet_requests']
        return await self._api_call("POST", "wallets/", payload)

    async def archive_wallets(self, data: ArchiveWalletsRequestContainer) -> List[WalletArchiveOrUnarchiveResponse]:
        """Archive the wallets specified in the list."""
        # payload = json.dumps([{"wallet": wallet_name} for wallet_name in data.wallet_names])
        payload = data.model_dump(exclude_none=True)['archive_wallet_requests']
        return await self._api_call("POST", "wallets/archive/", payload)

    async def unarchive_wallets(self, data: UnarchiveWalletsRequest) -> List[WalletArchiveOrUnarchiveResponse]:
        """Unarchive the wallets specified in the list."""
        # payload = json.dumps([{"wallet": wallet_name} for wallet_name in data.wallet_names])
        payload = data.model_dump(exclude_none=True)['unarchive_wallet_requests']
        return await self._api_call("POST", "wallets/unarchive/", payload)

    async def create_groups(self, data: CreateGroupsRequest) -> List[CreateGroupResponse]:
        """Create new wallet groups given a list of group names."""
        # payload = json.dumps([{"name": group_name} for group_name in data.group_names])
        payload = data.model_dump(exclude_none=True)['create_groups_requests']
        return await self._api_call("POST", "wallets/groups/", payload)

    async def add_wallets_to_group(self, data: AddWalletToGroupRequestContainer) -> List[AddWalletToGroupResponse]:
        """Add wallets to a specific group."""
        # payload = json.dumps([{"wallet": wallet_name, "group": data.group_name} for wallet_name in data.wallet_names])
        payload = data.model_dump(exclude_none=True)['add_wallet_to_group_requests']
        return await self._api_call("POST", "wallets/add-wallet-to-group/", payload)

    async def archive_wallet_group(self, data: ArchiveWalletGroupRequestContainer) -> List[GroupArchiveOrUnarchiveResponse]:
        """Archive the specified wallet groups."""
        # payload = json.dumps([{"group": group_name} for group_name in data.group_names])
        payload = data.model_dump(exclude_none=True)['archive_wallet_group_requests']
        return await self._api_call("POST", "wallets/group-archive/", payload)

    async def unarchive_wallet_group(self, data: UnarchiveWalletGroupRequestContainer) -> List[GroupArchiveOrUnarchiveResponse]:
        """Unarchive the specified wallet groups."""
        # payload = json.dumps([{"group": group_name} for group_name in data.group_names])
        payload = data.model_dump(exclude_none=True)['unarchive_wallet_group_requests']
        return await self._api_call("POST", "wallets/group-unarchive/", payload)

    async def remove_wallets_from_group(self, data: RemoveWalletsFromGroupRequestContainer) -> List[RemoveWalletFromGroupResponse]:
        """Remove wallets from a group."""
        # payload = json.dumps([{"wallet": wallet_name, "group": data.group_name} for wallet_name in data.wallet_names])
        payload = data.model_dump(exclude_none=True)['remove_wallets_from_group_requests']
        return await self._api_call("POST", "wallets/remove-wallet-from-group/", payload)

    async def transfer_tokens(self, data: TransferTokensRequestContainer) -> List[TransferTokenResponse]:
        """Transfer tokens from one wallet to another."""
        # payload = [v.model_dump() for v in data.transfer_tokens_requests]
        payload = data.model_dump(exclude_none=True)['transfer_tokens_requests']
        return await self._api_call("POST", "transfers/transfer/", payload)

    async def create_dca_order(self, data: DCAOrderRequestContainer) -> List[DCAOrderResponse]:
        """Create a DCA order."""
        # payload = [v.model_dump() for v in data.dca_order_requests]
        payload = data.model_dump(exclude_none=True)['dca_order_requests']
        return await self._api_call("POST", "transactions/dca-order/create/", payload)

    async def list_dca_orders(self, data: ListDCAOrderRequest) -> ListDCAOrderResponseContainer:
        """List all DCA orders."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", f"transactions/dca-order/", payload)

    async def cancel_dca_order(self, data: CancelDCAOrderRequestContainer) -> List[CancelDCAOrderResponse]:
        """Cancel a DCA order."""
        # payload = [v.model_dump() for v in data.cancel_dca_order_requests]
        payload = data.model_dump(exclude_none=True)['cancel_dca_order_requests']
        return await self._api_call("POST", "transactions/dca-order/cancel/", payload)
    
    async def create_order(self, data: CreateOrderRequestContainer) -> CreateOrderResponseContainer:
        """Create a order."""
        payload = data.model_dump(exclude_none=True)['create_order_requests']
        return await self._api_call("POST", "transactions/order/create/", payload)
    
    async def list_orders(self, data: ListOrderRequest) -> ListOrderResponseContainer:
        """List all orders."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", f"transactions/order/", payload)
    
    async def cancel_order(self, data: CancelOrderRequestContainer) -> CancelOrderResponseContainer:
        """Cancel a order."""
        payload = data.model_dump(exclude_none=True)['cancel_order_requests']
        return await self._api_call("POST", "transactions/order/cancel/", payload) 
    
    async def top_trending_tokens(self, data: TopTrendingTokensRequest) -> List:
        """Get the top trending tokens."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", f"tokens/trending/", payload)
    
    async def get_stake_balances(self) -> StakeBalanceResponse:
        """Get the stake balances."""
        return await self._api_call("GET", "frontend/wallets/stake/balance/")
    
    async def rename_wallet(self, data: RenameWalletRequestContainer) -> List:
        """Rename a wallet."""
        payload = data.model_dump(exclude_none=True)['rename_wallet_requests']
        return await self._api_call("POST", "wallets/rename/", payload)
    
    async def get_market_candle_data(self, data: CandleStickRequest) -> Dict:
        """Get the candle sticks."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", f"tokens/candles/", payload)
    
    async def send_key_to_telegram(self, data: PrivateKeyRequest) -> Dict:
        """Send the mnemonic or private key to telegram."""
        payload = data.model_dump(exclude_none=True)
        return await self._api_call("POST", f"users/telegram/send-message/", payload)

# ------------------------------
# Utility Functions
# ------------------------------   
    
def calculate(expr: str, variables: dict = None) -> float:
    """
    Evaluate a math/stat expression with support for variables and common functions.
    """
    variables = variables or {}
    # Allowed names from math and statistics
    safe_names = {
        k: v for k, v in vars(math).items() if not k.startswith("__")
    }
    safe_names.update({
        'mean': statistics.mean,
        'median': statistics.median,
        'stdev': statistics.stdev,
        'variance': statistics.variance,
        'sum': sum,
        'min': min,
        'max': max,
        'len': len,
        'abs': abs,
        'round': round
    })

    # Safe operators
    ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg
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
