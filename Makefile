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
	docker-compose down && docker-compose up -d
	