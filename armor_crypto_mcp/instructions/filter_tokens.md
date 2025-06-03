# Filter Tokens

Returns a list of tokens based on a variety of filters.

## Endpoint Details

- **Endpoint**: `filterTokens`
- **Method**: POST

## Arguments

| Name          | Type                    | Description                                                                                                                                |
| ------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| excludeTokens | [String]                | A list of token IDs (address:networkId) to exclude from results                                                                            |
| filters       | TokenFilters            | A set of filters to apply                                                                                                                  |
| limit         | Int                     | The maximum number of tokens to return                                                                                                     |
| offset        | Int                     | Where in the list the server should start when returning items. Use count+page from the previous query to request the next page of results |
| phrase        | String                  | A phrase to search for. Can match a token contract address or partially match a token's name or symbol                                     |
| rankings      | [TokenRanking]          | A list of ranking attributes to apply                                                                                                      |
| statsType     | TokenPairStatisticsType | The type of statistics returned. Can be FILTERED or UNFILTERED                                                                             |
| tokens        | [String]                | A list of token IDs (address:networkId) or addresses. Can be left blank to discover new tokens                                             |

## TokenRanking

Input type of TokenRanking.

### Input Fields

| Name      | Description                                     |
| --------- | ----------------------------------------------- |
| attribute | The attribute to rank tokens by                 |
| direction | The direction to apply to the ranking attribute |

## TokenRankingAttribute

The attribute used to rank tokens.

### Values

- age
- buyCount1
- buyCount4
- buyCount5m
- buyCount12
- buyCount24
- buyVolume1
- buyVolume4
- buyVolume5m
- buyVolume12
- buyVolume24
- change1
- change4
- change5m
- change12
- change24
- circulatingMarketCap
- createdAt
- graduationPercent
- high1
- high4
- high5m
- high12
- high24
- holders
- lastTransaction
- launchpadCompletedAt
- launchpadMigratedAt
- liquidity
- low1
- low4
- low5m
- low12
- low24
- marketCap
- notableHolderCount
- priceUSD
- sellCount1
- sellCount4
- sellCount5m
- sellCount12
- sellCount24
- sellVolume1
- sellVolume4
- sellVolume5m
- sellVolume12
- sellVolume24
- swapPct1dOldWallet
- swapPct7dOldWallet
- trendingScore
- trendingScore1
- trendingScore4
- trendingScore5m
- trendingScore12
- trendingScore24
- txnCount1
- txnCount4
- txnCount5m
- txnCount12
- txnCount24
- uniqueBuys1
- uniqueBuys4
- uniqueBuys5m
- uniqueBuys12
- uniqueBuys24
- uniqueSells1
- uniqueSells4
- uniqueSells5m
- uniqueSells12
- uniqueSells24
- uniqueTransactions1
- uniqueTransactions4
- uniqueTransactions5m
- uniqueTransactions12
- uniqueTransactions24
- volume1
- volume4
- volume5m
- volume12
- volume24
- volumeChange1
- volumeChange4
- volumeChange5m
- volumeChange12
- volumeChange24
- walletAgeAvg
- walletAgeStd

## RankingDirection

The order of ranking.

### Values

- ASC
- DESC

## TokenPairStatisticsType

The type of statistics returned. Can be FILTERED or UNFILTERED

### Values

- FILTERED
- UNFILTERED

## Response

### TokenFilterConnection

| Name    | Type                | Description                                               |
| ------- | ------------------- | --------------------------------------------------------- |
| count   | Int                 | The number of tokens returned                             |
| page    | Int                 | Where in the list the server started when returning items |
| results | [TokenFilterResult] | The list of tokens matching the filter parameters         |

### TokenFilterResult

| Name                 | Type          | Description                                                                          |
| -------------------- | ------------- | ------------------------------------------------------------------------------------ |
| buyCount1            | Int           | The number of buys in the past hour                                                  |
| buyCount4            | Int           | The number of buys in the past 4 hours                                               |
| buyCount5m           | Int           | The number of buys in the past 5 minutes                                             |
| buyCount12           | Int           | The number of buys in the past 12 hours                                              |
| buyCount24           | Int           | The number of buys in the past 24 hours                                              |
| buyVolume1           | String        | The buy volume in USD in the past hour                                               |
| buyVolume4           | String        | The buy volume in USD in the past 4 hours                                            |
| buyVolume5m          | String        | The buy volume in USD in the past 5 minutes                                          |
| buyVolume12          | String        | The buy volume in USD in the past 12 hours                                           |
| buyVolume24          | String        | The buy volume in USD in the past 24 hours                                           |
| change1              | String        | The percent price change in the past hour. Decimal format                            |
| change4              | String        | The percent price change in the past 4 hours. Decimal format                         |
| change5m             | String        | The percent price change in the past 5 minutes. Decimal format                       |
| change12             | String        | The percent price change in the past 12 hours. Decimal format                        |
| change24             | String        | The percent price change in the past 24 hours. Decimal format                        |
| circulatingMarketCap | String        | The circulating market cap                                                           |
| createdAt            | Int           | The unix timestamp for the creation of the token's first pair                        |
| exchanges            | [Exchange]    | The exchanges the token is listed on                                                 |
| high1                | String        | The highest price in USD in the past hour                                            |
| high4                | String        | The highest price in USD in the past 4 hours                                         |
| high5m               | String        | The highest price in USD in the past 5 minutes                                       |
| high12               | String        | The highest price in USD in the past 12 hours                                        |
| high24               | String        | The highest price in USD in the past 24 hours                                        |
| holders              | Int           | The number of different wallets holding the token                                    |
| isScam               | Boolean       | Whether the token has been flagged as a scam                                         |
| lastTransaction      | Int           | The unix timestamp for the token's last transaction                                  |
| liquidity            | String        | Amount of liquidity in the token's top pair                                          |
| low1                 | String        | The lowest price in USD in the past hour                                             |
| low4                 | String        | The lowest price in USD in the past 4 hours                                          |
| low5m                | String        | The lowest price in USD in the past 5 minutes                                        |
| low12                | String        | The lowest price in USD in the past 12 hours                                         |
| low24                | String        | The lowest price in USD in the past 24 hours                                         |
| marketCap            | String        | The fully diluted market cap                                                         |
| pair                 | Pair          | Metadata for the token's top pair                                                    |
| priceUSD             | String        | The token price in USD                                                               |
| quoteToken           | String        | The token of interest. Can be token0 or token1                                       |
| sellCount1           | Int           | The number of sells in the past hour                                                 |
| sellCount4           | Int           | The number of sells in the past 4 hours                                              |
| sellCount5m          | Int           | The number of sells in the past 5 minutes                                            |
| sellCount12          | Int           | The number of sells in the past 12 hours                                             |
| sellCount24          | Int           | The number of sells in the past 24 hours                                             |
| sellVolume1          | String        | The sell volume in USD in the past hour                                              |
| sellVolume4          | String        | The sell volume in USD in the past 4 hours                                           |
| sellVolume5m         | String        | The sell volume in USD in the past 5 minutes                                         |
| sellVolume12         | String        | The sell volume in USD in the past 12 hours                                          |
| sellVolume24         | String        | The sell volume in USD in the past 24 hours                                          |
| swapPct1dOldWallet   | String        | The percentage of wallets that are less than 1d old that have traded in the last 24h |
| swapPct7dOldWallet   | String        | The percentage of wallets that are less than 7d old that have traded in the last 24h |
| token                | EnhancedToken | Metadata for the token                                                               |
| txnCount1            | Int           | The number of transactions in the past hour                                          |
| txnCount4            | Int           | The number of transactions in the past 4 hours                                       |
| txnCount5m           | Int           | The number of transactions in the past 5 minutes                                     |
| txnCount12           | Int           | The number of transactions in the past 12 hours                                      |
| txnCount24           | Int           | The number of transactions in the past 24 hours                                      |
| uniqueBuys1          | Int           | The unique number of buys in the past hour                                           |
| uniqueBuys4          | Int           | The unique number of buys in the past 4 hours                                        |
| uniqueBuys5m         | Int           | The unique number of buys in the past 5 minutes                                      |
| uniqueBuys12         | Int           | The unique number of buys in the past 12 hours                                       |
| uniqueBuys24         | Int           | The unique number of buys in the past 24 hours                                       |
| uniqueSells1         | Int           | The unique number of sells in the past hour                                          |
| uniqueSells4         | Int           | The unique number of sells in the past 4 hours                                       |
| uniqueSells5m        | Int           | The unique number of sells in the past 5 minutes                                     |
| uniqueSells12        | Int           | The unique number of sells in the past 12 hours                                      |
| uniqueSells24        | Int           | The unique number of sells in the past 24 hours                                      |
| uniqueTransactions1  | Int           | The unique number of transactions in the past hour                                   |
| uniqueTransactions4  | Int           | The unique number of transactions in the past 4 hours                                |
| uniqueTransactions5m | Int           | The unique number of transactions in the past 5 minutes                              |
| uniqueTransactions12 | Int           | The unique number of transactions in the past 12 hours                               |
| uniqueTransactions24 | Int           | The unique number of transactions in the past 24 hours                               |
| volume1              | String        | The trade volume in USD in the past hour                                             |
| volume4              | String        | The trade volume in USD in the past 4 hours                                          |
| volume5m             | String        | The trade volume in USD in the past 5 minutes                                        |
| volume12             | String        | The trade volume in USD in the past 12 hours                                         |
| volume24             | String        | The trade volume in USD in the past 24 hours                                         |
| volumeChange1        | String        | The percent volume change in the past hour. Decimal format                           |
| volumeChange4        | String        | The percent volume change in the past 4 hours. Decimal format                        |
| volumeChange5m       | String        | The percent volume change in the past 5 minutes. Decimal format                      |
| volumeChange12       | String        | The percent volume change in the past 12 hours. Decimal format                       |
| volumeChange24       | String        | The percent volume change in the past 24 hours. Decimal format                       |
| walletAgeAvg         | String        | The average age of the wallets that traded in the last 24h                           |
| walletAgeStd         | String        | The standard deviation of age of the wallets that traded in the last 24h             |

## Exchange

Metadata for a decentralized exchange.

### Fields

| Name            | Type   | Description                                |
| --------------- | ------ | ------------------------------------------ |
| address         | String | The contract address of the exchange       |
| color           | String | The hex string for the exchange color      |
| exchangeVersion | String | The version of the exchange, if applicable |
| iconUrl         | String | The exchange logo URL                      |
| id              | String | The ID of the exchange (address:id)        |
| name            | String | The name of the exchange                   |
| networkId       | Int    | The network ID the exchange is deployed on |
| tradeUrl        | String | The URL for the exchange                   |

## Pair

Metadata for a token pair.

### Fields

| Name         | Type              | Description                                                                    |
| ------------ | ----------------- | ------------------------------------------------------------------------------ |
| address      | String            | The contract address of the pair                                               |
| createdAt    | Int               | The unix timestamp for the creation of the pair                                |
| exchangeHash | String            | The address for the exchange factory contract                                  |
| fee          | Int               | The exchange fee for swaps                                                     |
| id           | String            | The ID for the pair (address:networkId)                                        |
| networkId    | Int               | The network ID the pair is deployed on                                         |
| pooled       | PooledTokenValues | The pooled amounts of each token in the pair                                   |
| tickSpacing  | Int               | The amount of required tick separation. Only applicable for pairs on UniswapV3 |
| token0       | String            | The contract address of token0                                                 |
| token0Data   | EnhancedToken     | Metadata for the first token in the pair                                       |
| token1       | String            | The contract address of token1                                                 |
| token1Data   | EnhancedToken     | Metadata for the second token in the pair                                      |

## EnhancedToken

Metadata for a token.

### Fields

| Name                  | Type              | Description                                            |
| --------------------- | ----------------- | ------------------------------------------------------ |
| address               | String            | The contract address of the token                      |
| circulatingSupply     | String            | The circulating supply of the token                    |
| cmcId                 | Int               | The token ID on CoinMarketCap                          |
| createBlockNumber     | Int               | The block height the token was created at              |
| createdAt             | Int               | The unix timestamp for the creation of the token       |
| createTransactionHash | String            | The transaction hash of the token's creation           |
| creatorAddress        | String            | The token creator's wallet address                     |
| decimals              | Int               | The precision to which the token can be divided        |
| exchanges             | [Exchange]        | A list of exchanges where the token has been traded    |
| explorerData          | ExplorerTokenData | Information about the token from 3rd party sources     |
| freezable             | String            | Whether or not the token is freezable                  |
| id                    | String            | The ID of the token (address:networkId)                |
| imageLargeUrl         | String            | The large token logo URL                               |
| imageSmallUrl         | String            | The small token logo URL                               |
| imageThumbUrl         | String            | The thumbnail token logo URL                           |
| info                  | TokenInfo         | More metadata about the token                          |
| isScam                | Boolean           | Whether the token has been flagged as a scam           |
| launchpad             | LaunchpadData     | The launchpad data for the token, if applicable        |
| mintable              | String            | Whether or not the token is mintable                   |
| name                  | String            | The token name                                         |
| networkId             | Int               | The network ID the token is deployed on                |
| pooled                | String            | The amount of this token in the pair                   |
| socialLinks           | SocialLinks       | Community gathered links for the socials of this token |
| symbol                | String            | The token symbol                                       |
| totalSupply           | String            | The total supply of the token                          |

## PooledTokenValues

The pooled amounts of each token in a pair.

### Fields

| Name   | Type   | Description                      |
| ------ | ------ | -------------------------------- |
| token0 | String | The amount of token0 in the pool |
| token1 | String | The amount of token1 in the pool |

## ExplorerTokenData

Third party token data sourced from off chain.

### Fields

| Name          | Type    | Description                                      |
| ------------- | ------- | ------------------------------------------------ |
| blueCheckmark | Boolean | Whether the token has been verified on CoinGecko |
| description   | String  | A description of the token                       |
| divisor       | String  | The precision to which the token can be divided  |
| id            | String  | The ID of the token (address:networkId)          |
| tokenPriceUSD | String  | The token price in USD                           |
| tokenType     | String  | The token type                                   |

## TokenInfo

Metadata for a token.

### Fields

| Name              | Type    | Description                                  |
| ----------------- | ------- | -------------------------------------------- |
| address           | String  | The contract address of the token            |
| circulatingSupply | String  | The circulating supply of the token          |
| cmcId             | Int     | The token ID on CoinMarketCap                |
| description       | String  | A description of the token                   |
| id                | String  | Uniquely identifies the token                |
| imageBannerUrl    | String  | The token banner URL                         |
| imageLargeUrl     | String  | The large token logo URL                     |
| imageSmallUrl     | String  | The small token logo URL                     |
| imageThumbUrl     | String  | The thumbnail token logo URL                 |
| isScam            | Boolean | Whether the token has been flagged as a scam |
| name              | String  | The token name                               |
| networkId         | Int     | The network ID the token is deployed on      |
| symbol            | String  | The token symbol                             |
| totalSupply       | String  | The total supply of the token                |

## LaunchpadData

Launchpad information for a token.

### Fields

| Name                | Type    | Description                                               |
| ------------------- | ------- | --------------------------------------------------------- |
| completed           | Boolean | Indicates if the launchpad is completed                   |
| completedAt         | Int     | The unix timestamp when the launchpad was completed       |
| completedSlot       | Int     | The slot number when the launchpad was completed          |
| graduationPercent   | Float   | The percentage of the pool that was sold to the public    |
| launchpadName       | String  | The name of the launchpad                                 |
| launchpadProtocol   | String  | The launchpad protocol                                    |
| migrated            | Boolean | Indicates if the launchpad was migrated                   |
| migratedAt          | Int     | The unix timestamp when the launchpad was migrated        |
| migratedPoolAddress | String  | The pool address after the launchpad was migrated         |
| migratedSlot        | Int     | The slot number when the launchpad was migrated           |
| name                | String  | The name of the launchpad (DEPRECATED: Use launchpadName) |
| poolAddress         | String  | The address of the pool                                   |

## SocialLinks

Community gathered social links of tokens/NFTs.

### Fields

| Name          | Type   | Description       |
| ------------- | ------ | ----------------- |
| bitcointalk   | String | BitcoinTalk URL   |
| blog          | String | Blog URL          |
| coingecko     | String | CoinGecko URL     |
| coinmarketcap | String | CoinMarketCap URL |
| discord       | String | Discord URL       |
| email         | String | Email address     |
| facebook      | String | Facebook URL      |
| github        | String | GitHub URL        |
| instagram     | String | Instagram URL     |
| linkedin      | String | LinkedIn URL      |
| reddit        | String | Reddit URL        |
| slack         | String | Slack URL         |
| telegram      | String | Telegram URL      |
| twitch        | String | Twitch URL        |
| twitter       | String | Twitter URL       |
| website       | String | Website URL       |
| wechat        | String | WeChat URL        |
| whitepaper    | String | Whitepaper URL    |
| youtube       | String | YouTube URL       |

## NumberFilter

Input type of NumberFilter.

### Input Fields

| Name | Type  | Description              |
| ---- | ----- | ------------------------ |
| gt   | Float | Greater than             |
| gte  | Float | Greater than or equal to |
| lt   | Float | Less than                |
| lte  | Float | Less than or equal to    |

## TokenFilters

Input type of TokenFilters.

### Input Fields

| Name                       | Description                                                                                                                                                                                                                        |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| age                        | NumberFilter                                                                                                                                                                                                                       |
| buyCount1                  | The number of buys in the past hour                                                                                                                                                                                                |
| buyCount4                  | The number of buys in the past 4 hours                                                                                                                                                                                             |
| buyCount5m                 | The number of buys in the past 5 minutes                                                                                                                                                                                           |
| buyCount12                 | The number of buys in the past 12 hours                                                                                                                                                                                            |
| buyCount24                 | The number of buys in the past 24 hours                                                                                                                                                                                            |
| buyVolume1                 | The buy volume in USD in the past hour                                                                                                                                                                                             |
| buyVolume4                 | The buy volume in USD in the past 4 hours                                                                                                                                                                                          |
| buyVolume5m                | The buy volume in USD in the past 5 minutes                                                                                                                                                                                        |
| buyVolume12                | The buy volume in USD in the past 12 hours                                                                                                                                                                                         |
| buyVolume24                | The buy volume in USD in the past 24 hours                                                                                                                                                                                         |
| change1                    | The percent price change in the past hour. Decimal format                                                                                                                                                                          |
| change4                    | The percent price change in the past 4 hours. Decimal format                                                                                                                                                                       |
| change5m                   | The percent price change in the past 5 minutes. Decimal format                                                                                                                                                                     |
| change12                   | The percent price change in the past 12 hours. Decimal format                                                                                                                                                                      |
| change24                   | The percent price change in the past 24 hours. Decimal format                                                                                                                                                                      |
| circulatingMarketCap       | The circulating market cap                                                                                                                                                                                                         |
| createdAt                  | The unix timestamp for the creation of the token's first pair                                                                                                                                                                      |
| creatorAddress             | The address of the creator of the token                                                                                                                                                                                            |
| exchangeAddress            | The list of exchange contract addresses to filter by                                                                                                                                                                               |
| exchangeId                 | The list of exchange contract IDs to filter by. Applied in conjunction with network filter using an OR condition. When used together, the query returns results that match either the specified exchanges or the specified network |
| fdv                        | NumberFilter                                                                                                                                                                                                                       |
| freezable                  | The token in freezable                                                                                                                                                                                                             |
| high1                      | The highest price in USD in the past hour                                                                                                                                                                                          |
| high4                      | The highest price in USD in the past 4 hours                                                                                                                                                                                       |
| high5m                     | The highest price in USD in the past 5 minutes                                                                                                                                                                                     |
| high12                     | The highest price in USD in the past 12 hours                                                                                                                                                                                      |
| high24                     | The highest price in USD in the past 24 hours                                                                                                                                                                                      |
| holders                    | The number of different wallets holding the token                                                                                                                                                                                  |
| includeScams               | Whether to include tokens that have been flagged as scams. Default: false                                                                                                                                                          |
| isTestnet                  | Whether to filter for tokens on testnet networks. Use true for testnet tokens only, false for mainnet tokens only and undefined (default) for both                                                                                 |
| isVerified                 | Only include verified tokens                                                                                                                                                                                                       |
| lastTransaction            | The unix timestamp for the token's last transaction                                                                                                                                                                                |
| launchpadCompleted         | Indicates if the launchpad is completed                                                                                                                                                                                            |
| launchpadCompletedAt       | The timestamp when the launchpad was completed                                                                                                                                                                                     |
| launchpadGraduationPercent | The graduation percentage                                                                                                                                                                                                          |
| launchpadMigrated          | Indicates if the launchpad has migrated                                                                                                                                                                                            |
| launchpadMigratedAt        | The timestamp when the launchpad was migrated                                                                                                                                                                                      |
| launchpadName              | The name of the launchpad                                                                                                                                                                                                          |
| launchpadProtocol          | The launchpad protocol                                                                                                                                                                                                             |
| liquidity                  | The amount of liquidity in the token's top pair                                                                                                                                                                                    |
| low1                       | The lowest price in USD in the past hour                                                                                                                                                                                           |
| low4                       | The lowest price in USD in the past 4 hours                                                                                                                                                                                        |
| low5m                      | The lowest price in USD in the past 5 minutes                                                                                                                                                                                      |
| low12                      | The lowest price in USD in the past 12 hours                                                                                                                                                                                       |
| low24                      | The lowest price in USD in the past 24 hours                                                                                                                                                                                       |
| marketCap                  | The market cap of circulating supply                                                                                                                                                                                               |
| mintable                   | The token in mintable                                                                                                                                                                                                              |
| network                    | The list of network IDs to filter by. Applied in conjunction with exchangeId filter using an OR condition. When used together, the query returns results that match either the specified exchanges or the specified network.       |
| potentialScam              | Filter potential Scams                                                                                                                                                                                                             |
| priceUSD                   | The token price in USD                                                                                                                                                                                                             |
| sellCount1                 | The number of sells in the past hour                                                                                                                                                                                               |
| sellCount4                 | The number of sells in the past 4 hours                                                                                                                                                                                            |
| sellCount5m                | The number of sells in the past 5 minutes                                                                                                                                                                                          |
| sellCount12                | The number of sells in the past 12 hours                                                                                                                                                                                           |
| sellCount24                | The number of sells in the past 24 hours                                                                                                                                                                                           |
| sellVolume1                | The sell volume in USD in the past hour                                                                                                                                                                                            |
| sellVolume4                | The sell volume in USD in the past 4 hours                                                                                                                                                                                         |
| sellVolume5m               | The sell volume in USD in the past 5 minutes                                                                                                                                                                                       |
| sellVolume12               | The sell volume in USD in the past 12 hours                                                                                                                                                                                        |
| sellVolume24               | The sell volume in USD in the past 24 hours                                                                                                                                                                                        |
| swapPct1dOldWallet         | The percentage of wallets that are less than 1d old that have traded in the last 24h                                                                                                                                               |
| swapPct7dOldWallet         | The percentage of wallets that are less than 7d old that have traded in the last 24h                                                                                                                                               |
| trendingIgnored            | Whether to ignore pairs/tokens not relevant to trending                                                                                                                                                                            |
| txnCount1                  | The number of transactions in the past hour                                                                                                                                                                                        |
| txnCount4                  | The number of transactions in the past 4 hours                                                                                                                                                                                     |
| txnCount5m                 | The number of transactions in the past 5 minutes                                                                                                                                                                                   |
| txnCount12                 | The number of transactions in the past 12 hours                                                                                                                                                                                    |
| txnCount24                 | The number of transactions in the past 24 hours                                                                                                                                                                                    |
| uniqueBuys1                | The unique number of buys in the past hour                                                                                                                                                                                         |
| uniqueBuys4                | The unique number of buys in the past 4 hours                                                                                                                                                                                      |
| uniqueBuys5m               | The unique number of buys in the past 5 minutes                                                                                                                                                                                    |
| uniqueBuys12               | The unique number of buys in the past 12 hours                                                                                                                                                                                     |
| uniqueBuys24               | The unique number of buys in the past 24 hours                                                                                                                                                                                     |
| uniqueSells1               | The unique number of sells in the past hour                                                                                                                                                                                        |
| uniqueSells4               | The unique number of sells in the past 4 hours                                                                                                                                                                                     |
| uniqueSells5m              | The unique number of sells in the past 5 minutes                                                                                                                                                                                   |
| uniqueSells12              | The unique number of sells in the past 12 hours                                                                                                                                                                                    |
| uniqueSells24              | The unique number of sells in the past 24 hours                                                                                                                                                                                    |
| uniqueTransactions1        | The unique number of transactions in the past hour                                                                                                                                                                                 |
| uniqueTransactions4        | The unique number of transactions in the past 4 hours                                                                                                                                                                              |
| uniqueTransactions5m       | The unique number of transactions in the past 5 minutes                                                                                                                                                                            |
| uniqueTransactions12       | The unique number of transactions in the past 12 hours                                                                                                                                                                             |
| uniqueTransactions24       | The unique number of transactions in the past 24 hours                                                                                                                                                                             |
| volume1                    | The trade volume in USD in the past hour                                                                                                                                                                                           |
| volume4                    | The trade volume in USD in the past 4 hours                                                                                                                                                                                        |
| volume5m                   | The trade volume in USD in the past 5 minutes                                                                                                                                                                                      |
| volume12                   | The trade volume in USD in the past 12 hours                                                                                                                                                                                       |
| volume24                   | The trade volume in USD in the past 24 hours                                                                                                                                                                                       |
| volumeChange1              | The percent volume change in the past hour. Decimal format                                                                                                                                                                         |
| volumeChange4              | The percent volume change in the past 4 hours. Decimal format                                                                                                                                                                      |
| volumeChange5m             | The percent volume change in the past 5 minutes. Decimal format                                                                                                                                                                    |
| volumeChange12             | The percent volume change in the past 12 hours. Decimal format                                                                                                                                                                     |
| volumeChange24             | The percent volume change in the past 24 hours. Decimal format                                                                                                                                                                     |
| walletAgeAvg               | The average age of the wallets that traded in the last 24h                                                                                                                                                                         |
| walletAgeStd               | The standard deviation of age of the wallets that traded in the last 24h                                                                                                                                                           |

---

# Request Implementation

---

The following user query will dictate the graphQL query to be generated.

## User Query

```py
{user_query}
```

---

# Generate GraphQL query

---

## GraphQL Query Generation Instructions

### Notes

- All numeric values in filters should be passed as strings when they represent amounts (e.g., prices, volumes)
- Timestamps are returned as Unix timestamps (integers)
- Boolean values are used for flags like `isScam` and `isVerified`
- Arrays are used for lists of items like `exchanges` and `tokens`
- The `statsType` can only be "FILTERED" or "UNFILTERED"
- Ranking attributes and directions should be valid enum values as defined in the schema

### Return the GraphQL query in below format

```json
query {
  filterTokens(
    filters: {
      liquidity: { gt: 100000 }
      change24: { gt: 0.25 }
      txnCount24: { gt: 200 }
      network: [1]
    }
    limit: 1
  ) {
    results {
      buyCount1
      high1
      txnCount1
      uniqueTransactions1
      volume1
      liquidity
      marketCap
      priceUSD
      pair {
        token0
        token1
      }
      exchanges {
        name
      }
      token {
        address
        decimals
        name
        networkId
        symbol
      }
    }
  }
}
```

## Generate the GraphQL query
