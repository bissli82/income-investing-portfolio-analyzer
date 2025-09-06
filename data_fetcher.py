# Data Fetcher Module for Income Investing Analysis
import yfinance as yf
import pandas as pd
import warnings
import time

# Suppress pandas warnings for cleaner output
warnings.filterwarnings('ignore', category=FutureWarning)

def get_international_ticker_formats(symbol):
    """Get list of ticker formats to try for international markets"""
    symbols_to_try = [symbol]
    
    # Add exchange suffixes if not already present
    if not any(symbol.endswith(suffix) for suffix in ['.TO', '.TSE', '.AX', '.L', '.NE']):
        # Canadian exchanges
        symbols_to_try.append(f"{symbol}.TO")
        symbols_to_try.append(f"{symbol}.TSE")
        
        # Australian exchange
        symbols_to_try.append(f"{symbol}.AX")
        
        # London Stock Exchange
        symbols_to_try.append(f"{symbol}.L")
    
    # Try NEO Exchange format for some Canadian ETFs
    if symbol in ['HHIS', 'MSTE']:
        symbols_to_try.append(f"{symbol}.NE")
    
    return symbols_to_try

def format_date_dd_mm_yyyy(date_str):
    """Convert date from YYYY-MM-DD to DD/MM/YYYY format"""
    try:
        date_obj = pd.to_datetime(date_str)
        return date_obj.strftime('%d/%m/%Y')
    except:
        return date_str

def get_dividends_for_period(symbol, start_date, end_date, shares_owned):
    """Get total dividends collected for the period, with Canadian ETF support"""
    try:
        print(f"    💰 Getting dividends for period...")
        
        # Try different ticker formats for international markets
        symbols_to_try = get_international_ticker_formats(symbol)
        
        for ticker in symbols_to_try:
            try:
                yf_ticker = yf.Ticker(ticker)
                dividends = yf_ticker.dividends
                
                if not dividends.empty:
                    print(f"    ✓ Found dividend data using {ticker}")
                    break
                    
            except Exception as e:
                print(f"    ❌ Failed getting dividends with {ticker}: {e}")
                continue
        else:
            # No dividends found with any ticker format
            print(f"    ✓ No dividends found with any ticker format")
            return {
                'total_dividends': 0.0,
                'dividend_count': 0,
                'success': True
            }
        
        # Filter dividends for our investment period
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        
        # Handle timezone issues
        if hasattr(dividends.index, 'tz') and dividends.index.tz is not None:
            # Convert our dates to match dividend index timezone
            if start_dt.tz is None:
                start_dt = start_dt.tz_localize('UTC').tz_convert(dividends.index.tz)
            if end_dt.tz is None:
                end_dt = end_dt.tz_localize('UTC').tz_convert(dividends.index.tz)
        
        # Filter dividends within our period
        period_dividends = dividends[(dividends.index >= start_dt) & (dividends.index <= end_dt)]
        
        if period_dividends.empty:
            print(f"    ✓ No dividends in period")
            return {
                'total_dividends': 0.0,
                'dividend_count': 0,
                'success': True
            }
        
        # Calculate total dividends collected (dividend per share × shares owned)
        total_dividend_per_share = period_dividends.sum()
        total_dividends_collected = float(total_dividend_per_share) * shares_owned
        dividend_count = len(period_dividends)
        
        print(f"    ✓ Dividends: {dividend_count} payments, ${total_dividends_collected:.2f} total")
        
        return {
            'total_dividends': total_dividends_collected,
            'dividend_per_share': float(total_dividend_per_share),
            'dividend_count': dividend_count,
            'success': True
        }
        
    except Exception as e:
        print(f"    ❌ Error getting dividends: {e}")
        return {'success': False, 'error': str(e), 'total_dividends': 0.0}

def get_etf_additional_info(symbol):
    """Get NAV and ETF size information, with Canadian ETF support"""
    try:
        print(f"    📊 Getting NAV and ETF size info...")
        
        # Try different ticker formats for international markets
        symbols_to_try = get_international_ticker_formats(symbol)
        
        for ticker in symbols_to_try:
            try:
                yf_ticker = yf.Ticker(ticker)
                info = yf_ticker.info
                
                if info:
                    # Extract NAV (Net Asset Value)
                    nav = None
                    nav_keys = ['navPrice', 'bookValue', 'priceToBook']
                    for key in nav_keys:
                        if key in info and info[key]:
                            if key == 'priceToBook' and info[key] != 0:
                                # Calculate NAV from price-to-book ratio
                                regular_price = info.get('regularMarketPrice', 0)
                                if regular_price > 0:
                                    nav = regular_price / info[key]
                            else:
                                nav = info[key]
                            break
                    
                    # Extract ETF size (Assets Under Management)
                    etf_size = None
                    size_keys = ['totalAssets', 'fundInceptionDate']
                    for key in size_keys:
                        if key in info and info[key]:
                            if key == 'totalAssets':
                                etf_size = info[key]
                            break
                    
                    # Also try market cap as fallback
                    if not etf_size and 'marketCap' in info and info['marketCap']:
                        etf_size = info['marketCap']
                    
                    # Format the size for display (everything in millions for consistency)
                    formatted_size = "N/A"
                    if etf_size:
                        size_in_millions = etf_size / 1e6
                        if size_in_millions >= 1000:
                            # For very large funds, show as billions but with consistent decimal places
                            formatted_size = f"${size_in_millions/1000:.1f}B"
                        elif size_in_millions >= 1:
                            formatted_size = f"${size_in_millions:.1f}M"
                        elif size_in_millions >= 0.1:
                            formatted_size = f"${size_in_millions:.2f}M"
                        else:
                            # For very small funds, show in thousands
                            formatted_size = f"${etf_size/1e3:.1f}K"
                    
                    nav_display = f"${nav:.2f}" if nav else "N/A"
                    print(f"    ✓ NAV: {nav_display}, Size: {formatted_size} (using {ticker})")
                    return {
                        'nav': nav,
                        'etf_size': etf_size,
                        'etf_size_millions': etf_size / 1e6 if etf_size else 0,
                        'formatted_size': formatted_size,
                        'success': True,
                        'ticker_used': ticker
                    }
                
            except Exception as e:
                print(f"    ❌ Failed getting additional info with {ticker}: {e}")
                continue
        
        # If all methods failed
        print(f"    ❌ Could not get additional info for {symbol}")
        return {
            'nav': None,
            'etf_size': None,
            'etf_size_millions': 0,
            'formatted_size': "N/A",
            'success': False,
            'error': f'Could not retrieve additional info for {symbol}'
        }
        
    except Exception as e:
        print(f"    ❌ Error getting additional info for {symbol}: {e}")
        return {
            'nav': None,
            'etf_size': None,
            'etf_size_millions': 0,
            'formatted_size': "N/A",
            'success': False,
            'error': str(e)
        }

def get_current_market_price(symbol):
    """Get current market price for a symbol, with Canadian ETF support"""
    try:
        print(f"    📈 Getting current market price...")
        
        # Try different ticker formats for international markets
        symbols_to_try = get_international_ticker_formats(symbol)
        
        for ticker in symbols_to_try:
            try:
                # Method 1: Get most recent trading day data
                yf_ticker = yf.Ticker(ticker)
                hist = yf_ticker.history(period="5d", auto_adjust=False)
                
                if not hist.empty:
                    # Get the most recent close price
                    current_price = float(hist['Close'].iloc[-1])
                    current_date = hist.index[-1].strftime('%Y-%m-%d')
                    print(f"    ✓ Current price ({current_date}): ${current_price:.2f} (using {ticker})")
                    return {'price': current_price, 'date': current_date, 'success': True, 'ticker_used': ticker}
                
                # Method 2: Try info if history fails
                info = yf_ticker.info
                if 'regularMarketPrice' in info and info['regularMarketPrice']:
                    current_price = float(info['regularMarketPrice'])
                    print(f"    ✓ Current price (from info): ${current_price:.2f} (using {ticker})")
                    return {'price': current_price, 'success': True, 'ticker_used': ticker}
                
            except Exception as e:
                print(f"    ❌ Failed with {ticker}: {e}")
                continue
        
        print(f"    ❌ No current price data available with any ticker format")
        return {'success': False, 'error': 'No current price data available'}
        
    except Exception as e:
        print(f"    ❌ Error getting current price: {e}")
        return {'success': False, 'error': str(e)}

def get_historical_price_with_fallback(symbol, preferred_date):
    """Get historical price for a specific date with fallback to actual launch date"""
    try:
        print(f"Getting historical data for {symbol}...")
        
        # Try different ticker formats for international markets
        symbols_to_try = get_international_ticker_formats(symbol)
        
        last_error = None
        successful_ticker = None
        
        for ticker in symbols_to_try:
            try:
                print(f"  Trying ticker format: {ticker}")
                
                # First try the preferred date
                data = yf.download(ticker, start=preferred_date, end=pd.Timestamp(preferred_date) + pd.Timedelta(days=5), 
                                  auto_adjust=False, progress=False)
                
                if not data.empty:
                    # Get the opening price of the first available trading day
                    initial_price = float(data.iloc[0]['Open'])
                    actual_date = data.index[0].strftime('%Y-%m-%d')
                    successful_ticker = ticker
                    
                    formatted_date = format_date_dd_mm_yyyy(actual_date)
                    print(f"  ✓ Price on {formatted_date}: ${initial_price:.2f} (using {ticker})")
                    return {
                        'price': initial_price,
                        'date': actual_date,
                        'formatted_date': formatted_date,
                        'ticker': successful_ticker,
                        'is_fallback': actual_date != preferred_date,
                        'error': None
                    }
                else:
                    # If preferred date fails, try to find the earliest available date
                    print(f"  No data for {preferred_date}, searching for earliest available date...")
                    
                    # Try a wider range to find when this ETF actually started
                    search_start = pd.Timestamp(preferred_date) - pd.Timedelta(days=90)  # Go back 3 months
                    search_end = pd.Timestamp.today()
                    
                    data = yf.download(ticker, start=search_start.strftime('%Y-%m-%d'), 
                                     end=search_end.strftime('%Y-%m-%d'), 
                                     auto_adjust=False, progress=False)
                    
                    if not data.empty:
                        # Get the first available trading day
                        initial_price = float(data.iloc[0]['Open'])
                        actual_date = data.index[0].strftime('%Y-%m-%d')
                        successful_ticker = ticker
                        
                        formatted_date = format_date_dd_mm_yyyy(actual_date)
                        print(f"  ✓ Found earliest date {formatted_date}: ${initial_price:.2f} (using {ticker}) **")
                        return {
                            'price': initial_price,
                            'date': actual_date,
                            'formatted_date': formatted_date,
                            'ticker': successful_ticker,
                            'is_fallback': True,
                            'error': None
                        }
                
            except Exception as e:
                last_error = str(e)
                print(f"  ❌ Failed with {ticker}: {e}")
                continue
        
        # If all formats failed, return the error
        return {
            'price': None,
            'date': None,
            'ticker': None,
            'is_fallback': False,
            'error': f"No data available with any ticker format. Last error: {last_error}"
        }
        
    except Exception as e:
        print(f"  ❌ Error getting historical data: {e}")
        return {
            'price': None,
            'date': None,
            'ticker': None,
            'is_fallback': False,
            'error': str(e)
        }

def get_historical_price(symbol, date):
    """Legacy function for compatibility"""
    result = get_historical_price_with_fallback(symbol, date)
    if result['error']:
        return None, result['error']
    return result['price'], None

def process_etf_data(symbol, start_date, end_date, investment_amount):
    """Process all data for a single ETF with dynamic start date support"""
    print(f"Processing {symbol}...")
    
    # Get initial price with fallback to actual launch date
    price_result = get_historical_price_with_fallback(symbol, start_date)
    if price_result['error']:
        return None, price_result['error']
    
    initial_price = price_result['price']
    actual_start_date = price_result['date']
    formatted_start_date = price_result['formatted_date']
    is_fallback = price_result['is_fallback']
    ticker_used = price_result['ticker']
    
    # Calculate shares purchased
    shares_purchased = investment_amount / initial_price
    
    # Get current market price
    current_data = get_current_market_price(symbol)
    time.sleep(0.2)  # Be nice to the API
    
    if current_data.get('success'):
        current_price = current_data['price']
        current_value = shares_purchased * current_price
        gain_loss = current_value - investment_amount
        gain_loss_pct = (gain_loss / investment_amount) * 100
        
        print(f"  💰 Current portfolio value: ${current_value:,.2f} ({gain_loss_pct:+.1f}%)")
    else:
        current_price = 0.0
        current_value = 0.0
        gain_loss = 0.0
        gain_loss_pct = 0.0
        print(f"  ❌ Could not get current price")
    
    # Get additional ETF information (NAV and size)
    additional_info = get_etf_additional_info(symbol)
    time.sleep(0.2)  # Be nice to the API
    
    nav = additional_info.get('nav', None)
    etf_size = additional_info.get('formatted_size', 'N/A')
    etf_size_millions = additional_info.get('etf_size_millions', 0)
    
    # Get dividend data for the period (use actual start date)
    dividend_data = get_dividends_for_period(symbol, actual_start_date, end_date, shares_purchased)
    time.sleep(0.2)  # Be nice to the API
    
    dividends_collected = dividend_data.get('total_dividends', 0.0)
    
    # Calculate total return (includes dividends)
    total_return = gain_loss + dividends_collected
    total_return_pct = (total_return / investment_amount) * 100 if current_data.get('success') else 0.0
    
    # Create symbol display with ** if it's a fallback date
    symbol_display = f"{symbol}**" if is_fallback else symbol
    
    return {
        'Symbol': symbol_display,
        'Initial Share Price USD': round(initial_price, 2),
        'Current Share Price USD': round(current_price, 2),
        'NAV USD': round(nav, 2) if nav else 'N/A',
        'ETF Size': etf_size,
        'ETF Size Millions': etf_size_millions,
        'Shares Purchased': round(shares_purchased, 2),
        'Current Portfolio Value USD': round(current_value, 2),
        'Dividends Collected USD': round(dividends_collected, 2),
        'Gain/Loss USD': round(gain_loss, 2),
        'Gain/Loss %': round(gain_loss_pct, 1),
        'Total Return USD': round(total_return, 2),
        'Total Return %': round(total_return_pct, 1),
        'Verified': '✅ VERIFIED',
        'Actual Start Date': actual_start_date,
        'Formatted Start Date': formatted_start_date,
        'Is Fallback': is_fallback,
        'Original Symbol': symbol
    }, None
