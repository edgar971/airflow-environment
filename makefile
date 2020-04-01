build:
	docker-compose build --no-cache
	docker-compose pull
start:
	docker-compose up -d
stop:
	docker-compose stop
clean:
	docker-compose down -v
