#!/usr/bin/env bash

# Load config.
source ./scripts/load_colors.sh

# Bring the containers down.
docker-compose down --remove-orphans && docker-compose up -d && echo -e "${SUCCESS}It was dead 💀 But it came back to live! 🧟${NC}"