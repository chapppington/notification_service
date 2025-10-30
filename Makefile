APP_CONTAINER = main-app
STORAGES_CONTAINER = mongodb
CELERY_WORKER_CONTAINER = celery-worker
REDIS_CONTAINER = redis
APP_FILE = docker_compose/app.yaml
STORAGES_FILE = docker_compose/storages.yaml
CELERY_FILE = docker_compose/celery.yaml
DC = docker compose
ENV_FILE = --env-file .env
EXEC = docker exec -it
LOGS = docker logs

.PHONY: all
all:
	${DC} -f ${STORAGES_FILE} -f ${CELERY_FILE} -f ${APP_FILE} ${ENV_FILE} up --build -d

.PHONY: all-down
all-down:
	${DC} -f ${STORAGES_FILE} -f ${CELERY_FILE} -f ${APP_FILE} ${ENV_FILE} down

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV_FILE} up  --build -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: storages-logs
storages-logs:
	${LOGS} ${STORAGES_CONTAINER} -f

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV_FILE} up  --build -d

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: celery
celery:
	${DC} -f ${CELERY_FILE} ${ENV_FILE} up --build -d

.PHONY: celery-down
celery-down:
	${DC} -f ${CELERY_FILE} down

.PHONY: celery-logs
celery-logs:
	${LOGS} ${CELERY_WORKER_CONTAINER} -f

.PHONY: redis-cli
redis-cli:
	${EXEC} ${REDIS_CONTAINER} redis-cli

.PHONY: flower
flower:
	@echo "Flower UI available at http://localhost:5555"

.PHONY: precommit 
precommit:
	pre-commit run --all-files

.PHONY: test
test:
	pytest -v