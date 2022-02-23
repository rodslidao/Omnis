include .env
.PHONY: up
up:
	docker-compose -f ./docker-compose.yml -f ./elasticstack/elastic-compose.yml up -d --build

.PHONY: down
down:
	docker-compose -f ./docker-compose.yml -f ./elasticstack/elastic-compose.yml down

.PHONY: logs
logs:
	docker-compose logs -f

.PHONY: restart
restart:
	docker-compose restart

.PHONY: restart-force
restart-force:
	docker-compose down && docker-compose up -d

.PHONY: build
build:
	docker-compose build
