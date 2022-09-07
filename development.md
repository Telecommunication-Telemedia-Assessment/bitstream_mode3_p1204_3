# Development Guide

* please run the following things before commiting:
    * `./check.sh`
    * `poetry run pytest -vv --capture=sys`
    * `./prettify.sh`

# Docker
* in case the requirements are updated run:
    * `poetry export --without-hashes -f requirements.txt > requirements.txt`
    * the docker container does not use poetry, thus needs the updated requirements.txt