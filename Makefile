docker-compose-up:
	docker compose -f compose.dev.yaml up -d --build

docker-compose-logs:
	docker compose -f compose.dev.yaml logs -f

docker-compose-down:
	docker compose -f compose.dev.yaml stop -t 1
	docker compose -f compose.dev.yaml down

create-migration:
ifdef MESSAGE
	docker exec tuvino-api alembic revision --autogenerate -m "$(MESSAGE)"
	docker exec tuvino-api alembic upgrade head
else
	$(error ERROR: La variable MESSAGE no ha sido proporcionada. Uso: make migration MESSAGE="Tu mensaje de migración")
endif

test:
	docker exec tuvino-api pytest

upgrade:
	docker exec tuvino-api alembic upgrade head

restart:
	docker compose -f compose.dev.yaml stop -t 1
	docker compose -f compose.dev.yaml down -v
	make docker-compose-up
	make migrate

downgrade:
ifdef VERSION
	docker exec tuvino-api alembic downgrade "$(VERSION)"
else
	$(error ERROR: Especifique una version a la que retroceder")
endif