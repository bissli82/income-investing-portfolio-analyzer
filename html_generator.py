# HTML Report Generator for Income Investing Analysis
import pandas as pd
from datetime import datetime

def format_date_dd_mm_yyyy(date_str):
    """Convert date from YYYY-MM-DD to DD/MM/YYYY format"""
    try:
        import pandas as pd
        date_obj = pd.to_datetime(date_str)
        return date_obj.strftime('%d/%m/%Y')
    except:
        return date_str

def create_html_report(working_etfs_df, failed_etfs_df, investment_amount, start_date):
    """Generate HTML report with portfolio analysis"""
    
    # Calculate totals
    total_initial_investment = len(working_etfs_df) * investment_amount
    total_current_value = working_etfs_df['Current Portfolio Value USD'].sum()
    total_dividends_collected = working_etfs_df['Dividends Collected USD'].sum()
    total_gain_loss = total_current_value - total_initial_investment
    total_gain_loss_pct = (total_gain_loss / total_initial_investment * 100) if total_initial_investment > 0 else 0
    total_return_with_dividends = total_current_value + total_dividends_collected - total_initial_investment
    total_return_pct_with_dividends = (total_return_with_dividends / total_initial_investment * 100) if total_initial_investment > 0 else 0
    
    # Format dates
    formatted_start_date = format_date_dd_mm_yyyy(start_date)
    
    # Collect ETFs that started later (with **) for footnotes
    fallback_etfs = []
    if 'Is Fallback' in working_etfs_df.columns:
        for _, row in working_etfs_df.iterrows():
            if row.get('Is Fallback', False):
                original_symbol = row.get('Original Symbol', row['Symbol'].replace('**', ''))
                formatted_date = row.get('Formatted Start Date', 'Unknown')
                fallback_etfs.append(f"**{original_symbol}: Started trading on {formatted_date}")
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Income Investing Analysis</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            max-width: 1400px;
            margin: 0 auto;
            overflow-x: auto;
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .info {{
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 25px;
            text-align: center;
            color: #34495e;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 13px;
            min-width: 1200px;
        }}
        th {{
            background-color: #3498db;
            color: white;
            padding: 10px 8px;
            text-align: center;
            font-weight: bold;
            cursor: pointer;
            font-size: 12px;
            user-select: none;
            position: relative;
        }}
        th:hover {{
            background-color: #2980b9;
        }}
        th.sort-asc::after {{
            content: ' ↑';
            position: absolute;
            right: 5px;
            opacity: 1;
        }}
        th.sort-desc::after {{
            content: ' ↓';
            opacity: 1;
        }}
        td {{
            padding: 8px 6px;
            border-bottom: 1px solid #ddd;
            text-align: center;
        }}
        .symbol {{
            text-align: center;
        }}
        .currency {{
            text-align: center;
        }}
        .shares {{
            text-align: center;
        }}
        .verification {{
            text-align: center;
        }}
        .gain {{
            color: #27ae60;
            font-weight: bold;
        }}
        .loss {{
            color: #e74c3c;
            font-weight: bold;
        }}
        .fallback-etf {{
            background-color: #ffebee !important;
        }}
        .summary {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-top: 30px;
            border-left: 4px solid #3498db;
        }}
        .summary h3 {{
            color: #2c3e50;
            margin-top: 0;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .summary-item {{
            background: white;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .summary-value {{
            font-size: 1.2em;
            font-weight: bold;
            color: #2c3e50;
        }}
        .summary-label {{
            font-size: 0.9em;
            color: #7f8c8d;
            margin-top: 5px;
        }}
        .positive {{ color: #27ae60; }}
        .negative {{ color: #e74c3c; }}
        .failed-table {{
            margin-top: 40px;
        }}
        .failed-table h2 {{
            color: #e74c3c;
        }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/sortable-tablesort@2.0.1/sortable.min.js"></script>
</head>
<body>
    <div class="container">
        <h1>📊 Income Investing Portfolio Analysis</h1>
        
        <div class="info">
            <strong>Analysis Date:</strong> {datetime.now().strftime("%d/%m/%Y")} | 
            <strong>Reference Date:</strong> {formatted_start_date} | 
            <strong>Investment per ETF:</strong> ${investment_amount:,.2f}
        </div>

        <div class="summary">
            <h3>💰 Portfolio Summary</h3>
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="summary-value">${total_initial_investment:,.2f}</div>
                    <div class="summary-label">Initial Investment</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">${total_current_value:,.2f}</div>
                    <div class="summary-label">Current Value</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">${total_dividends_collected:,.2f}</div>
                    <div class="summary-label">Dividends Collected</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value {'positive' if total_gain_loss >= 0 else 'negative'}">${total_gain_loss:,.2f}</div>
                    <div class="summary-label">Price Gain/Loss ({total_gain_loss_pct:+.1f}%)</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value {'positive' if total_return_with_dividends >= 0 else 'negative'}">${total_return_with_dividends:,.2f}</div>
                    <div class="summary-label">Total Return ({total_return_pct_with_dividends:+.1f}%)</div>
                </div>
                <div class="summary-item">
                    <div class="summary-value">{len(working_etfs_df)}/{len(working_etfs_df) + len(failed_etfs_df)}</div>
                    <div class="summary-label">Working ETFs</div>
                </div>
            </div>
        </div>

        <h2 style="color: #2c3e50; margin-top: 30px;">📈 Active Portfolio</h2>
        <table id="resultsTable" class="sortable">
            <thead>
                <tr>
                    <th data-sort="string">Symbol</th>
                    <th data-sort="float">Initial Price (USD)</th>
                    <th data-sort="float">Shares Purchased</th>
                    <th data-sort="float">Current Price (USD)</th>
                    <th data-sort="float">Current Value (USD)</th>
                    <th data-sort="float">Dividends Collected (USD)</th>
                    <th data-sort="float">Gain/Loss (USD)</th>
                    <th data-sort="float">Gain/Loss (%)</th>
                    <th data-sort="float">Total Return (USD)</th>
                    <th data-sort="float">Total Return (%)</th>
                    <th data-sort="string">Status</th>
                </tr>
            </thead>
            <tbody>
    """
    
    # Add working ETF rows
    for _, row in working_etfs_df.iterrows():
        row_class = ""
        
        # Check if this is a fallback ETF (started later) and add red background
        if '**' in str(row['Symbol']):
            row_class = 'fallback-etf'
        
        # Determine gain/loss color
        gain_loss_class = ""
        if row['Gain/Loss USD'] > 0:
            gain_loss_class = 'gain'
        elif row['Gain/Loss USD'] < 0:
            gain_loss_class = 'loss'
        
        # Determine total return class for styling
        total_return_class = ''
        if row['Total Return USD'] > 0:
            total_return_class = 'gain'
        elif row['Total Return USD'] < 0:
            total_return_class = 'loss'
        
        html_content += f"""
                <tr class="{row_class}">
                    <td class="symbol">{row['Symbol']}</td>
                    <td class="currency" data-sort="{row['Initial Share Price USD']}">${row['Initial Share Price USD']:.2f}</td>
                    <td class="shares" data-sort="{row['Shares Purchased']}">{row['Shares Purchased']:.2f}</td>
                    <td class="currency" data-sort="{row['Current Share Price USD']}">${row['Current Share Price USD']:.2f}</td>
                    <td class="currency" data-sort="{row['Current Portfolio Value USD']}">${row['Current Portfolio Value USD']:,.2f}</td>
                    <td class="currency" data-sort="{row['Dividends Collected USD']}">${row['Dividends Collected USD']:,.2f}</td>
                    <td class="currency {gain_loss_class}" data-sort="{row['Gain/Loss USD']}">${row['Gain/Loss USD']:,.2f}</td>
                    <td class="currency {gain_loss_class}" data-sort="{row['Gain/Loss %']}">{row['Gain/Loss %']:+.1f}%</td>
                    <td class="currency {total_return_class}" data-sort="{row['Total Return USD']}">${row['Total Return USD']:,.2f}</td>
                    <td class="currency {total_return_class}" data-sort="{row['Total Return %']}">{row['Total Return %']:+.1f}%</td>
                    <td class="verification">{row['Verified']}</td>
                </tr>
        """
    
    html_content += """
            </tbody>
        </table>
    """
    
    # Add failed ETFs table if there are any
    if not failed_etfs_df.empty:
        html_content += """
        <div class="failed-table">
            <h2>❌ Failed to Retrieve Data</h2>
            <table>
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for _, row in failed_etfs_df.iterrows():
            html_content += f"""
                    <tr>
                        <td class="symbol">{row['Symbol']}</td>
                        <td class="verification">{row['Verified']}</td>
                    </tr>
            """
        
        html_content += """
                </tbody>
            </table>
        </div>
        """
    
    # Add footnotes if there are any fallback ETFs
    if fallback_etfs:
        html_content += """
        <div style="margin-top: 30px; padding: 20px; background-color: #f8f9fa; border-radius: 8px; border-left: 4px solid #17a2b8;">
            <h3 style="color: #2c3e50; margin-top: 0;">📝 Notes</h3>
            <ul style="margin: 10px 0; padding-left: 20px;">
        """
        
        for note in fallback_etfs:
            html_content += f"<li>{note}</li>"
        
        html_content += """
            </ul>
            <p style="margin-bottom: 0; font-style: italic; color: #6c757d;">
                ETFs marked with ** started trading after the preferred reference date and use their actual launch date.
            </p>
        </div>
        """
    
    html_content += """
    </div>
    
    <script>
        // Initialize sortable tables
        document.addEventListener('DOMContentLoaded', function() {
            const table = document.getElementById('resultsTable');
            if (table) {
                new Sortable(table, {
                    headers: {
                        0: { sorter: 'text' },
                        1: { sorter: 'digit' },
                        2: { sorter: 'digit' },
                        3: { sorter: 'digit' },
                        4: { sorter: 'digit' },
                        5: { sorter: 'digit' },
                        6: { sorter: 'digit' },
                        7: { sorter: 'digit' },
                        8: { sorter: 'digit' },
                        9: { sorter: 'digit' },
                        10: { sorter: 'text' }
                    }
                });
            }
        });
    </script>
</body>
</html>
    """
    
    return html_content

def save_html_report(html_content, filename="income_investing_report.html"):
    """Save HTML content to file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML Report Generated: {filename}")
