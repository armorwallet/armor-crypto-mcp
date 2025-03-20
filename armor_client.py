import json
import os
from typing import List, Optional, TypedDict, Literal

import httpx
from dotenv import load_dotenv

load_dotenv()
BASE_API_URL = os.getenv("BASE_API_URL")

# Pydantic data models for API client
class WalletTokenPairs(TypedDict):
    wallet: str
    token: str

class WalletTokenBalance(TypedDict):
    wallet: str
    token: str
    balance: float

class ConversionRequest(TypedDict):
    input_amount: float
    input_token: str
    output_token: str

class ConversionResponse(TypedDict):
    input_amount: float
    input_token: str
    output_token: str
    output_amount: float

class SwapQuoteRequest(TypedDict):
    from_wallet: str
    input_token: str
    output_token: str
    input_amount: float

class SwapQuoteResponse(TypedDict):
    id: str
    wallet_address: str
    input_token_symbol: str
    input_token_address: str
    output_token_symbol: str
    output_token_address: str
    input_amount: float
    output_amount: float
    slippage: float

class SwapTransactionRequest(TypedDict):
    transaction_ids: str

class SwapTransactionResponse(TypedDict):
    id: str
    transaction_error: Optional[str]
    transaction_url: str
    input_amount: float
    output_amount: float
    status: str
    buying_price: float

class WalletBalance(TypedDict):
    mint_address: str
    name: str
    symbol: str
    decimals: int
    amount: float
    usd_price: str  # Using str since the API returns price as string
    usd_amount: float

class WalletInfo(TypedDict):
    id: str
    name: str
    is_archived: bool
    public_address: str

class Wallet(WalletInfo):  # All fields required
    balances: List[WalletBalance]

class TokenDetailsRequest(TypedDict):
    query: str
    include_details: bool

class TokenDetailsResponse(TypedDict):
    name: str
    symbol: str
    mint_address: Optional[str]  # if include_details is true
    decimals: Optional[int]
    image: Optional[str]
    holders: Optional[int]
    jupiter: Optional[bool]
    verified: Optional[bool]
    liquidityUsd: Optional[float]
    marketCapUsd: Optional[float]
    priceUsd: Optional[float]
    lpBurn: Optional[float]
    market: Optional[str]
    freezeAuthority: Optional[str]
    mintAuthority: Optional[str]
    poolAddress: Optional[str]
    totalBuys: Optional[int]
    totalSells: Optional[int]
    totalTransactions: Optional[int]
    volume: Optional[float]
    volume_5m: Optional[float]
    volume_15m: Optional[float]
    volume_30m: Optional[float]
    volume_1h: Optional[float]
    volume_6h: Optional[float]
    volume_12h: Optional[float]
    volume_24h: Optional[float]

class GroupInfo(TypedDict):
    id: str
    name: str
    is_archived: bool

class SingleGroupInfo(GroupInfo):  # All fields required
    wallets: List[WalletInfo]

class WalletArchiveOrUnarchiveResponse(TypedDict):
    wallet_name: str
    message: str

class CreateGroupResponse(TypedDict):
    id: str
    name: str
    is_archived: bool

class AddWalletToGroupResponse(TypedDict):
    wallet_name: str
    group_name: str
    message: str

class GroupArchiveOrUnarchiveResponse(TypedDict):
    group: str

class RemoveWalletFromGroupResponse(TypedDict):
    wallet: str
    group: str

class UserWalletsAndGroupsResponse(TypedDict):
    id: str
    email: str
    first_name: str
    last_name: str
    slippage: float
    wallet_groups: List[GroupInfo]
    wallets: List[WalletInfo]

class TransferTokensRequest(TypedDict):
    from_wallet: str
    to_wallet_address: str
    token: str
    amount: float

class TransferTokenResponse(TypedDict):
    amount: float
    from_wallet_address: str
    to_wallet_address: str
    token_address: str
    transaction_url: str
    message: str


class DCAOrderRequest(TypedDict):
    wallet: str
    input_token: str
    output_token: str
    amount: float
    cron_expression: str
    strategy_duration: int
    strategy_duration_unit: Literal["MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "YEAR"]
    watch_field: str
    token_watcher: str
    delta_type: Literal["INCREASE", "DECREASE", "MOVE", "MOVE_DAILY", "AVERAGE_MOVE"]
    delta_percentage: float
    time_zone: str


class DCAWatcher(TypedDict):
    watch_field: str
    delta_type: Literal["INCREASE", "DECREASE", "MOVE", "MOVE_DAILY", "AVERAGE_MOVE"]
    initial_value: float
    delta_percentage: float


class DCAOrderResponse(TypedDict):
    id: str
    amount: float
    investment_per_cycle: float
    cycles_completed: int
    total_cycles: int
    human_readable_expiry: str
    status: str
    input_token_address: str
    output_token_address: str
    wallet_name: str
    watchers: List[DCAWatcher]
    dca_transactions: List[dict]  # Can be further typed if transaction structure is known


class CancelDCAOrderRequest(TypedDict):
    dca_order_id: str


class CancelDCAOrderResponse(TypedDict):
    dca_order_id: str
    status: str


class ArmorWalletAPIClient:
    def __init__(self, access_token: str):
        self.access_token = access_token

    async def _api_call(self, method: str, endpoint: str, payload: str = None) -> dict:
        """Utility function for API calls to the wallet.
           It sets common headers and raises errors on non-2xx responses.
        """
        url = f"https://{BASE_API_URL}.armorwallet.ai/api/v1/{endpoint}"
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

    async def login(self, email: str, password: str) -> dict:
        """Log in to the wallet API."""
        payload = json.dumps({"email": email, "password": password})
        result = await self._api_call("POST", "users/login/", payload)
        self.access_token = result.get('access')
        return result

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

