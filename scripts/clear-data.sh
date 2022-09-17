#!/usr/bin/env bash

# Load config.
source ./scripts/load_colors.sh

# Remove candle data
find ./user_data/data/* -maxdepth 0 -type d | xargs rm -r && echo -e "${SUCCESS}Data directory cleared! 🧹${NC}"

# Remove backtesting results
rm ./user_data/backtest_results/*.json && echo -e "${SUCCESS}Bcktest results directory cleared! 🧹${NC}"