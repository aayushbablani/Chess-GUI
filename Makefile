run_backend: build_backend
	docker-compose --file DockerCompose.yml up

build_backend: backend/Dockerfile backend/requirements.txt backend/main.py backend/database.py
	docker build -t chess_backend:latest backend/

clean:
	docker-compose --file DockerCompose.yml down
	docker volume rm chesscom_backendDatabaseStore
	docker rmi chess_backend:latest -f