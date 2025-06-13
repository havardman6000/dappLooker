# Enhanced DappLooker Data Fetcher

🚀 **Complete cryptocurrency market data collection from DappLooker APIs with Irys integration**

## ✨ Key Features

### 📊 **Complete Data Collection**
- **Base Chain**: All ecosystems (virtuals, defi, meme, gaming, ai, etc.)
- **Solana Chain**: Complete ecosystem coverage
- **Specific Addresses**: Sample token addresses for targeted data

### 🕒 **Daily Refresh System**
- **Timestamped Filenames**: `market_data_YYYYMMDD_HHMMSS.csv`
- **Duplicate Prevention**: Token ID-based deduplication
- **Incremental Updates**: Skip existing records for faster refreshes

### 🧹 **Automatic File Management**
- **4-Day Retention**: Automatically removes files older than 4 days
- **Smart Cleanup**: Removes old CSV and log files
- **File Size Monitoring**: Real-time size tracking

### 📤 **Enhanced Irys Integration**
- **Rich Metadata Tags**: appName, date, time, dataType, chains
- **Automatic Upload**: Seamless integration with Irys network
- **Transaction Tracking**: Full upload verification and logging

### 📝 **Comprehensive Monitoring**
- **Real-Time Progress**: Live updates during data collection
- **Detailed Logging**: Complete operation history
- **Error Handling**: Robust error recovery and reporting

## 🚀 Quick Start

### 1. **Environment Setup**
```bash
# Copy and configure environment variables
cp env_template.txt .env
# Edit .env with your wallet private key
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Run Data Collection**
```bash
python3 enhanced_dapplooker.py
```

## 📁 **File Structure**

```
market_data_YYYYMMDD_HHMMSS.csv  # Timestamped data files
enhanced_dapplooker.log          # Comprehensive logs
enhanced_dapplooker.py           # Main script
requirements.txt                 # Python dependencies
.env                            # Environment configuration
```

## 🔧 **Configuration**

### API Configuration
- **API Key**: `e3541b9c746540028b6be3fd4cd3a3b5` (built-in)
- **Endpoints**: DappLooker crypto-market API
- **Rate Limiting**: Built-in delays for API protection

### Irys Configuration
```bash
IRYS_NODE=https://uploader.irys.xyz
IRYS_TOKEN=ethereum
WALLET_PRIVATE_KEY=your_private_key_here
UPLOAD_ENABLED=true
```

## 📊 **Data Columns**

The CSV includes 27 comprehensive columns:
- **Identity**: id, last_updated_at
- **Token Info**: symbol, name, chain, contract_address, description, ecosystem
- **Market Metrics**: price, market_cap, volume, price_changes (1h, 24h, 7d, 30d)
- **Liquidity**: total_liquidity, circulating_supply, total_supply
- **Technical**: RSI, SMA, support, resistance levels
- **Social**: follower_count, engagement, impressions

## 🔄 **Daily Usage**

### Automated Daily Refresh
```bash
# Run daily for fresh data
python3 enhanced_dapplooker.py

# Data automatically:
# ✅ Deduplicates against existing records
# ✅ Creates timestamped files
# ✅ Uploads to Irys with metadata
# ✅ Cleans up old files (4+ days)
```

### Manual Token Queries
The script automatically fetches:
1. **Base Virtuals Ecosystem** (priority)
2. **Base All Ecosystems** (defi, meme, gaming, ai, etc.)
3. **Sample Addresses** (specific tokens)
4. **Solana All Ecosystems** (complete coverage)

## 📈 **Performance**

- **Real-Time CSV Updates**: Data written immediately per page
- **Duplicate Detection**: Prevents redundant data collection
- **Progress Monitoring**: Live file size and record counts
- **Error Recovery**: Robust handling of API timeouts/errors

## 🔗 **Irys Integration**

### Upload Metadata
```json
{
  "appName": "DappLooker",
  "date": "2025-06-13",
  "time": "12:58:15",
  "dataType": "crypto-market",
  "chains": "base,solana"
}
```

### Access Your Data
- **Gateway**: `https://gateway.irys.xyz/{transaction_id}`
- **Explorer**: `https://explorer.irys.xyz/tx/{transaction_id}`

## 📝 **Logging**

### Log Levels
- **INFO**: Progress updates, file operations, upload status
- **ERROR**: API failures, file errors, upload issues

### Log Rotation
- Automatic cleanup of old log files
- Current log: `enhanced_dapplooker.log`

## 🛠 **Troubleshooting**

### Common Issues
1. **API Rate Limits**: Built-in delays handle this automatically
2. **File Permissions**: Ensure write access to directory
3. **Irys Upload**: Check wallet private key in .env
4. **Network Issues**: Script retries failed requests

### Error Recovery
- Failed API calls are logged and skipped
- Partial data is always preserved
- Script continues on non-critical errors

## 📊 **Expected Output**

```
🚀 Enhanced DappLooker API Fetcher Started
📅 Date: 2025-06-13 00:58:15
======================================================================
🧹 Cleaning up files older than 4 days...
   ✅ No old files to remove
📋 Creating market_data_20250613_005815.csv...
✅ market_data_20250613_005815.csv created with 27 columns
📊 Found 0 existing records in market_data_20250613_005815.csv

🔄 BASE CHAIN - COMPLETE DATA COLLECTION
--------------------------------------------------
🌍 Fetching BASE virtuals ecosystem data...
   → Page 1...
   ✅ Added 30 records, skipped 0 duplicates (Size: 24,943 bytes)
   📄 Page 1: 30 fetched, 30 new, 0 duplicates
   ...

======================================================================
🎉 DATA COLLECTION COMPLETE
⏱️  Duration: 0:01:32.456789
📊 Total new records: 8195
📁 File: market_data_20250613_005815.csv
💾 File size: 1,149,410 bytes (1.10 MB)
🕒 Timestamp: 20250613_005815

📤 UPLOADING TO IRYS
--------------------------------------------------
🎊 UPLOAD SUCCESSFUL!
   🆔 Transaction ID: abc123...
   🔗 Gateway: https://gateway.irys.xyz/abc123...
   🔍 Explorer: https://explorer.irys.xyz/tx/abc123...
✅ COMPLETE SUCCESS!
🔄 Daily refresh ready - run again tomorrow for updates
```

## 🎯 **Perfect for**
- Daily cryptocurrency market analysis
- DeFi research and monitoring
- Token ecosystem tracking
- Automated data pipelines
- Blockchain analytics projects 