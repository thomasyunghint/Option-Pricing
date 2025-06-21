# Real-Time Option Analytics Dashboard

This project implements a web-based dashboard for real-time option pricing analytics. Users input a ticker (e.g. AAPL, NVDA, GOOG, etc.), strike, expiration, and option type; the app fetches live market data, shows the current stock price and a historical price chart, computes and displays Option Greeks, and visualizes the implied volatility surface.




---

### Key Features
1. Live Market Data
  - Streams real-time underlying prices and option chains, with auto-retry and lightweight caching for sub-second refresh.
2. Black-Scholes Pricing Engine & Greeks
3. Implied-Vol Surface Builder
  - Extracts IVs across strikes/expiries, fits a smooth 3-D surface (SABR/SVI), and flags anomalies or stale quotes.
4. Interactive Visual Dashboard
  - Dash + Plotly UI showing historical price chart, Greek curves, and a rotatable IV surface; all inputs are reactive sliders/dropdowns.





---


**Author:** Thomas Tse
**Mentor:** Mitch Gao, Ph.D. — Director, Desk Quant (Unified Global Markets), UBS
