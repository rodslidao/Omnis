include .env
.PHONY: up
up:
	docker pull omnisofc/backend:latest && \
	docker-compose up -d

.PHONY: down
down:
	docker-compose down

.PHONY: logs
logs:
	docker-compose logs -f

.PHONY: graph_up
graph_up:
	docker-compose  --env-file=.env --file ./elasticstack/elastic-compose.yml up -d --build

.PHONY: graph_down
graph_down:
	docker-compose --env-file=.env --file ./elasticstack/elastic-compose.yml down

.PHONY: restart
restart:
	docker-compose restart

.PHONY: restart-force
restart-force:
	docker-compose down && docker-compose up -d

.PHONY: build
build:
	docker-compose build
