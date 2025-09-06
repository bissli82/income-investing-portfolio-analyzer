# Income Investing ETF Symbols Configuration
# Add or remove symbols here to customize your analysis

# Main ETF list for analysis
INCOME_ETFS = [
    'CCIF',   # Capital City Income Fund
    'CONY',   # YieldMax COIN Option Income Strategy ETF
    'HHIS',   # Harvest Diversified High Income Shares ETF (Launched Jan 2025)
    'IGLD',   # FT Cboe Vest Gold Strategy Quarterly Buffer ETF
    'MSTE',   # Harvest MicroStrategy Enhanced High Income Shares ETF (Launched Mar 5, 2025)
    'MSTY',   # YieldMax TSLA Option Income Strategy ETF
    'NVDY',   # YieldMax NVDA Option Income Strategy ETF
    'OXLC',   # Oxford Lane Capital Corp
    'QDTE',   # FlexShares Nasdaq-100 Dynamic Tail Hedge ETF
    'QQQI',   # Invesco NASDAQ Next Gen 100 ETF
    'QYLD',   # Global X NASDAQ 100 Covered Call ETF
    'SPYI',   # NEOS S&P 500 High Income ETF
    'USCL',   # GraniteShares 1.25x Long US Large Cap ETF
    'XFLT',   # Wright Physical Silver ETF Trust
    'YBTC',   # YieldMax BTC Option Income Strategy ETF
    'YMAG',   # YieldMax Magnificent 7 Fund of Option Income ETFs
    'YMAX',   # YieldMax Universe Fund of Option Income ETFs
]

# Investment amount per ETF (in USD)
INVESTMENT_PER_ETF = 10000

# Analysis start date (preferred start date for all ETFs)
# Note: ETFs that started later will use their actual launch date with ** notation
# Format: YYYY-MM-DD (required by yfinance), displayed as DD/MM/YYYY in reports
START_DATE = "2025-01-02"  # 02/01/2025 - January 2nd, 2025

# Optional: Categories for better organization
ETF_CATEGORIES = {
    'Covered Call': ['QYLD', 'SPYI'],
    'YieldMax Options': ['CONY', 'MSTE', 'MSTY', 'NVDY', 'YBTC', 'YMAG', 'YMAX'],
    'Income Funds': ['CCIF', 'OXLC'],
    'Specialty': ['HHIS', 'IGLD', 'QDTE', 'QQQI', 'USCL', 'XFLT'],
}

# Optional: Expected dividend frequencies (for reference)
DIVIDEND_FREQUENCY = {
    'Monthly': ['YMAX', 'YMAG', 'YBTC'],
    'Quarterly': ['CCIF', 'CONY', 'IGLD', 'MSTY', 'NVDY', 'OXLC', 'QDTE', 'QQQI', 'QYLD', 'SPYI', 'XFLT'],
    'Semi-Annual': ['USCL'],
    'Unknown': ['HHIS', 'MSTE'],
}
