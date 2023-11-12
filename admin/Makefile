db-up:
	docker compose up --build -d

kill:
	[[ $(docker ps -q) = "" ]] || docker kill $(docker ps -q) && yes | docker system prune -a && [[ $(docker ps -a | wc -l | xargs) == "1" && $(docker images | wc -l | xargs) == "1" ]] && docker volume rm $(docker volume ls -q) && docker network rm $(docker network ls -q); sudo rm -Rvf ./data; echo "Done"

connect:
	docker exec -it postgres psql -U admin admin_db

lint:
	black app.py app/ && flake8 app.py app/


.PHONY: db-up db-kill connect
