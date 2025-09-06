# Income Investing Analysis - Main Script
import pandas as pd
import warnings
import time
from datetime import datetime

# Import our custom modules
from symbols import INCOME_ETFS, INVESTMENT_PER_ETF, START_DATE
from data_fetcher import process_etf_data
from verification import verify_price_with_alternative_source, get_verification_status
from html_generator import create_html_report, save_html_report

# Suppress pandas warnings for cleaner output
warnings.filterwarnings('ignore', category=FutureWarning)

def main():
    """Run the complete income investing portfolio analysis"""
    print("="*60)
    print("INCOME INVESTING - INITIAL PURCHASE ANALYSIS")
    print("="*60)
    print(f"Reference Date: {START_DATE} (Raw Market Prices - Not Dividend Adjusted)")
    print(f"Investment Amount: ${INVESTMENT_PER_ETF:,} per ETF")
    print("="*60)
    
    # Initialize data structures
results = []
    verification_results = []
    end_date = pd.Timestamp.today().strftime("%Y-%m-%d")
    
    # Process each ETF
    for etf in INCOME_ETFS:
        try:
            # Try to get data using the simplified data fetcher
            etf_data, error = process_etf_data(etf, START_DATE, end_date, INVESTMENT_PER_ETF)
            
            if etf_data is not None:
                # Data retrieved successfully
                results.append(etf_data)
                verification_results.append({
                    'symbol': etf,
                    'main_price': etf_data['Initial Share Price USD'],
                    'verification': {'verified': True}
                })
            else:
                # Primary method failed, try verification method as backup
                print(f"  ❌ No data from primary source, trying alternative...")
                verification = verify_price_with_alternative_source(etf, START_DATE)
                time.sleep(0.2)
                
                if verification.get('average') is not None:
                    # Alternative source provided data
                    initial_price = verification['average']
                    shares_purchased = INVESTMENT_PER_ETF / initial_price
                    
                    status = get_verification_status(verification)
                    
                    results.append({
                        'Symbol': etf,
                        'Initial Share Price USD': round(initial_price, 2),
                        'Shares Purchased': round(shares_purchased, 2),
                        'Current Share Price USD': 0.00,
                        'Current Portfolio Value USD': 0.00,
                        'Dividends Collected USD': 0.00,
                        'Gain/Loss USD': 0.00,
                        'Gain/Loss %': 0.0,
                        'Total Return USD': 0.00,
                        'Total Return %': 0.0,
                        'Verified': status
                    })
                    
                    verification_results.append({
                        'symbol': etf,
                        'main_price': initial_price,
                        'verification': verification
                    })
                    
                    print(f"  {status}: ${initial_price:.2f}")
                else:
                    # Complete failure - mark in red
                    results.append({
                        'Symbol': etf,
                        'Initial Share Price USD': 0.00,
                        'Shares Purchased': 0.00,
                        'Current Share Price USD': 0.00,
                        'Current Portfolio Value USD': 0.00,
                        'Dividends Collected USD': 0.00,
                        'Gain/Loss USD': 0.00,
                        'Gain/Loss %': 0.0,
                        'Total Return USD': 0.00,
                        'Total Return %': 0.0,
                        'Verified': '🔴 NO DATA'
                    })
                    
                    verification_results.append({
                        'symbol': etf,
                        'main_price': 0.00,
                        'verification': {'error': 'No data available from any source', 'verified': False}
                    })
                    
                    print(f"  🔴 FAILED: No data available from any source")
        
        except Exception as e:
            print(f"  ❌ Unexpected error processing {etf}: {e}")
            # Add failed entry
    results.append({
        'Symbol': etf,
                'Initial Share Price USD': 0.00,
                'Shares Purchased': 0.00,
                'Current Share Price USD': 0.00,
                'Current Portfolio Value USD': 0.00,
                'Dividends Collected USD': 0.00,
                'Gain/Loss USD': 0.00,
                'Gain/Loss %': 0.0,
                'Total Return USD': 0.00,
                'Total Return %': 0.0,
                'Verified': '🔴 ERROR'
            })
    
    # Convert to DataFrame and split into working vs failed ETFs
    results_df = pd.DataFrame(results)
    
    # Separate working ETFs from failed ones
    working_etfs = results_df[~results_df['Verified'].str.contains('🔴', na=False)].copy()
    failed_etfs = results_df[results_df['Verified'].str.contains('🔴', na=False)].copy()
    
    # Display results
    print_results(working_etfs, failed_etfs, verification_results)
    
    # Generate HTML report
    html_content = create_html_report(working_etfs, failed_etfs, INVESTMENT_PER_ETF, START_DATE)
    save_html_report(html_content)
    
    print("\n" + "="*60)
    print(f"Total ETFs Analyzed: {len(INCOME_ETFS)}")
    print("="*60)

def print_results(working_etfs, failed_etfs, verification_results):
    """Print console results"""
    
    # Display working ETFs table
    if not working_etfs.empty:
        print("\n" + "="*200)
        print("Symbol  Initial Share Price USD  Shares Purchased  Current Share Price USD  Current Portfolio Value USD  "
              "Dividends Collected USD  Gain/Loss USD  Gain/Loss %  Total Return USD  Total Return %   Verified")
        print("\n" + "-" * 200)
        
        for _, row in working_etfs.iterrows():
            print(f"  {row['Symbol']:<6} {row['Initial Share Price USD']:>22.2f} {row['Shares Purchased']:>16.2f} "
                  f"{row['Current Share Price USD']:>22.2f} {row['Current Portfolio Value USD']:>27.2f} "
                  f"{row['Dividends Collected USD']:>23.2f} {row['Gain/Loss USD']:>13.2f} {row['Gain/Loss %']:>11.1f} "
                  f"{row['Total Return USD']:>16.2f} {row['Total Return %']:>14.1f} {row['Verified']}")
    
    # Display failed ETFs
    if not failed_etfs.empty:
        print("\n" + "="*60)
        print("FAILED ETFs (No Data Available)")
        print("="*60)
        print("Symbol  Verified")
        
        for _, row in failed_etfs.iterrows():
            print(f"  {row['Symbol']:<6} {row['Verified']}")
    
    # Verification Summary
    verified_count = sum(1 for vr in verification_results if vr['verification'].get('verified', False))
    total_count = len(verification_results)
    
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    print(f"Prices Verified: {verified_count}/{total_count} ETFs")
    print(f"Verification Rate: {(verified_count/total_count*100):.1f}%")
    
    unverified = [vr for vr in verification_results if not vr['verification'].get('verified', False)]
    if unverified:
        print(f"\nUnverified ETFs:")
        for vr in unverified:
            error_msg = vr['verification'].get('error', 'Alternative source used')
            print(f"  {vr['symbol']}: ${vr['main_price']:.2f} - {error_msg}")
    
    # Portfolio Summary
    if not working_etfs.empty:
        print("\n" + "="*60)
        print("PORTFOLIO SUMMARY")
        print("="*60)
        
        # Calculate portfolio totals (using working ETFs)
        total_initial_investment = len(working_etfs) * INVESTMENT_PER_ETF
        total_current_value = working_etfs['Current Portfolio Value USD'].sum()
        total_dividends_collected = working_etfs['Dividends Collected USD'].sum()
        total_gain_loss = total_current_value - total_initial_investment
        total_gain_loss_pct = (total_gain_loss / total_initial_investment * 100) if total_initial_investment > 0 else 0
        
        # Total return including dividends
        total_return_with_dividends = total_current_value + total_dividends_collected - total_initial_investment
        total_return_pct_with_dividends = (total_return_with_dividends / total_initial_investment * 100) if total_initial_investment > 0 else 0
        
        print(f"Working ETFs: {len(working_etfs)}/{len(working_etfs) + len(failed_etfs)}")
        print(f"Total Initial Investment: ${total_initial_investment:,.2f}")
        print(f"Total Current Value: ${total_current_value:,.2f}")
        print(f"Total Dividends Collected: ${total_dividends_collected:,.2f}")
        print(f"Total Gain/Loss (Price Only): ${total_gain_loss:,.2f} ({total_gain_loss_pct:+.1f}%)")
        print(f"Total Return (Price + Dividends): ${total_return_with_dividends:,.2f} ({total_return_pct_with_dividends:+.1f}%)")
        
        # Show best and worst performers
        if not working_etfs.empty:
            best_performer = working_etfs.loc[working_etfs['Gain/Loss %'].idxmax()]
            worst_performer = working_etfs.loc[working_etfs['Gain/Loss %'].idxmin()]
            highest_dividend = working_etfs.loc[working_etfs['Dividends Collected USD'].idxmax()]
            
            print(f"\nBest Price Performer: {best_performer['Symbol']} ({best_performer['Gain/Loss %']:+.1f}%)")
            print(f"Worst Price Performer: {worst_performer['Symbol']} ({worst_performer['Gain/Loss %']:+.1f}%)")
            print(f"Highest Dividend Payer: {highest_dividend['Symbol']} (${highest_dividend['Dividends Collected USD']:.2f})")

# Run the analysis when script is executed directly
if __name__ == "__main__":
    main()
