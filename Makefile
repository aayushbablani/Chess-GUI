BACKEND_FILES := $(shell \
	find ./backend -type f \
		-not -path "./backend/engine/*" \
		-not -path "./backend/stockfish/*" \
		-not -path "./backend/__pycache__/*" \
)

FRONTEND_FILES := $(shell find ./frontend -type f)

all: .chess_backend .chess_frontend DockerCompose.yml
	docker-compose --file DockerCompose.yml up

run: DockerCompose.yml
	docker-compose --file DockerCompose.yml up

build: .chess_backend .chess_frontend

.chess_backend: $(BACKEND_FILES)
	docker build -t chess_backend:latest backend/
	touch .chess_backend
	echo "dummy file to indicate to make if container image exists." > .chess_backend

.chess_frontend: $(FRONTEND_FILES)
	docker build -t chess_frontend:latest frontend/
	touch .chess_frontend
	echo "dummy file to indicate to make if container image exists." > .chess_frontend

clean:
	docker-compose --file DockerCompose.yml down
	docker volume rm chesscom_backendDatabaseStore
	docker rmi chess_backend:latest -f && rm .chess_backend
	docker rmi chess_frontend:latest -f && rm .chess_frontend