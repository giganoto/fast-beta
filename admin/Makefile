.PHONY: up kill connect lint clean-containers clean-volumes clean-networks help

up:
	docker compose up --build -d

kill:
	docker kill $$(docker ps -q) || true
	docker system prune -a -f
	docker volume rm $$(docker volume ls -q) || true
	docker network rm $$(docker network ls -q) || true
	sudo rm -rf ./data
	echo "Cleanup complete"

connect:
	docker exec -it postgres psql -U admin admin_db

lint:
	black app.py app/ && flake8 app.py app/

help:
	@echo "up: Start all services"
	@echo "kill: Stop and remove all containers, networks, and volumes"
	@echo "connect: Connect to the PostgreSQL database"
	@echo "lint: Run linting tools on the codebase"
