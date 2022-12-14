PROJECT_NAME?=potoo

SOURCE_DIRS=src airflow
TEST_DIRS=src/potoo/tests

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: help
help:
	@echo "\033[1;37m$(PROJECT_NAME)\033[0m :: Available Commands"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | sed -e "s/^Makefile://" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

pythonpath: ## Configure PYTHONPATH
	@export PYTHONPATH="$PYTHONPATH:$PWD/src/"

k3d-start:  ## Start a new k3d cluster
	@k3d cluster create $(PROJECT_NAME) \
		--agents 2 \
		--registry-create registry:0.0.0.0:8008 \
		--k3s-node-label type=agent@agent:0,1 \
		--volume "$(PWD)/.data/:/data@agent:0,1"

data-reset: ## Wipe out all database data
	@rm -rf .data/postgresql.cluster
	@rm -rf .data/.user_scripts_initialized

k3d-stop:  ## Stop the k3d cluster
	@k3d cluster delete $(PROJECT_NAME)

tilt: ## Deploy and start your dev flow
	@tilt up

_guard-%:
	@#$(or ${$*}, $(error $* is not set))

.PHONY: airflow
airflow:  ## Open Airflow dashboard
	@open http://localhost:8080/

.PHONY: superset
superset:  ## Open Airflow dashboard
	@open http://localhost:8088/

migration-create: _guard-MSG  ## Create a new Alembic migration
	@cd src/potoo && alembic revision --autogenerate -m ${MSG}

migration-exec: ## Run all migrations
	@cd src/potoo && alembic upgrade head

image: ## Build the image
	@docker build . --tag hlushko/potoo

lint: ## Lint source code
	@echo "🛠 isort"
	@isort $(SOURCE_DIRS)
	@echo "🛠 black"
	@black $(SOURCE_DIRS)
	@echo "🛠 flake8"
	@flake8 $(SOURCE_DIRS)
	@echo "🛠 mypy"
	@mypy $(SOURCE_DIRS)

tests: ## Run tests
	@pytest $(TEST_DIRS)