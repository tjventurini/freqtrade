#!/usr/bin/env bash

# Load config.
source ./scripts/load_colors.sh

# Clean up.
if test -f docker-compose.yml; then
    docker-compose down --remove-orphans && echo -e "${SUCCESS}Stopped containers ✅${NC}"
    rm ./docker-compose.yml && echo -e "${SUCCESS}Removed docker-compose.yml ✅${NC}"
fi
if test -f .env; then
    rm ./.env && echo -e "${SUCCESS}Removed .env ✅${NC}"
fi

echo -e "${SUCCESS}It's clear now 🧹${NC}"