docker-compose-up:
	docker compose -f compose.yaml up -d --build

docker-compose-logs:
	docker compose -f compose.yaml logs -f

docker-compose-down:
	docker compose -f compose.yaml stop -t 1
	docker compose -f compose.yaml down

test:
	docker exec tuvino pytest