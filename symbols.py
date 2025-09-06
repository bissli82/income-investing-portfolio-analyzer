# Extended Income Investing ETF Symbols Configuration
# Comprehensive list of income-focused ETFs and dividend stocks
# Add or remove symbols here to customize your analysis

# Extended ETF list for analysis
INCOME_ETFS = [
    'FSCO',   # FS KKR Capital Corp
    'EIC',    # Eagle Point Income Company Inc
    'OXLC',   # Oxford Lane Capital Corp
    'GOF',    # Guggenheim Strategic Opportunities Fund
    'BBDC',   # Barings BDC Inc
    'FSK',    # FS KKR Capital Corp II
    'XFLT',   # Wright Physical Silver ETF Trust
    'PBDC',   # Apollo Investment Corporation
    'MFC',    # Manulife Financial Corporation
    'JFR',    # Nuveen Floating Rate Income Fund
    'ECC',    # Eagle Point Credit Company Inc
    'KIO',    # KKR Income Opportunities Fund
    'BIZD',   # VanEck BDC Income ETF
    'OCSL',   # Oaktree Specialty Lending Corporation
    'PDI',    # PIMCO Dynamic Income Fund
    'BGH',    # Barings Global Short Duration High Yield Fund
    'EXG',    # Eaton Vance Tax-Managed Global Diversified Equity Income Fund
    'LGI',    # Lazard Global Total Return and Income Fund
    'MPV',    # Barings Participation Investors
    'BRW',    # Saba Capital Income & Opportunities Fund
    'EARN',   # Ellington Residential Mortgage REIT
    'ADX',    # Adams Diversified Equity Fund
    'PDX',    # PIMCO Dynamic Income Opportunities Fund
    'MEGI',   # MainStay CBRE Global Infrastructure Megatrends Fund
    'NIE',    # AllianzGI Equity & Convertible Income Fund
    'PCF',    # Putnam High Income Securities Fund
    'SRV',    # NXG Cushing Midstream Energy Fund
    'BCSF',   # Bain Capital Specialty Finance Inc
    'OCCI',   # OFS Credit Company Inc
    'TRIN',   # Trinity Capital Inc
    'IML',    # Invesco Multi-Sector Income ETF
    'NML',    # Neuberger Berman MLP and Energy Income Fund
    'SPE',    # Special Opportunities Fund Inc
    'RLTY',   # Cohen & Steers Real Estate Opportunities and Income Fund
    'CLM',    # Cornerstone Strategic Value Fund
    'PEO',    # Adams Natural Resources Fund
    'CRF',    # Cornerstone Total Return Fund
    'GDV',    # Gabelli Dividend & Income Trust
    'PAXS',   # PIMCO Access Income Fund
    'DSU',    # Blackstone Debt Strategies Fund
    'GHY',    # PGIM Global High Yield Fund
    'CION',   # CION Investment Corporation
    'CPZ',    # Calamos Long/Short Equity & Dynamic Income Trust
    'NBXG',   # Neuberger Berman Next Generation Connectivity Fund
    'ISD',    # PGIM High Yield Bond Fund
    'USA',    # Liberty All-Star Equity Fund
    'PDO',    # PIMCO Dynamic Income Opportunities Fund
    'ETW',    # Eaton Vance Tax-Managed Global Buy-Write Opportunities Fund
    'BTX',    # Brooklyn ImmunoTherapeutics Inc
    'MARY',   # Procure Space ETF
    'ARDC',   # Ares Dynamic Credit Allocation Fund
    'CII',    # Blackrock Enhanced Capital and Income Fund
    'EVT',    # Eaton Vance Tax Advantaged Dividend Income Fund
    'RYT',    # Invesco S&P 500 Equal Weight Technology ETF
    'EOI',    # Eaton Vance Enhanced Equity Income Fund
    'PDT',    # John Hancock Premium Dividend Fund
    'HTD',    # John Hancock Tax Advantaged Dividend Income Fund
    'ETG',    # Eaton Vance Tax-Advantaged Global Dividend Income Fund
    'BST',    # BlackRock Science and Technology Trust
    'DUI',    # SPDR S&P Dividend ETF
    'RMT',    # Royce Micro-Cap Trust
    'UTF',    # Cohen & Steers Infrastructure Fund
    'FFA',    # First Trust Enhanced Equity Income Fund
    'DST',    # BlackRock Debt Strategies Fund
    'DHF',    # BNY Mellon High Yield Strategies Fund
    'BDJ',    # Blackrock Enhanced Equity Dividend Trust
    'ASG',    # Liberty All-Star Growth Fund
    'BMEZ',   # BlackRock Health Sciences Trust II
    'EOS',    # Eaton Vance Enhanced Equity Income Fund II
    'JCE',    # Nuveen Core Equity Alpha Fund
]

# Investment amount per ETF (in USD)
INVESTMENT_PER_ETF = 10000

# Analysis start date (preferred start date for all ETFs)
# Note: ETFs that started later will use their actual launch date with ** notation
# Format: YYYY-MM-DD (required by yfinance), displayed as DD/MM/YYYY in reports
START_DATE = "2025-01-02"  # 02/01/2025 - January 2nd, 2025

# Optional: Categories for better organization
ETF_CATEGORIES = {
    'Business Development Companies (BDCs)': ['FSCO', 'EIC', 'BBDC', 'FSK', 'PBDC', 'BIZD', 'OCSL', 'BCSF', 'OCCI', 'TRIN', 'CION'],
    'Closed-End Funds - High Yield': ['OXLC', 'GOF', 'JFR', 'ECC', 'KIO', 'PDI', 'BGH', 'PCF', 'IML', 'PAXS', 'DSU', 'GHY', 'ISD'],
    'Closed-End Funds - Equity Income': ['EXG', 'LGI', 'MPV', 'BRW', 'ADX', 'PDX', 'CLM', 'PEO', 'CRF', 'GDV', 'CPZ', 'USA', 'EVT', 'EOI', 'PDT', 'HTD', 'ETG', 'BST', 'RMT', 'FFA', 'BDJ', 'ASG', 'EOS', 'JCE'],
    'Specialty Income': ['XFLT', 'MFC', 'MEGI', 'NIE', 'SRV', 'NML', 'SPE', 'RLTY', 'NBXG', 'ETW', 'BTX', 'MARY', 'ARDC', 'CII', 'RYT', 'DUI', 'UTF', 'DST', 'DHF', 'BMEZ'],
    'REITs & Real Estate': ['EARN', 'RLTY', 'UTF'],
}

# Optional: Expected dividend frequencies (for reference)
DIVIDEND_FREQUENCY = {
    'Monthly': ['OXLC', 'FSK', 'EIC', 'GOF', 'BBDC', 'PBDC', 'ECC', 'KIO', 'OCSL', 'BGH', 'MPV', 'BRW', 'EARN', 'MEGI', 'BCSF', 'OCCI', 'TRIN', 'CLM', 'CRF', 'GDV', 'PAXS', 'DSU', 'GHY', 'CION'],
    'Quarterly': ['FSCO', 'JFR', 'BIZD', 'PDI', 'EXG', 'LGI', 'ADX', 'PDX', 'NIE', 'PCF', 'SRV', 'IML', 'NML', 'SPE', 'RLTY', 'PEO', 'CPZ', 'NBXG', 'ISD', 'USA', 'PDO', 'ETW', 'ARDC', 'CII', 'EVT', 'RYT', 'EOI', 'PDT', 'HTD', 'ETG', 'BST', 'DUI', 'RMT', 'UTF', 'FFA', 'DST', 'DHF', 'BDJ', 'ASG', 'BMEZ', 'EOS', 'JCE'],
    'Semi-Annual': ['XFLT', 'MFC'],
    'Variable/Unknown': ['BTX', 'MARY'],
}

# Optional: Risk levels (for reference)
RISK_LEVELS = {
    'Conservative': ['MFC', 'DUI', 'UTF', 'USA', 'ASG'],
    'Moderate': ['FSCO', 'EIC', 'BBDC', 'FSK', 'BIZD', 'PDI', 'EXG', 'LGI', 'ADX', 'IML', 'EVT', 'EOI', 'PDT', 'HTD', 'ETG', 'RMT', 'FFA', 'BDJ', 'EOS', 'JCE'],
    'Aggressive': ['OXLC', 'GOF', 'PBDC', 'JFR', 'ECC', 'KIO', 'BGH', 'MPV', 'BRW', 'EARN', 'PDX', 'MEGI', 'NIE', 'PCF', 'SRV', 'BCSF', 'OCCI', 'TRIN', 'NML', 'SPE', 'RLTY', 'CLM', 'PEO', 'CRF', 'GDV', 'PAXS', 'DSU', 'GHY', 'CION', 'CPZ', 'NBXG', 'ISD', 'PDO', 'ETW', 'ARDC', 'CII', 'BST', 'DST', 'DHF', 'BMEZ'],
    'High Risk': ['XFLT', 'BTX', 'MARY', 'RYT'],
}
