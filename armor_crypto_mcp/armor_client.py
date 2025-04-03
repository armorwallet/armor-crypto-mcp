import json
import os
from pydantic import BaseModel, Field
from typing_extensions import List, Optional, Literal

import httpx
from dotenv import load_dotenv

load_dotenv()
BASE_API_URL = os.getenv("BASE_API_URL")

# Pydantic data models for API client
class WalletTokenPairs(BaseModel):
    wallet: str = Field(description="name of wallet")
    token: str = Field(description="public address of token")


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
    from_wallet: str = Field(description="wallet name")
    input_token: str = Field(description="public address of input token")
    output_token: str = Field(description="public address of output token")
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
    slippage: float = Field(description="slippage percentage")


class SwapTransactionRequest(BaseModel):
    transaction_ids: str = Field(description="unique ids of the generated swap quotes")


class SwapTransactionResponse(BaseModel):
    id: str = Field(description="unique id of the swap transaction")
    transaction_error: Optional[str] = Field(description="error message if the transaction fails")
    transaction_url: str = Field(description="public url of the transaction")
    input_amount: float = Field(description="input amount in input token")
    output_amount: float = Field(description="output amount in output token")
    status: str = Field(description="status of the transaction")


class WalletBalance(BaseModel):
    mint_address: str = Field(description="mint address of the token")
    name: str = Field(description="name of the token")
    symbol: str = Field(description="symbol of the token")
    decimals: int = Field(description="number of decimals of the token")
    amount: float = Field(description="balance of the token")
    usd_price: str = Field(description="price of the token in USD")  # Using str since the API returns price as string
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
    include_details: bool = Field(description="returns only name and address if False, otherwise returns complete details")


class TokenDetailsResponse(BaseModel):
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
    to_wallet_address: str = Field(description="public address of the wallet to transfer tokens to")
    token: str = Field(description="public address of the token to transfer")
    amount: float = Field(description="amount of tokens to transfer")


class TransferTokenResponse(BaseModel):
    amount: float = Field(description="amount of tokens transferred")
    from_wallet_address: str = Field(description="public address of the wallet tokens were transferred from")
    to_wallet_address: str = Field(description="public address of the wallet tokens were transferred to")
    token_address: str = Field(description="public address of the token transferred")
    transaction_url: str = Field(description="public url of the transaction")
    message: str = Field(description="message of the operation showing if tokens were transferred")


class DCAOrderRequest(BaseModel):
    wallet: str = Field(description="name of the wallet")
    input_token: str = Field(description="public address of the input token")
    output_token: str = Field(description="public address of the output token")
    amount: float = Field(description="amount of tokens to invest")
    cron_expression: str = Field(description="cron expression for the DCA order")
    strategy_duration: int = Field(description="duration of the DCA order")
    strategy_duration_unit: Literal["MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "YEAR"] = Field(description="unit of the duration of the DCA order")
    watch_field: str = Field(description="field to watch for the DCA order")
    token_watcher: str = Field(description="name of the token watcher")
    delta_type: Literal["INCREASE", "DECREASE", "MOVE", "MOVE_DAILY", "AVERAGE_MOVE"] = Field(description="type of the delta")
    delta_percentage: float = Field(description="percentage of the delta")
    time_zone: str = Field(description="user's time zone")


class DCAWatcher(BaseModel):
    watch_field: str = Field(description="field to watch for the DCA order")
    delta_type: Literal["INCREASE", "DECREASE", "MOVE", "MOVE_DAILY", "AVERAGE_MOVE"] = Field(description="type of the delta")
    initial_value: float = Field(description="initial value of the delta")
    delta_percentage: float = Field(description="percentage of the delta")


class DCAOrderResponse(BaseModel):
    id: str = Field(description="id of the DCA order")
    amount: float = Field(description="amount of tokens to invest")
    investment_per_cycle: float = Field(description="amount of tokens to invest per cycle")
    cycles_completed: int = Field(description="number of cycles completed")
    total_cycles: int = Field(description="total number of cycles")
    human_readable_expiry: str = Field(description="human readable expiry date of the DCA order")
    status: str = Field(description="status of the DCA order")
    input_token_address: str = Field(description="public address of the input token")
    output_token_address: str = Field(description="public address of the output token")
    wallet_name: str = Field(description="name of the wallet")
    watchers: List[DCAWatcher] = Field(description="list of watchers for the DCA order")
    dca_transactions: List[dict] = Field(description="list of DCA transactions")  # Can be further typed if transaction structure is known


class CancelDCAOrderRequest(BaseModel):
    dca_order_id: str = Field(description="id of the DCA order")


class CancelDCAOrderResponse(BaseModel):
    dca_order_id: str = Field(description="id of the DCA order")
    status: str = Field(description="status of the DCA order")


class ArmorWalletAPIClient:
    def __init__(self, access_token: str, base_api_url:str='https://app.armorwallet.ai/api/v1'):
        self.base_api_url = base_api_url
        self.access_token = access_token

    async def _api_call(self, method: str, endpoint: str, payload: str = None) -> dict:
        """Utility function for API calls to the wallet.
           It sets common headers and raises errors on non-2xx responses.
        """
        url = f"{self.base_api_url}/{endpoint}"
        print(url)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.request(method, url, headers=headers, data=payload)
        if response.status_code >= 400:
            raise Exception(f"API Error {response.status_code}: {response.text}")
        try:
            return response.json()
        except Exception:
            return {"text": response.text}

    async def get_wallet_token_balance(self, wallet_token_pairs: List[WalletTokenPairs]) -> List[WalletTokenBalance]:
        """Get balances from a list of wallet and token pairs.
        """
        payload = json.dumps(wallet_token_pairs)
        return await self._api_call("POST", "tokens/wallet-token-balance/", payload)

    async def conversion_api(self, conversion_request: List[ConversionRequest]) -> List[ConversionResponse]:
        """Perform a token conversion."""
        payload = json.dumps(conversion_request)
        return await self._api_call("POST", "tokens/token-price-conversion/", payload)

    async def swap_quote(self, swap_quote_requests: List[SwapQuoteRequest]) -> List[SwapQuoteResponse]:
        """Obtain a swap quote."""
        payload = json.dumps(swap_quote_requests)
        return await self._api_call("POST", "transactions/quote/", payload)

    async def swap_transaction(self, swap_transaction_requests: List[SwapTransactionRequest]) -> List[SwapTransactionResponse]:
        """Execute the swap transactions."""
        payload = json.dumps(swap_transaction_requests)
        return await self._api_call("POST", "transactions/swap/", payload)

    async def get_wallets_from_group(self, group_name: str) -> list:
        """Return the list of wallet names from the specified group."""
        result = await self._api_call("GET", f"wallets/groups/{group_name}")
        try:
            return [wallet['name'] for wallet in result['wallets']]
        except Exception:
            return []

    async def get_all_wallets(self) -> List[Wallet]:
        """Return all wallets with balances."""
        return await self._api_call("GET", "wallets/")

    async def get_token_details(self, token_details_requests: List[TokenDetailsRequest]) -> List[TokenDetailsResponse]:
        """Retrieve token details."""
        payload = json.dumps(token_details_requests)
        return await self._api_call("POST", "tokens/search-token/", payload)

    async def list_groups(self) -> List[GroupInfo]:
        """Return a list of wallet groups."""
        return await self._api_call("GET", "wallets/groups/")

    async def list_single_group(self, group_name: str) -> SingleGroupInfo:
        """Return details for a single wallet group."""
        return await self._api_call("GET", f"wallets/groups/{group_name}")

    async def create_wallet(self, wallet_names_list: list) -> List[WalletInfo]:
        """Create new wallets given a list of wallet names."""
        payload = json.dumps([{"name": wallet_name} for wallet_name in wallet_names_list])
        return await self._api_call("POST", "wallets/", payload)

    async def archive_wallets(self, wallet_names_list: list) -> List[WalletArchiveOrUnarchiveResponse]:
        """Archive the wallets specified in the list."""
        payload = json.dumps([{"wallet": wallet_name} for wallet_name in wallet_names_list])
        return await self._api_call("POST", "wallets/archive/", payload)

    async def unarchive_wallets(self, wallet_names_list: list) -> List[WalletArchiveOrUnarchiveResponse]:
        """Unarchive the wallets specified in the list."""
        payload = json.dumps([{"wallet": wallet_name} for wallet_name in wallet_names_list])
        return await self._api_call("POST", "wallets/unarchive/", payload)

    async def create_groups(self, group_names_list: list) -> List[CreateGroupResponse]:
        """Create new wallet groups given a list of group names."""
        payload = json.dumps([{"name": group_name} for group_name in group_names_list])
        return await self._api_call("POST", "wallets/groups/", payload)

    async def add_wallets_to_group(self, group_name: str, wallet_names_list: list) -> List[AddWalletToGroupResponse]:
        """Add wallets to a specific group."""
        payload = json.dumps([{"wallet": wallet_name, "group": group_name} for wallet_name in wallet_names_list])
        return await self._api_call("POST", "wallets/add-wallet-to-group/", payload)

    async def archive_wallet_group(self, group_names_list: list) -> List[GroupArchiveOrUnarchiveResponse]:
        """Archive the specified wallet groups."""
        payload = json.dumps([{"group": group_name} for group_name in group_names_list])
        return await self._api_call("POST", "wallets/group-archive/", payload)

    async def unarchive_wallet_group(self, group_names_list: list) -> List[GroupArchiveOrUnarchiveResponse]:
        """Unarchive the specified wallet groups."""
        payload = json.dumps([{"group": group_name} for group_name in group_names_list])
        return await self._api_call("POST", "wallets/group-unarchive/", payload)

    async def remove_wallets_from_group(self, group_name: str, wallet_names_list: list) -> List[RemoveWalletFromGroupResponse]:
        """Remove wallets from a group."""
        payload = json.dumps([{"wallet": wallet_name, "group": group_name} for wallet_name in wallet_names_list])
        return await self._api_call("POST", "wallets/remove-wallet-from-group/", payload)

    async def get_user_wallets_and_groups_list(self) -> UserWalletsAndGroupsResponse:
        """Return user wallets and groups."""
        return await self._api_call("GET", "users/me/")

    async def transfer_tokens(self, transfer_tokens_requests: List[TransferTokensRequest]) -> List[TransferTokenResponse]:
        """Transfer tokens from one wallet to another."""
        payload = json.dumps(transfer_tokens_requests)
        return await self._api_call("POST", "transfers/transfer/", payload)

    async def create_dca_order(self, dca_order_requests: List[DCAOrderRequest]) -> List[DCAOrderResponse]:
        """Create a DCA order."""
        payload = json.dumps(dca_order_requests)
        return await self._api_call("POST", "transactions/dca-order/", payload)

    async def list_dca_orders(self) -> List[DCAOrderResponse]:
        """List all DCA orders."""
        return await self._api_call("GET", "transactions/dca-order/")

    async def cancel_dca_order(self, cancel_dca_order_requests: List[CancelDCAOrderRequest]) -> List[CancelDCAOrderResponse]:
        """Cancel a DCA order."""
        payload = json.dumps(cancel_dca_order_requests)
        return await self._api_call("POST", "transactions/dca-order/cancel/", payload)

