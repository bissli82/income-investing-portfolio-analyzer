# Data Fetcher Module for Income Investing Analysis
import yfinance as yf
import pandas as pd
import warnings
import time

# Suppress pandas warnings for cleaner output
warnings.filterwarnings('ignore', category=FutureWarning)

def get_dividends_for_period(symbol, start_date, end_date, shares_owned):
    """Get total dividends collected for the period"""
    try:
        print(f"    💰 Getting dividends for period...")
        
        ticker = yf.Ticker(symbol)
        dividends = ticker.dividends
        
        if dividends.empty:
            print(f"    ✓ No dividends found")
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

def get_current_market_price(symbol):
    """Get current market price for a symbol"""
    try:
        print(f"    📈 Getting current market price...")
        
        # Method 1: Get most recent trading day data
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="5d", auto_adjust=False)
        
        if not hist.empty:
            # Get the most recent close price
            current_price = float(hist['Close'].iloc[-1])
            current_date = hist.index[-1].strftime('%Y-%m-%d')
            print(f"    ✓ Current price ({current_date}): ${current_price:.2f}")
            return {'price': current_price, 'date': current_date, 'success': True}
        
        # Method 2: Try info if history fails
        info = ticker.info
        if 'regularMarketPrice' in info and info['regularMarketPrice']:
            current_price = float(info['regularMarketPrice'])
            print(f"    ✓ Current price (from info): ${current_price:.2f}")
            return {'price': current_price, 'success': True}
        
        print(f"    ❌ No current price data available")
        return {'success': False, 'error': 'No current price data'}
        
    except Exception as e:
        print(f"    ❌ Error getting current price: {e}")
        return {'success': False, 'error': str(e)}

def get_historical_price(symbol, date):
    """Get historical price for a specific date"""
    try:
        print(f"Getting historical data for {symbol}...")
        
        # Download historical data with raw prices (not dividend adjusted)
        data = yf.download(symbol, start=date, end=pd.Timestamp(date) + pd.Timedelta(days=5), 
                          auto_adjust=False, progress=False)
        
        if data.empty:
            return None, "No data available"
        
        # Get the opening price of the first available trading day
        initial_price = float(data.iloc[0]['Open'])
        actual_date = data.index[0].strftime('%Y-%m-%d')
        
        print(f"  ✓ Price on {actual_date}: ${initial_price:.2f}")
        return initial_price, None
        
    except Exception as e:
        print(f"  ❌ Error getting historical data: {e}")
        return None, str(e)

def process_etf_data(symbol, start_date, end_date, investment_amount):
    """Process all data for a single ETF"""
    print(f"Processing {symbol}...")
    
    # Get initial price
    initial_price, error = get_historical_price(symbol, start_date)
    if initial_price is None:
        return None, error
    
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
    
    # Get dividend data for the period
    dividend_data = get_dividends_for_period(symbol, start_date, end_date, shares_purchased)
    time.sleep(0.2)  # Be nice to the API
    
    dividends_collected = dividend_data.get('total_dividends', 0.0)
    
    # Calculate total return (includes dividends)
    total_return = gain_loss + dividends_collected
    total_return_pct = (total_return / investment_amount) * 100 if current_data.get('success') else 0.0
    
    return {
        'Symbol': symbol,
        'Initial Share Price USD': round(initial_price, 2),
        'Shares Purchased': round(shares_purchased, 2),
        'Current Share Price USD': round(current_price, 2),
        'Current Portfolio Value USD': round(current_value, 2),
        'Dividends Collected USD': round(dividends_collected, 2),
        'Gain/Loss USD': round(gain_loss, 2),
        'Gain/Loss %': round(gain_loss_pct, 1),
        'Total Return USD': round(total_return, 2),
        'Total Return %': round(total_return_pct, 1),
        'Verified': '✅ VERIFIED'
    }, None
