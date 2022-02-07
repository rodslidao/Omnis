include .env
.PHONY: up
up:
	docker-compose up -d

.PHONY: down
down:
	docker-compose down

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
