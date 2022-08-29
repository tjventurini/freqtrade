init:
	@bash ./scripts/init.sh

up:
	@bash ./scripts/up.sh

start: up

down:
	@bash ./scripts/down.sh

stop: down

clear:
	@bash ./scripts/clear.sh

restart:
	@bash ./scripts/restart.sh