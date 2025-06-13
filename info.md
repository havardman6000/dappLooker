Get All Tokens: https://docs.dapplooker.com/data-apis-for-ai/api-endpoints/get-list-of-all-tokens

Data APIs for AI
API Endpoints
List of All Tokens
Retrieve a list of available Crypto token and their basic metadata. This endpoint is useful for discovering which crypto token are currently active on a specific chain or protocol.

Endpoint
GET https://api.dapplooker.com/v1/crypto-metainfo

💡 Pro Tips 
This endpoint returns a maximum of 100 items per page. Use page query parameter to navigate through results.

You can fetch list of tokens directly by specifying the chain and ecosystem—no need to pass individual token addresses.

To retrieve details for specific token(s), use the token_addresses query parameter.

Query Parameters
Parameter name

Type

Mandatory

Description

api_key

string

Yes

Your unique Loky API key used for authentication

chain

string

Yes

The network chain to query. Supported chains: base, solana

token_addresses

string

No

Comma-separated token contract addresses (upto 30) to fetch info

ecosystem

string

No

Specific ecosystem tokens to query. Supported ecosystem: virtuals

page

integer

No, Default page 1

Page number, 100 items per page.

Sample Request
Copy
# With Pagination Enabled Chain Filter
curl --location 'https://api.dapplooker.com/v1/crypto-metainfo?api_key=<API_KEY>&chain=base&page=1'

# With Pagination Enabled Ecosystem Filter
curl --location 'https://api.dapplooker.com/v1/crypto-metainfo?api_key=<API_KEY>&chain=base&ecosystem=virtuals&page=1'

# With Specific Token Addresses
curl --location 'https://api.dapplooker.com/v1/crypto-metainfo?api_key=<API_KEY>&chain=solana&token_addresses=FVdo7CDJarhYoH6McyTFqx71EtzCPViinvdd1v86Qmy5%2C2w3A2P5juwg234spHKfps7WReWoVmujtErqjaZm9VaiP&page=1'
Sample Response
Copy
[
  {
    "id": "aimonica-brands",
    "symbol": "AIMONICA",
    "name": "Aimonica Brands",
    "address": "FVdo7CDJarhYoH6McyTFqx71EtzCPViinvdd1v86Qmy5",
    "chain": "solana",
    "ecosystem": "solana"
  },
  {
    "id": "aipump",
    "symbol": "AIPUMP",
    "name": "aiPump",
    "address": "2w3A2P5juwg234spHKfps7WReWoVmujtErqjaZm9VaiP",
    "chain": "solana",
    "ecosystem": "solana"
  }
]
Response Fields Explanation
id (string): A unique assigned identifier for the token.

symbol (string): The token's symbol, typically used for trading or display.

name (string): The human-readable name of the token.

address (string): The token's on-chain contract or mint address.

chain (string): The blockchain network where the token is deployed.

ecosystem (string): The broader platform or ecosystem the token belongs to.





- Get Token DeFi Insights: https://docs.dapplooker.com/data-apis-for-ai/api-endpoints/get-crypto-token-market-data


Token Market Data + On-Chain Intelligence + Mindshare
Retrieve detailed information and comprehensive metrics for specified token(s). This endpoint is critical for in-depth analysis, including market data and technical indicators.

Endpoint 
GET https://api.dapplooker.com/v1/crypto-market

💡 Pro Tips 
This endpoint returns a maximum of 30 items per page. Use page query parameter and pagination attributes (being returned in the response) to navigate through results.

You can fetch tokens data directly by specifying the chain and ecosystem—no need to pass individual token addresses, ids or tickers.

To retrieve data for specific token(s), use the token_addresses , token_ids or token_tickers query parameter.

Query Parameters
Parameter name

Type

Mandatory

Description

api_key

string

Yes

Your unique Loky API key used for authentication

chain

string

Yes

The network chain to query. Supported chains: base, solana

token_tickers

string

No

Comma-separated token tickers (upto 30) to fetch info

token_addresses

string

No

Comma-separated token contract addresses (upto 30) to fetch info

token_ids

string

No

Comma-separated token IDs (upto 30) to fetch info

ecosystem

string

No

Specific ecosystem tokens to query. Supported ecosystem: virtuals

page

integer

No, Default page 1

Page number, 30 items per page

Sample Request
Copy
# With Token Tickers
curl --location 'https://api.dapplooker.com/v1/crypto-market?api_key=<API_KEY>&chain=base&token_tickers=AIXBT'

# With Token Addresses
curl --location 'https://api.dapplooker.com/v1/crypto-market?api_key=<API_KEY>&chain=base&token_addresses=0x4F9Fd6Be4a90f2620860d680c0d4d5Fb53d1A825'

# With Token IDs
curl --location 'https://api.dapplooker.com/v1/crypto-market?api_key=<API_KEY>&chain=base&token_ids=aixbt,vaderai-by-virtuals'

# With Pagination Enabled Ecosystem Filter
curl --location 'https://api.dapplooker.com/v1/crypto-market/?api_key=<API_KEY>&chain=base&ecosystem=virtuals&page=1'
Sample Response
Copy
{
  "success": true,
  "data": [
    {
      "id": "aixbt",
      "token_info": {
        "id": "aixbt",
        "symbol": "AIXBT",
        "name": "aixbt by Virtuals",
        "handle": "aixbt_agent",
        "description": "AIXBT is an AI agent and driven crypto market intelligence platform designed to provide token holders with a strategic edge in the rapidly evolving crypto space. Leveraging advanced narrative detection and alpha-focused analysis, AIXBT automates the process of tracking and interpreting market trends, helping users gain actionable insights. This project emphasizes integrating various data sources and platforms for comprehensive analysis and decision-making.",
        "ca": "0x4f9fd6be4a90f2620860d680c0d4d5fb53d1a825",
        "chain": "base",
        "ecosystem": "virtuals"
      },
      "technical_indicators": {
        "support": "0.2103200000",
        "resistance": "0.2459300000",
        "rsi": "40.35",
        "sma": "0.2305506000"
      },
      "token_holder_insights": {
        "total_holder_count": 322354,
        "holder_count_change_percentage_24h": "0.07",
        "fifty_percentage_holding_wallet_count": "18.00",
        "first_100_buyers_initial_bought": "945882.24",
        "first_100_buyers_initial_bought_percentage": "0.09",
        "first_100_buyers_current_holding": "2029647.49",
        "first_100_buyers_current_holding_percentage": "0.20",
        "top_10_holder_balance": "406519449.12",
        "top_10_holder_percentage": "40.65",
        "top_50_holder_balance": "622587344.39",
        "top_50_holder_percentage": "62.26",
        "top_100_holder_balance": "672075585.75",
        "top_100_holder_percentage": "67.21"
      },
      "smart_money_insights": {
        "top_25_holder_buy_24h": "5051812.00",
        "top_25_holder_sold_24h": "5509253.60"
      },
      "dev_wallet_insights": {
        "wallet_address": "0x8dfb37aae4f8fcbd1f90015a9e75b48f50fd9f59",
        "wallet_balance": null,
        "dev_wallet_total_holding_percentage": null,
        "dev_wallet_outflow_txs_count_24h": null,
        "dev_wallet_outflow_amount_24h": null,
        "fresh_wallet": false,
        "dev_sold": false,
        "dev_sold_percentage": "0.00",
        "bundle_wallet_count": 1,
        "bundle_wallet_supply_percentage": null
      },
      "token_metrics": {
        "usd_price": "0.2168",
        "mcap": "202601848.00",
        "fdv": "216746287.00",
        "volume_24h": "92977418.00",
        "total_liquidity": "3146010.00",
        "price_change_percentage_1h": "-1.56",
        "price_change_percentage_24h": "-7.91",
        "price_change_percentage_7d": "3.52",
        "price_change_percentage_30d": "36.41",
        "volume_change_percentage_7d": "-13.40",
        "volume_change_percentage_30d": "13.70",
        "mcap_change_percentage_7d": "16.00",
        "mcap_change_percentage_30d": "51.50",
        "price_high_24h": "0.2354",
        "price_ath": "0.9426",
        "circulating_supply": "934741953.00",
        "total_supply": "1000000000.00"
      },
      "x_social_metrics": {
        "mindshare_3d": 3.89078276679337,
        "mindshare_change_percentage_3d": -8.96,
        "impression_count_3d": 1993494,
        "impression_count_change_percentage_3d": -1.31,
        "engagement_count_3d": 32860,
        "engagement_count_change_percentage_3d": 0.59,
        "follower_count_3d": 458966,
        "smart_follower_count_3d": 7363,
        "mindshare_7d": 4.14033463609196,
        "mindshare_change_percentage_7d": -0.02,
        "impression_count_7d": 4740567,
        "impression_count_change_percentage_7d": 2.09,
        "engagement_count_7d": 78922,
        "engagement_count_change_percentage_7d": -3.13,
        "follower_count_7d": 458966,
        "smart_follower_count_7d": 7343
      },
      "last_updated_at": "2025-05-30T06:18:49.679Z"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pageSize": 30,
      "pageCount": 1,
      "total": 1
    }
  }
}
Response Fields Explanation
Token Info:
id (string): Unique identifier for the token.

symbol (string): Token name.

ecosystem (string): Ecosystem of the token.

image (string): URL of the token’s image.

description (string): Description of the token.

ca (string): Contract address of the token.

Token Holder Insights:
total_holder_count (integer): Total number of token holders.

holder_count_change_percentage_24h (decimal): Change in the number of holders over the last 24 hours (percentage).

fifty_percentage_holding_wallet_count (integer): Number of wallets holding 50% of the total supply.

first_100_buyers_initial_bought (decimal): Total amount initially purchased by the first 100 buyers.

first_100_buyers_initial_bought_percentage (decimal): Percentage of total supply initially bought by the first 100 buyers.

first_100_buyers_current_holding (decimal): Current total holdings of the first 100 buyers.

first_100_buyers_current_holding_percentage (decimal): Current percentage of total supply held by the first 100 buyers.

top_10_holder_balance (decimal): Combined token balance of the top 10 holders.

top_10_holder_percentage (decimal): Percentage of total token supply held by the top 10 holders.

top_50_holder_balance (decimal): Combined token balance of the top 50 holders.

top_50_holder_percentage (decimal): Percentage of total token supply held by the top 50 holders.

top_100_holder_balance (decimal): Combined token balance of the top 100 holders.

top_100_holder_percentage (decimal): Percentage of total token supply held by the top 100 holders.

Technical Indicators:
support (decimal): Support price level.

resistance (decimal): Resistance price level.

rsi (decimal): Relative Strength Index (RSI) of the token.

sma (decimal): Simple Moving Average (SMA) of the token.

Token Metrics:
usd_price (decimal): Current price of the token in USD.

mcap (decimal): Market capitalization of the token.

fully_diluted_valuation (decimal): Fully diluted valuation of the token.

volume_24h (decimal): Trading volume of the token in the last 24 hours.

price_change_percentage_1h (decimal): Price change in the last 1 hour (percentage).

price_change_percentage_24h (decimal): Price change in the last 24 hours (percentage).

price_change_percentage_7d (decimal): Price change in the last 7 days (percentage).

price_change_percentage_30d (decimal): Price change in the last 30 days (percentage).

volume_change_percentage_7d (decimal): 7-day trading volume change (percentage).

volume_change_percentage_30d (decimal): 30-day trading volume change (percentage).

mcap_change_percentage_7d (decimal): 7-day market capitalization change (percentage).

mcap_change_percentage_30d (decimal): 30-day market capitalization change (percentage).

price_high_24h (decimal): Highest price of the token in the last 24 hours.

price_ath (decimal): All-time high price of the token.

circulating_supply (decimal): Number of tokens currently in circulation.

total_supply (decimal): Total supply of the token.

X Social Metrics:
mindshare_3d (decimal): Token's share of attention in social discussions in the past 3 days.

mindshare_change_percentage_3d (decimal): Percent change of mindshare value in the past 3 days.

impression_count_3d (integer): Number of times the token content is viewed in the past 3 days.

impression_count_change_percentage_3d (decimal): Percent change of impression count value in the past 3 days.

engagement_count_3d (integer): Interactions like likes, shares, and comments in the past 3 days.

engagement_count_change_percentage_3d (decimal): Percent change of engagement count value in the past 3 days.

follower_count_3d (integer): Total followers tracking the token in the past 3 days.

smart_follower_count_3d (integer): Followers with high influence or expertise in the past 3 days.

mindshare_7d (decimal): Token's share of attention in social discussions in the past 7 days.

mindshare_change_percentage_7d (decimal): Percent change of mindshare value in the past 7 days.

impression_count_7d (integer): Number of times the token content is viewed in the past 7 days.

impression_count_change_percentage_7d (decimal): Percent change of impression count value in the past 7 days.

engagement_count_7d (integer): Interactions like likes, shares, and comments in the past 7 days.

engagement_count_change_percentage_7d (decimal): Percent change of engagement count value in the past 7 days.

follower_count_7d (integer): Total followers tracking the token in the past 7 days.

smart_follower_count_7d (integer): Followers with high influence or expertise in the past 7 days.

Last Update Datetime:
last_updated_at (DateTime): ISO timestamp of last data update.

Pagination Attributes:
page (integer): The current given page number, also being returned in the response.

pageSize (integer): The number of max items can be included per page.

pageCount (integer): The total number of pages available.

total (integer): The total number of items available across all pages.