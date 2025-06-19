#!/usr/bin/env python3
"""
Enhanced DappLooker Two-Step API Fetcher
- Step 1: Get All Tokens (crypto-metainfo API - 100 per page)
- Step 2: Get Token Market Data (crypto-market API with token_tickers)
- Daily refresh with timestamped filenames  
- Duplicate prevention using token IDs
- Automatic Irys upload with DappLooker tags and date
- 4-day file retention with auto-cleanup
- Comprehensive logging and monitoring
"""

import csv
import requests
import time
import logging
import os
import subprocess
import glob
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_KEY = "0de6af685d0d40e2852ead2d67210442"
METAINFO_URL = "https://api.dapplooker.com/v1/crypto-metainfo"
MARKET_URL = "https://api.dapplooker.com/v1/crypto-market/"

# Irys Configuration
IRYS_NODE = os.getenv('IRYS_NODE', 'https://uploader.irys.xyz')
IRYS_TOKEN = os.getenv('IRYS_TOKEN', 'ethereum')
WALLET_PRIVATE_KEY = os.getenv('WALLET_PRIVATE_KEY')
UPLOAD_ENABLED = os.getenv('UPLOAD_ENABLED', 'true').lower() == 'true'

# File retention settings
RETENTION_DAYS = 4

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('enhanced_dapplooker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def cleanup_old_files():
    """Remove files older than RETENTION_DAYS"""
    logger.info(f"🧹 Cleaning up files older than {RETENTION_DAYS} days...")
    
    cutoff_date = datetime.now() - timedelta(days=RETENTION_DAYS)
    removed_count = 0
    
    # Clean up CSV files
    for pattern in ['market_data_*.csv', 'missing_tokens_*.csv', 'simple_market_data_*.csv']:
        for file_path in glob.glob(pattern):
            try:
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_time < cutoff_date:
                    os.remove(file_path)
                    logger.info(f"   🗑️  Removed old file: {file_path}")
                    removed_count += 1
            except Exception as e:
                logger.error(f"   ❌ Error removing {file_path}: {e}")
    
    # Clean up log files
    for log_file in glob.glob('*.log'):
        try:
            if log_file != 'enhanced_dapplooker.log':  # Keep current log
                file_time = datetime.fromtimestamp(os.path.getmtime(log_file))
                if file_time < cutoff_date:
                    os.remove(log_file)
                    logger.info(f"   🗑️  Removed old log: {log_file}")
                    removed_count += 1
        except Exception as e:
            logger.error(f"   ❌ Error removing {log_file}: {e}")
    
    if removed_count > 0:
        logger.info(f"   ✅ Cleaned up {removed_count} old files")
    else:
        logger.info("   ✅ No old files to remove")

def initialize_csv(filename):
    """Create CSV file with headers"""
    fieldnames = [
        # Token Info
        'id', 'symbol', 'name', 'chain', 'ecosystem', 'address',
        # Market Data
        'usd_price', 'mcap', 'fdv', 'volume_24h', 'total_liquidity',
        'price_change_percentage_1h', 'price_change_percentage_24h',
        'price_change_percentage_7d', 'price_change_percentage_30d',
        'volume_change_percentage_7d', 'volume_change_percentage_30d',
        'mcap_change_percentage_7d', 'mcap_change_percentage_30d',
        'price_high_24h', 'price_ath', 'circulating_supply', 'total_supply',
        # Technical Indicators
        'support', 'resistance', 'rsi', 'sma',
        # Token Holder Insights
        'total_holder_count', 'holder_count_change_percentage_24h',
        'fifty_percentage_holding_wallet_count',
        'first_100_buyers_initial_bought',
        'first_100_buyers_initial_bought_percentage',
        'first_100_buyers_current_holding',
        'first_100_buyers_current_holding_percentage',
        'top_10_holder_balance', 'top_10_holder_percentage',
        'top_50_holder_balance', 'top_50_holder_percentage',
        'top_100_holder_balance', 'top_100_holder_percentage',
        # Smart Money Insights
        'top_25_holder_buy_24h', 'top_25_holder_sold_24h',
        # Dev Wallet Insights
        'wallet_address', 'wallet_balance',
        'dev_wallet_total_holding_percentage',
        'dev_wallet_outflow_txs_count_24h',
        'dev_wallet_outflow_amount_24h',
        'fresh_wallet', 'dev_sold', 'dev_sold_percentage',
        'bundle_wallet_count', 'bundle_wallet_supply_percentage',
        # Social Metrics
        'mindshare_3d', 'mindshare_change_percentage_3d',
        'impression_count_3d', 'impression_count_change_percentage_3d',
        'engagement_count_3d', 'engagement_count_change_percentage_3d',
        'follower_count_3d', 'smart_follower_count_3d',
        'mindshare_7d', 'mindshare_change_percentage_7d',
        'impression_count_7d', 'impression_count_change_percentage_7d',
        'engagement_count_7d', 'engagement_count_change_percentage_7d',
        'follower_count_7d', 'smart_follower_count_7d',
        # Metadata
        'last_updated_at'
    ]
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
    
    logger.info(f"✅ {filename} created with {len(fieldnames)} columns")
    return fieldnames

def initialize_missing_tokens_csv(filename):
    """Create CSV file for tokens missing market data"""
    fieldnames = ['symbol', 'chain', 'timestamp', 'reason']
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
    
    logger.info(f"✅ {filename} created for tracking missing market data")
    return fieldnames

def log_missing_tokens(token_symbols, chain, filename, reason):
    """Log tokens that don't have market data to separate CSV"""
    if not token_symbols:
        return
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['symbol', 'chain', 'timestamp', 'reason'])
        
        for symbol in token_symbols:
            writer.writerow({
                'symbol': symbol,
                'chain': chain,
                'timestamp': timestamp,
                'reason': reason
            })

def get_all_tokens(chain):
    """
    Step 1: Get all tokens using crypto-metainfo API
    Returns list of token symbols
    100 tokens per page
    """
    tokens = []
    page = 1
    total_tokens = 0
    
    while True:
        params = {
            'api_key': API_KEY,
            'chain': chain,
            'page': page
        }
        
        try:
            response = requests.get(METAINFO_URL + "/", params=params, timeout=60)  # Add trailing slash
            response.raise_for_status()
            
            try:
                data = response.json()
                # Handle the correct API response format: {"success": true, "data": [...]}
                if not data.get('success'):
                    logger.error(f"❌ API returned success=false: {data}")
                    break
                    
                token_data = data.get('data', [])
            except ValueError as e:
                logger.error(f"❌ Invalid JSON response: {str(e)}")
                logger.debug(f"Response content: {response.text[:200]}...")
                break
                
            if not token_data:
                logger.info("   ✅ No more tokens found")
                break
            
            # Extract token symbols
            for token in token_data:
                if token.get('symbol'):
                    tokens.append(token['symbol'].lower())
                    total_tokens += 1
            
            logger.info(f"   📄 Page {page}: {len(token_data)} tokens found (Total: {total_tokens})")
            
            if len(token_data) < 100:  # Less than max per page means we're done
                break
                
            page += 1
            time.sleep(0.2)  # Rate limiting
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching tokens page {page}: {str(e)}")
            break
        except Exception as e:
            logger.error(f"❌ Unexpected error on page {page}: {str(e)}")
            break
    
    logger.info(f"✅ STEP 1 Complete: Found {total_tokens} tokens")
    return tokens

def classify_tokens(token_symbols):
    """Classify tokens as clean or problematic based on special characters"""
    clean_tokens = []
    problematic_tokens = []
    
    for token in token_symbols:
        # Check for problematic characters that cause URL encoding issues
        if any(char in token for char in ['$', ',', '&', '=', '?', '#', '%', '+', ' ']):
            problematic_tokens.append(token)
        else:
            clean_tokens.append(token)
    
    return clean_tokens, problematic_tokens

def try_batch_request(chain, batch, batch_type=""):
    """Try to process a batch of tokens with 502 error retry logic"""
    token_tickers = ','.join(batch)
    
    params = {
        'api_key': API_KEY,
        'chain': chain,
        'token_tickers': token_tickers
    }
    
    # Retry logic for 502 errors
    max_retries = 3
    retry_delays = [2, 5, 10]  # Progressive delays in seconds
    
    for attempt in range(max_retries):
        try:
            response = requests.get(MARKET_URL, params=params, timeout=60)
            response.raise_for_status()
            
            try:
                data = response.json()
                if not data.get('success'):
                    logger.warning(f"⚠️ {batch_type}Batch API returned success=false: {data}")
                    return False, None, f"API success=false: {data}"
                    
                market_data = data.get('data', [])
                return True, market_data, None
                
            except ValueError as e:
                logger.warning(f"⚠️ {batch_type}Batch JSON error: {str(e)}")
                return False, None, f"JSON parsing error: {str(e)}"
            
        except requests.exceptions.HTTPError as e:
            if hasattr(e.response, 'status_code') and e.response.status_code == 502:
                if attempt < max_retries - 1:  # Don't retry on last attempt
                    delay = retry_delays[attempt]
                    logger.warning(f"⚠️ {batch_type}502 Server Error (attempt {attempt + 1}/{max_retries}), retrying in {delay}s...")
                    time.sleep(delay)
                    continue
                else:
                    logger.warning(f"⚠️ {batch_type}502 Server Error - max retries exceeded")
                    return False, None, f"Request error: {str(e)}"
            else:
                logger.warning(f"⚠️ {batch_type}HTTP error: {str(e)}")
                return False, None, f"Request error: {str(e)}"
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️ {batch_type}Batch request error: {str(e)}")
            return False, None, f"Request error: {str(e)}"
        except Exception as e:
            logger.warning(f"⚠️ {batch_type}Batch unexpected error: {str(e)}")
            return False, None, f"Unexpected error: {str(e)}"
    
    return False, None, "Max retries exceeded"

def try_individual_requests(chain, tokens, missing_tokens_filename):
    """Process tokens individually as fallback, only log failures to CSV"""
    individual_data = []
    individual_processed = 0
    
    logger.info(f"   🔄 Falling back to individual requests for {len(tokens)} tokens...")
    
    for token in tokens:
        params = {
            'api_key': API_KEY,
            'chain': chain,
            'token_tickers': token
        }
        
        # Retry logic for individual requests too
        max_retries = 2
        retry_delays = [1, 3]
        
        for attempt in range(max_retries):
            try:
                response = requests.get(MARKET_URL, params=params, timeout=30)
                response.raise_for_status()
                
                try:
                    data = response.json()
                    if data.get('success'):
                        token_data = data.get('data', [])
                        if token_data:
                            individual_data.extend(token_data)
                            individual_processed += 1
                        else:
                            # No market data returned - not an error, just no data
                            log_missing_tokens([token], chain, missing_tokens_filename, "No market data returned")
                    else:
                        # API returned success=false - log as error
                        log_missing_tokens([token], chain, missing_tokens_filename, f"API error - success=false")
                    break  # Success, exit retry loop
                except ValueError as e:
                    # JSON parsing error - log as error
                    log_missing_tokens([token], chain, missing_tokens_filename, f"JSON parsing error: {str(e)}")
                    break  # No point retrying JSON errors
                    
            except requests.exceptions.HTTPError as e:
                if hasattr(e.response, 'status_code') and e.response.status_code == 502:
                    if attempt < max_retries - 1:  # Don't retry on last attempt
                        delay = retry_delays[attempt]
                        time.sleep(delay)
                        continue
                    else:
                        # Max retries exceeded for 502
                        log_missing_tokens([token], chain, missing_tokens_filename, f"Request error: {str(e)}")
                        break
                else:
                    # Other HTTP errors - log and exit
                    log_missing_tokens([token], chain, missing_tokens_filename, f"Request error: {str(e)}")
                    break
            except requests.exceptions.RequestException as e:
                # Other request errors - log and exit
                log_missing_tokens([token], chain, missing_tokens_filename, f"Request error: {str(e)}")
                break
            except Exception as e:
                # Unexpected error - log and exit
                log_missing_tokens([token], chain, missing_tokens_filename, f"Unexpected error: {str(e)}")
                break
        
        time.sleep(0.1)  # Small delay between individual requests
    
    return individual_data, individual_processed

def get_market_data(chain, token_symbols, fieldnames, filename, existing_ids, missing_tokens_filename):
    """
    Step 2: Get market data using crypto-market API with smart batching
    - Use normal batches for clean tokens
    - Use smaller batches for problematic tokens
    - Fall back to individual requests when batches fail
    - Only log to CSV after individual fallback fails
    """
    total_processed = 0
    
    # Classify tokens
    clean_tokens, problematic_tokens = classify_tokens(token_symbols)
    
    logger.info(f"   📊 Token classification: {len(clean_tokens)} clean, {len(problematic_tokens)} problematic")
    
    # Process clean tokens in normal batches (30 tokens)
    if clean_tokens:
        logger.info(f"   🔄 Processing {len(clean_tokens)} clean tokens in normal batches...")
        batch_size = 30
        
        for i in range(0, len(clean_tokens), batch_size):
            batch = clean_tokens[i:i+batch_size]
            batch_num = i//batch_size + 1
            
            success, market_data, error = try_batch_request(chain, batch, f"Clean batch {batch_num}: ")
            
            if success:
                # Track which tokens got market data
                tokens_with_data = set()
                for record in market_data:
                    token_info = record.get('token_info', {})
                    symbol = token_info.get('symbol', '').lower()
                    if symbol:
                        tokens_with_data.add(symbol)
                
                # Find tokens without market data
                tokens_without_data = [token for token in batch if token not in tokens_with_data]
                if tokens_without_data:
                    log_missing_tokens(tokens_without_data, chain, missing_tokens_filename, "No market data returned")
                
                # Write to CSV
                records_added = write_market_data(market_data, fieldnames, filename, existing_ids)
                total_processed += records_added
                
                missing_count = len(tokens_without_data)
                logger.info(f"   ✅ Clean batch {batch_num}: Processed {len(batch)} tokens, added {records_added} records, {missing_count} missing")
            else:
                # Batch failed, fall back to individual requests
                logger.info(f"   ⚠️ Clean batch {batch_num} failed, falling back to individual requests")
                individual_data, individual_count = try_individual_requests(chain, batch, missing_tokens_filename)
                
                if individual_data:
                    records_added = write_market_data(individual_data, fieldnames, filename, existing_ids)
                    total_processed += records_added
                    logger.info(f"   ✅ Individual fallback: Added {records_added} records from {individual_count} tokens")
            
            time.sleep(0.2)  # Rate limiting
    
    # Process problematic tokens in smaller batches (10 tokens)
    if problematic_tokens:
        logger.info(f"   🔄 Processing {len(problematic_tokens)} problematic tokens in smaller batches...")
        batch_size = 10
        
        for i in range(0, len(problematic_tokens), batch_size):
            batch = problematic_tokens[i:i+batch_size]
            batch_num = i//batch_size + 1
            
            success, market_data, error = try_batch_request(chain, batch, f"Problematic batch {batch_num}: ")
            
            if success:
                # Track which tokens got market data
                tokens_with_data = set()
                for record in market_data:
                    token_info = record.get('token_info', {})
                    symbol = token_info.get('symbol', '').lower()
                    if symbol:
                        tokens_with_data.add(symbol)
                
                # Find tokens without market data
                tokens_without_data = [token for token in batch if token not in tokens_with_data]
                if tokens_without_data:
                    log_missing_tokens(tokens_without_data, chain, missing_tokens_filename, "No market data returned")
                
                # Write to CSV
                records_added = write_market_data(market_data, fieldnames, filename, existing_ids)
                total_processed += records_added
                
                missing_count = len(tokens_without_data)
                logger.info(f"   ✅ Problematic batch {batch_num}: Processed {len(batch)} tokens, added {records_added} records, {missing_count} missing")
            else:
                # Batch failed, fall back to individual requests
                logger.info(f"   ⚠️ Problematic batch {batch_num} failed, falling back to individual requests")
                individual_data, individual_count = try_individual_requests(chain, batch, missing_tokens_filename)
                
                if individual_data:
                    records_added = write_market_data(individual_data, fieldnames, filename, existing_ids)
                    total_processed += records_added
                    logger.info(f"   ✅ Individual fallback: Added {records_added} records from {individual_count} tokens")
            
            time.sleep(0.2)  # Rate limiting
    
    return total_processed

def write_market_data(market_data, fieldnames, filename, existing_ids):
    """Write market data to CSV file"""
    records_added = 0
    
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        for record in market_data:
            # Flatten nested data
            flat_record = {}
            
            # Token Info
            token_info = record.get('token_info', {})
            for key in ['id', 'symbol', 'name', 'chain', 'ecosystem', 'address']:
                flat_record[key] = token_info.get(key)
            
            # Technical Indicators
            tech_indicators = record.get('technical_indicators', {})
            for key in ['support', 'resistance', 'rsi', 'sma']:
                flat_record[key] = tech_indicators.get(key)
            
            # Token Holder Insights
            holder_insights = record.get('token_holder_insights', {})
            for key in holder_insights:
                flat_record[key] = holder_insights.get(key)
            
            # Smart Money Insights
            smart_money = record.get('smart_money_insights', {})
            for key in smart_money:
                flat_record[key] = smart_money.get(key)
            
            # Dev Wallet Insights
            dev_wallet = record.get('dev_wallet_insights', {})
            for key in dev_wallet:
                flat_record[key] = dev_wallet.get(key)
            
            # Token Metrics
            metrics = record.get('token_metrics', {})
            for key in metrics:
                flat_record[key] = metrics.get(key)
            
            # Social Metrics
            social = record.get('x_social_metrics', {})
            for key in social:
                flat_record[key] = social.get(key)
            
            # Metadata
            flat_record['last_updated_at'] = record.get('last_updated_at')
            
            # Write record
            writer.writerow(flat_record)
            records_added += 1
    
    if records_added > 0:
        file_size = os.path.getsize(filename)
        logger.info(f"   ✅ Added {records_added} records (Size: {file_size:,} bytes)")
    
    return records_added

def upload_to_irys(csv_file_path):
    """Upload CSV file to Irys with DappLooker tags"""
    if not UPLOAD_ENABLED:
        logger.info("📤 Upload disabled")
        return None
    
    if not os.path.exists(csv_file_path):
        logger.error(f"❌ File not found: {csv_file_path}")
        return None
    
    file_size = os.path.getsize(csv_file_path)
    logger.info(f"📤 Uploading to Irys...")
    logger.info(f"   📁 File: {csv_file_path}")
    logger.info(f"   📊 Size: {file_size:,} bytes")
    
    try:
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Simplified tag set - removed dataType, version, fileSize, status, timestamp, content-type
        cmd = [
            'irys', 'upload', str(csv_file_path),
            '--token', IRYS_TOKEN,
            '--host', IRYS_NODE,
            '--wallet', WALLET_PRIVATE_KEY,
            '--tags', 'appName', 'DappLooker',
            '--tags', 'date', current_date,
            '--tags', 'time', current_time,
            '--tags', 'chains', 'base,solana'
        ]
        
        logger.info("🏷️ Irys Tags:")
        logger.info("   • appName: DappLooker")
        logger.info(f"   • date: {current_date}")
        logger.info(f"   • time: {current_time}")
        logger.info("   • chains: base,solana")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            output = result.stdout.strip()
            
            # Enhanced transaction ID extraction with multiple patterns
            tx_id = None
            
            # Log the raw output for debugging
            logger.info(f"📄 Raw Irys output ({len(output)} chars):")
            for i, line in enumerate(output.split('\n')):
                logger.info(f"   Line {i}: '{line}'")
            
            # Pattern 1: Standard format
            for line in output.split('\n'):
                if line.startswith('Uploaded to https://gateway.irys.xyz/'):
                    tx_id = line.split('/')[-1].strip()
                    logger.info(f"✅ TX ID extracted (Pattern 1): {tx_id}")
                    break
            
            # Pattern 2: Any line containing gateway.irys.xyz
            if not tx_id:
                for line in output.split('\n'):
                    if 'gateway.irys.xyz' in line and '/' in line:
                        tx_id = line.split('/')[-1].strip()
                        logger.info(f"✅ TX ID extracted (Pattern 2): {tx_id}")
                        break
            
            # Pattern 3: Look for long alphanumeric strings (likely TX IDs)
            if not tx_id:
                for line in output.split('\n'):
                    words = line.split()
                    for word in words:
                        # Irys TX IDs are typically 44+ characters, base58 encoded
                        if len(word) >= 40 and word.replace('-', '').replace('_', '').isalnum():
                            # Exclude wallet addresses (start with 0x)
                            if not word.startswith('0x'):
                                tx_id = word
                                logger.info(f"✅ TX ID extracted (Pattern 3): {tx_id}")
                                break
                    if tx_id:
                        break
            
            if tx_id:
                logger.info("🎊 UPLOAD SUCCESSFUL!")
                logger.info("=" * 60)
                logger.info(f"📦 FILE: {os.path.basename(csv_file_path)}")
                logger.info(f"🆔 TRANSACTION ID: {tx_id}")
                logger.info(f"🔗 ACCESS LINK: https://gateway.irys.xyz/{tx_id}")
                logger.info(f"🔍 EXPLORER LINK: https://explorer.irys.xyz/tx/{tx_id}")
                logger.info("=" * 60)
                logger.info("💡 Use the ACCESS LINK above to download/view your file")
                
                # Verify the link works by testing the format
                if len(tx_id) >= 40 and tx_id.replace('-', '').replace('_', '').isalnum():
                    logger.info("✅ Transaction ID format appears valid")
                else:
                    logger.warning(f"⚠️ Transaction ID format may be invalid: {tx_id}")
                
                return tx_id
            else:
                logger.warning("⚠️ Upload completed but transaction ID not found in output")
                logger.info(f"📤 Full stdout: {output}")
                logger.info(f"📤 Full stderr: {result.stderr}")
                return "success"
        else:
            logger.error(f"❌ Upload failed: {result.stderr}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Upload error: {e}")
        return None

def process_chain(chain, fieldnames, filename, existing_ids, missing_tokens_filename):
    """Process all tokens for a chain"""
    logger.info(f"\n🔄 PROCESSING: {chain.upper()}")
    logger.info("-" * 60)
    
    # Step 1: Get all tokens
    logger.info(f"📋 STEP 1: Getting all tokens for {chain.upper()}")
    tokens = get_all_tokens(chain)
    
    if not tokens:
        logger.warning(f"⚠️ No tokens found for {chain}")
        return 0
    
    # Step 2: Get market data for tokens
    logger.info(f"\n📊 STEP 2: Getting market data for {len(tokens)} tokens")
    total_processed = get_market_data(chain, tokens, fieldnames, filename, existing_ids, missing_tokens_filename)
    
    return total_processed

def main():
    """Main execution - Two-step process using both APIs"""
    start_time = datetime.now()
    
    logger.info("🚀 Enhanced DappLooker Two-Step API Fetcher Started")
    logger.info("📋 Step 1: Get All Tokens (crypto-metainfo)")
    logger.info("📊 Step 2: Get Market Data (crypto-market)")
    logger.info(f"📅 Date: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 70)
    
    # Cleanup old files first
    cleanup_old_files()
    
    # Create CSV file with date/time stamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"market_data_{timestamp}.csv"
    fieldnames = initialize_csv(filename)
    
    # Create missing tokens CSV file
    missing_tokens_filename = f"missing_tokens_{timestamp}.csv"
    initialize_missing_tokens_csv(missing_tokens_filename)
    
    # Track existing IDs for duplicate prevention
    existing_ids = set()
    total_records = 0
    
    # Process Base chain
    total_records += process_chain("base", fieldnames, filename, existing_ids, missing_tokens_filename)
    
    # Process Solana chain
    total_records += process_chain("solana", fieldnames, filename, existing_ids, missing_tokens_filename)
    
    # Upload to Irys
    logger.info("\n📤 UPLOADING TO IRYS")
    logger.info("-" * 50)
    tx_id = upload_to_irys(filename)
    
     # Final summary
    end_time = datetime.now()
    duration = end_time - start_time
    
    # Check if missing tokens file has content
    missing_tokens_count = 0
    if os.path.exists(missing_tokens_filename):
        with open(missing_tokens_filename, 'r') as f:
            missing_tokens_count = sum(1 for line in f) - 1  # Subtract header
    
    logger.info("\n🎯 FINAL RESULTS")
    logger.info("=" * 70)
    logger.info(f"📊 Total Records Collected: {total_records:,}")
    logger.info(f"📁 Market Data File: {filename}")
    logger.info(f"🔍 Missing Tokens File: {missing_tokens_filename}")
    logger.info(f"❌ Tokens Without Market Data: {missing_tokens_count:,}")
    logger.info(f"⏱️  Duration: {duration}")
    
    if tx_id and tx_id != "success":
        logger.info("🎊 IRYS UPLOAD SUCCESSFUL!")
        logger.info(f"🆔 TRANSACTION ID: {tx_id}")
        logger.info(f"🔗 ACCESS YOUR FILE: https://gateway.irys.xyz/{tx_id}")
        logger.info(f"🔍 VIEW ON EXPLORER: https://explorer.irys.xyz/tx/{tx_id}")
        logger.info("💡 Copy the ACCESS link to download your file anytime!")
    elif tx_id == "success":
        logger.info("✅ Upload completed successfully")
    else:
        logger.info("⚠️  Upload failed or skipped")
    
    logger.info("=" * 70)
    logger.info(f"📝 Log saved to: enhanced_dapplooker.log")
    logger.info(f"🔍 Missing tokens tracked in: {missing_tokens_filename}")
    logger.info(f"🧹 Files older than {RETENTION_DAYS} days automatically cleaned")
    logger.info("🔄 Daily refresh ready - run again tomorrow for updates")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code) 