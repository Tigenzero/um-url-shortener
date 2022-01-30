OK="OK ${CNone}"
ROOT_DIR := $(shell pwd)
export FLASK_APP=app.short_url
REDIS_SERVER = "127.0.0.1"
REDIS_PORT = "6379"

venv:
	@echo "Creating virtual environment"
	pip3 install --upgrade --user pipenv; \
	python3 -m pipenv install;
	@echo "${OK}"
.PHONY: venv

unit-test: venv
	export PYTHONPATH=${PYTHONPATH}:${ROOT_DIR}; \
	export REDIS_PORT=${REDIS_PORT}; \
	export REDIS_SERVER=${REDIS_SERVER}; \
	python3 -m pipenv check; \
	python3 -m pipenv install --dev; \
	python3 -m pipenv run python3 -m unittest;
	@echo "${OK}"

integration-test: venv
	export PYTHONPATH=${PYTHONPATH}:${ROOT_DIR}; \
	python3 -m pipenv check; \
	python3 -m pipenv install --dev; \
	python3 -m pipenv run python3 -m integtest;
	@echo "${OK}"

get_redis:
	@echo "Getting Redis"
	docker pull redis; \
	docker container create -p ${REDIS_PORT}:${REDIS_PORT} --name ${REDIS_SERVER} redis;
	@echo "${OK}"
.PHONY: get_redis

start_redis:
	@echo "Starting Redis Server ${REDIS_SERVER}"
	docker container start ${REDIS_SERVER};
	@echo "${OK}"

stop_redis:
	@echo "Stopping Redis Server ${REDIS_SERVER}"
	docker container stop ${REDIS_SERVER};
	@echo "${OK}"

run: venv
	@echo "Starting Flask Server"
	export PYTHONPATH=${PYTHONPATH}:${ROOT_DIR}; \
	export REDIS_PORT=${REDIS_PORT}; \
	export REDIS_SERVER=${REDIS_SERVER}; \
	python3 -m pipenv run flask run;
	@echo "${OK}"

clean:
	@echo "Cleaning Up"
	rm -rf ${ROOT_DIR}/d_c/
	docker container stop ${REDIS_SERVER}
	docker container rm ${REDIS_SERVER}
	@echo "${OK}"