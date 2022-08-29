#!/usr/bin/env bash

# Load config.
source ./scripts/load_colors.sh

# Start the containers.
docker-compose up -d && echo -e "${SUCCESS}It's alive! 🧟${NC}"