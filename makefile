build:
	docker-compose build --no-cache
start:
	docker-compose up -d
stop:
	docker-compose stop
clean:
	docker-compose down -v
