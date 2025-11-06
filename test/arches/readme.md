# Arches testing docker containers

Use `docker-compose up -d` or the makefile function `make setup-arches-docker` to create the Arches testing environment. 

The following containers are created:
- arches-qgis-arches - a barebones, headless, containerised Arches instance for testing with the QGIS plugin.
- arches-qgis-postgres - a PostgreSQL container for the Arches project database.
- arches-qgis-elasticsearch - an Elaticsearch container for the Arches project index.

The provided .env contains all relevant information and does not need to be changed, but it has been set up in a way that values can be changed if necessary.

The Arches dockerfile runs the `entrypoint.sh` found in this directory and creates an Arches project and copies the `settings_local.py` and `project_setup.py` files. The `project_setup.py` file creates an Oauth2 application which is supplied to `settings_local.py` and used in the plugin tests.

It will have pre-built resource models for testing.

Containers can be stopped using `docker compose down` or the makefile function `make shutdown-arches-docker` which includes the `-v` flag to remove volumes from the host machine.