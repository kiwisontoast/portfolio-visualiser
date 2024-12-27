# Portfolio-Visualiser
The portfolio visualiser is a tool for tracking and analyzing investment portfolios. It provides users with real-time visualization of their portfolio and enables them to experiments with hypothetical portfolio compositions, offering an interface for investment decision-making.

## Key Features
- Managing and visualizing investment portfolios
    - Add and remove stocks with specific investment amounts
    - Real-time portfolio value calculations
    - Dynamic pie chart visualization of portfolio
- Create and analyze hypothetical portfolios
    - Design theoretical portfolio using percentages.
    - Visualize hypothetical portfolio compositions
- User-friendly interface features
    - Dark/light mode button
    - Responsive pie chart display
    - Input fields for stock management
    - Real-time updates of visualizations
    - Automatic window sizing and layout management

## Dependencies
- This project requires:
  ~ yfinance
  ~ matplotlib
  ~ numpy
  ~ tkinter
  ~ sv_ttk

## Usage
**Managing Real Portfolio**
- Enter a stock ticker (e.g.,AAPL,GOOGL)
- Input the investment amount in Dollars
- Click "Add Stock" to include in portfolio
- Use "Remove/Reduce Stock" to decrease positions
- View current portfolio value and allocation

**Creating Hypothetical Portfolios**
- Enter a stock ticker
- Specify desired percentage allocation
- Add to hypothetical portfolio
- Adjust allocations as needed
- Compare different portfolio strategies

**Interface Controls**
- Toggle between dark and light mode using theme switch button
- Create portfolio visualizations using respective buttons
- View real-time updates of portfolio values and allocations

## Warnings
**Operating System Compatibility**
- This is optimized for Windows. While it may run on other operating systems, some visual elements and GUI components might behave differently.
**Data Management**
- Real-time stock data is dependent on yfinance's availability.
- Invalid stock tickers will trigger error handling.
**Portfolio Management**
- Ensure percentages in hypothetical portfolios sum to 100.

## Authors
Dev Shroff & Krishnika Anandan





