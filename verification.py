# Price Verification Module for Income Investing Analysis
import yfinance as yf
import pandas as pd
import warnings

# Suppress pandas warnings for cleaner output
warnings.filterwarnings('ignore', category=FutureWarning)

def verify_price_with_alternative_source(symbol, target_date):
    """
    Verify price using multiple yfinance methods for cross-validation, with Canadian ETF support
    Returns dict with verification status and average price
    """
    try:
        print(f"    🔍 Trying alternative verification methods...")
        
        # Try different ticker formats for Canadian ETFs
        symbols_to_try = [symbol]
        
        # Add .TO suffix for Toronto Stock Exchange if not already present
        if not symbol.endswith('.TO') and not symbol.endswith('.TSE'):
            symbols_to_try.append(f"{symbol}.TO")
            symbols_to_try.append(f"{symbol}.TSE")
        
        # Try NEO Exchange format for some Canadian ETFs
        if symbol in ['HHIS', 'MSTE']:
            symbols_to_try.append(f"{symbol}.NE")
        
        prices = []
        methods = []
        
        for ticker_format in symbols_to_try:
            print(f"    📊 Trying verification with {ticker_format}...")
            
            # Method 1: Ticker.history with different periods
            try:
                ticker = yf.Ticker(ticker_format)
                hist1 = ticker.history(start=target_date, end=pd.Timestamp(target_date) + pd.Timedelta(days=5), 
                                     auto_adjust=False)
                if not hist1.empty:
                    price1 = float(hist1.iloc[0]['Open'])
                    prices.append(price1)
                    methods.append(f"Method 1 ({ticker_format})")
                    print(f"    ✓ Method 1 ({ticker_format}): ${price1:.2f}")
            except Exception as e:
                print(f"    ❌ Method 1 failed with {ticker_format}: {e}")
            
            # Method 2: yf.download with different date range
            try:
                start_range = pd.Timestamp(target_date) - pd.Timedelta(days=2)
                end_range = pd.Timestamp(target_date) + pd.Timedelta(days=4)
                
                data3 = yf.download(ticker_format, start=start_range.strftime('%Y-%m-%d'), 
                                  end=end_range.strftime('%Y-%m-%d'), auto_adjust=False, progress=False)
                if not data3.empty:
                    # Find the closest date to our target
                    target_ts = pd.Timestamp(target_date)
                    closest_idx = None
                    min_diff = pd.Timedelta.max
                    
                    for idx in data3.index:
                        diff = abs(idx - target_ts)
                        if diff < min_diff:
                            min_diff = diff
                            closest_idx = idx
                    
                    if closest_idx is not None:
                        price3 = float(data3.loc[closest_idx]['Open'])
                        prices.append(price3)
                        methods.append(f"Method 2 ({ticker_format})")
                        print(f"    ✓ Method 2 ({ticker_format}): ${price3:.2f}")
            except Exception as e:
                print(f"    ❌ Method 2 failed with {ticker_format}: {e}")
            
            # If we found data with this ticker format, we can break
            if prices:
                break
        
        # Analyze results
        if len(prices) == 0:
            print(f"    ❌ All methods failed")
            return {'error': 'All verification methods failed', 'verified': False}
        
        if len(prices) == 1:
            print(f"    ⚠️ Only 1 method succeeded: ${prices[0]:.2f}")
            return {
                'average': prices[0],
                'verified': False,
                'methods': methods,
                'prices': prices
            }
        
        # Check if prices agree (within 1% tolerance)
        avg_price = sum(prices) / len(prices)
        max_diff = max(abs(p - avg_price) / avg_price for p in prices)
        
        if max_diff <= 0.01:  # 1% tolerance
            print(f"    ✅ {len(prices)} methods agree: ${avg_price:.2f}")
            return {
                'average': avg_price,
                'verified': True,
                'methods': methods,
                'prices': prices
            }
        else:
            print(f"    ⚠️ Price discrepancy detected (max diff: {max_diff:.1%})")
            print(f"    📊 Prices: {[f'${p:.2f}' for p in prices]}")
            return {
                'average': avg_price,
                'verified': False,
                'methods': methods,
                'prices': prices,
                'discrepancy': max_diff
            }
            
    except Exception as e:
        print(f"    ❌ Verification error: {e}")
        return {'error': str(e), 'verified': False}

def get_verification_status(verification_result):
    """Convert verification result to status string"""
    if verification_result.get('verified'):
        return '✅ VERIFIED'
    elif verification_result.get('average') is not None:
        return '🟡 ALT SOURCE'
    else:
        return '🔴 NO DATA'
