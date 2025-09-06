# 📊 Income Investing Portfolio Analyzer

A comprehensive Python tool for analyzing income-focused ETF portfolios, tracking dividends, and calculating total returns with beautiful HTML reports.

## 🎯 What This Tool Does

This analyzer helps income investors track their ETF portfolio performance by:

- **📈 Real-time price tracking** - Fetches current and historical ETF prices
- **💰 Dividend collection analysis** - Calculates total dividends received over time
- **🔍 Price verification** - Cross-validates prices using multiple data sources
- **📊 Total return calculation** - Shows both price performance AND dividend income
- **🎨 Beautiful HTML reports** - Generates sortable, interactive reports
- **⚙️ Easy customization** - Simple configuration file for managing ETF symbols

## 📋 Sample Output

The tool analyzes your portfolio and shows:

```
Symbol  Initial Price  Current Price  Portfolio Value  Dividends Collected  Total Return
MSTY    $27.14        $15.62         $5,755.34       $5,295.14           +10.5% ✅
YBTC    $50.00        $45.22         $9,044.00       $2,927.80           +19.7% ✅
IGLD    $18.86        $22.73         $12,051.96      $602.33             +26.5% ✅
```

**Key Insight:** Many income ETFs show negative price performance but positive total returns when dividends are included!

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (Check with: `python --version`)
- **uv package manager** (Recommended) or pip

### Installation

#### Option 1: Using uv (Recommended)

1. **Install uv** (if you don't have it):
   ```bash
   # Windows (PowerShell)
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and run**:
   ```bash
   git clone <your-repo-url>
   cd "Income Investing"
   uv run python main.py
   ```

#### Option 2: Using pip

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd "Income Investing"
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install yfinance pandas
   ```

4. **Run the analyzer**:
   ```bash
   python main.py
   ```

## ⚙️ Configuration

### Adding/Removing ETFs

Edit `symbols.py` to customize your portfolio:

```python
# Add or remove ETF symbols here
INCOME_ETFS = [
    'QYLD',   # Global X NASDAQ 100 Covered Call ETF
    'JEPI',   # JPMorgan Equity Premium Income ETF
    'SCHD',   # Schwab US Dividend Equity ETF
    # Add your ETFs here!
]

# Change investment amount per ETF
INVESTMENT_PER_ETF = 10000  # $10,000 per ETF

# Change analysis start date
START_DATE = "2025-01-02"  # When you started investing
```

### Supported ETF Categories

The tool works with various income-focused ETFs:

- **Covered Call ETFs**: QYLD, SPYI
- **YieldMax Options**: CONY, MSTY, NVDY, YBTC, YMAG, YMAX
- **Income Funds**: CCIF, OXLC
- **Dividend ETFs**: Any dividend-paying ETF

## 📁 Project Structure

```
Income Investing/
├── main.py              # Entry point - run this!
├── symbols.py           # ETF configuration (edit this to add/remove ETFs)
├── Analysis.py          # Main analysis logic
├── data_fetcher.py      # Price and dividend data retrieval
├── verification.py      # Price verification and validation
├── html_generator.py    # HTML report generation
├── pyproject.toml       # Project dependencies
└── README.md           # This file
```

## 📊 Understanding the Output

### Console Output
- **Real-time progress** as each ETF is processed
- **Verification status** for data accuracy
- **Portfolio summary** with key metrics

### HTML Report (`income_investing_report.html`)
- **Interactive table** with sortable columns
- **Color-coded gains/losses** (green = profit, red = loss)
- **Portfolio summary** with total returns
- **Responsive design** that works on all devices

### Key Metrics Explained

- **Initial Share Price**: Price when you started investing (Jan 2, 2025)
- **Current Share Price**: Most recent market price
- **Dividends Collected**: Total dividend income received
- **Gain/Loss**: Price performance only (excludes dividends)
- **Total Return**: Complete performance including dividends
- **Verification Status**: 
  - ✅ VERIFIED: Price confirmed by multiple sources
  - 🟡 ALT SOURCE: Alternative source used
  - 🔴 NO DATA: Unable to retrieve data

## 🔧 Troubleshooting

### Common Issues

**"uv: command not found"**
- Install uv using the installation commands above

**"No module named 'yfinance'"**
- Run `uv add yfinance pandas` or `pip install yfinance pandas`

**ETF showing "🔴 NO DATA"**
- ETF might be delisted or have a different symbol
- Check the symbol on Yahoo Finance
- Remove from `symbols.py` if no longer available

**Prices look wrong**
- The tool uses raw market prices (not dividend-adjusted)
- Prices are verified using multiple sources
- Check the verification status in the output

### Getting Help

1. **Check the console output** for detailed error messages
2. **Verify ETF symbols** on [Yahoo Finance](https://finance.yahoo.com)
3. **Update dependencies**: `uv sync` or `pip install --upgrade yfinance pandas`

## 🎯 Advanced Usage

### Running Analysis for Different Periods

Edit `START_DATE` in `symbols.py`:
```python
START_DATE = "2024-01-01"  # Analyze from beginning of 2024
```

### Customizing Investment Amounts

```python
INVESTMENT_PER_ETF = 5000   # $5,000 per ETF instead of $10,000
```

### Adding New Data Sources

The modular design makes it easy to extend:
- Add new data sources in `data_fetcher.py`
- Enhance verification in `verification.py`
- Customize reports in `html_generator.py`

## 📈 Sample Results

Based on real data, here's what the tool revealed about income ETFs:

**Price vs. Total Return Analysis:**
- **CONY**: -48% price performance → **-3.4% total return** (dividends saved the day!)
- **MSTY**: -43% price performance → **+9.2% total return** (massive dividend income)
- **YBTC**: -10% price performance → **+18.8% total return** (monthly dividends rock!)

**Key Insight**: Income investing isn't about price appreciation—it's about total return including dividends!

## 🛠️ Technical Details

- **Data Source**: Yahoo Finance via yfinance library
- **Price Verification**: Multi-source cross-validation
- **Dividend Tracking**: Historical dividend collection analysis
- **Report Generation**: Dynamic HTML with CSS styling and JavaScript sorting
- **Error Handling**: Robust error handling for missing data

## 📝 License

This project is open source. Feel free to modify and distribute.

## 🤝 Contributing

Found a bug or want to add a feature? 
1. Fork the repository
2. Make your changes
3. Test with your own portfolio
4. Submit a pull request

## 🎉 Happy Investing!

Remember: **Income investing is a marathon, not a sprint.** This tool helps you see the complete picture of your returns, including the dividends that make income investing so powerful!

---

*Disclaimer: This tool is for educational and analysis purposes only. Not financial advice. Always do your own research before investing.*
