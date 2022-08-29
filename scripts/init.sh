#!/usr/bin/env bash

# Load configurations.
source ./scripts/load_colors.sh

# Function to show help message.
function showHelp() {
    echo -e "${WARN}Usage (Makefile): make init${NC}"
}

# Get the correct environment if given.
if [ ! -z "$1" ]; then
    case "$1" in
        --prod)
            ENVIRONMENT="prod"
            ;;
        --local)
            ENVIRONMENT="local"
            ;;
        *)
            showHelp
            exit 1
            ;;
    esac
fi

# Let the user select the environment if not given.
if [ -z "$ENVIRONMENT" ]; then
    echo -e "${WARN}Select environment:${NC}"
    select env in "prod" "local"; do
        case $env in
            prod)
                ENVIRONMENT="prod"
                break
                ;;
            local)
                ENVIRONMENT="local"
                break
                ;;
            *)
                showHelp
                exit 1;
                ;;
        esac
    done
fi

# Link the correct docker-compose.<ENVIRONMENT>.yml file if there is none yet.
if test ! -f docker-compose.yml; then
    ln --symbolic --relative ./docker-compose.$ENVIRONMENT.yml ./docker-compose.yml
    echo -e "${SUCCESS}docker-compose.yml was created ✅${NC}"
else
    echo -e "${WARN}docker-compose.yml already exists, skipping...${NC}"
fi

# Copy .env.example to .env if there is none yet.
if test ! -f .env; then
    cp .env.example .env
    echo -e "${SUCCESS}.env was created ✅${NC}"
else
    echo -e "${WARN}.env already exists, skipping...${NC}"
fi

# Print some info
echo -e "${SUCCESS}Done! 🚀${NC}"
echo -e "${WARN}Please update your '.env' file now 🧐${NC}"
echo -e "${WARN}Afterwards you can execute 'make start' to start the service.${NC}"

# Exit sucessfully.
exit 0