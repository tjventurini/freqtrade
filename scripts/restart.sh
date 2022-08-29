#!/usr/bin/env bash

# Load config.
source ./scripts/load_colors.sh

# Bring the containers down.
docker-compose down --remove-orphans && docker-compose upd -d && echo -e "${SUCCESS}It's dead now! 💀${NC}"