all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

validate_env:
	@command -v docker > /dev/null || (echo "You need to install docker and docker-compose before proceeding" && exit 1)
	@command -v docker-compose > /dev/null || (echo "You need to install docker and docker-compose before proceeding" && exit 1)

build: delete-container ## Build the container
	@docker-compose build
	@docker-compose up -d

test: start ## Run tests
	@docker-compose exec backend pytest

restart: ## Restart the container
	@docker-compose restart app

cmd: start ## Access bash
	@docker-compose exec app /bin/bash

shell: start ## Access django shell
	@docker-compose exec app /bin/bash -c "./manage.py shell"

up: start ## Start django dev server
	@docker-compose exec app /bin/bash -c "./manage.py runserver 0.0.0.0:8000"

start:
	@docker-compose start

down: ## Stop container
	@docker-compose stop || true

delete-container: down
	@docker-compose down || true

remove: delete-container ## Delete containers and images

.DEFAULT_GOAL := help
