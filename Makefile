docker-compose-up:
	docker compose -f compose.dev.yaml up -d --build

docker-compose-logs:
	docker compose -f compose.dev.yaml logs -f

docker-compose-down:
	docker compose -f compose.dev.yaml stop -t 1
	docker compose -f compose.dev.yaml down

test:
	docker exec tuvino-api pytest