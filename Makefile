# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* test_TA_Weather/*.py

black:
	@black scripts/* test_TA_Weather/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr test_TA_Weather-*.dist-info
	@rm -fr test_TA_Weather.egg-info

install:
	@pip install . -U

all: clean install test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
PYPI_USERNAME=<AUTHOR>
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u $(PYPI_USERNAME)

pypi:
	@twine upload dist/* -u $(PYPI_USERNAME)


# ----------------------------------
#      API
# ----------------------------------
run_api:
	uvicorn test_TA_Weather.api.api:app --reload


# ----------------------------------
#      API
# ----------------------------------
GCP_PROJECT_ID=profound-hydra-337814
DOCKER_IMAGE_NAME=testta
GCR_MULTI_REGION=eu.gcr.io
GCR_REGION=europe-west3

# ----------------------------------
#      DOCKER
# ----------------------------------

docker_params:
	@echo "project id: ${GCP_PROJECT_ID}"
	@echo "image name: ${DOCKER_IMAGE_NAME}"
	@echo "multi region: ${GCR_MULTI_REGION}"
	@echo "region: ${GCR_REGION}"

docker_build:
	python setup.py sdist
	docker build -t ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME} .

docker_run:
	docker run -e PORT=8000 -p 8000:8000 ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME}

docker_push:
	docker push ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME}

docker_deploy:
	gcloud run deploy --image ${GCR_MULTI_REGION}/${GCP_PROJECT_ID}/${DOCKER_IMAGE_NAME} --platform managed --region ${GCR_REGION}
