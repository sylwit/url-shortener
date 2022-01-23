.PHONY: dump db

dump:
	docker-compose run --rm dynamodump -r local -m backup --host db --port 8000 --accessKey x --secretKey x -s "*" --schemaOnly

db:
	docker-compose up -d db
	sleep 3
	docker-compose run --rm dynamodump -r local -m restore --host db --port 8000 --accessKey x --secretKey x -s "*" --schemaOnly
	docker-compose stop db