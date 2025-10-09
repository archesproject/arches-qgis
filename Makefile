#/***************************************************************************
# ArchesProject
#
# This plugin links QGIS to an Arches project.
#							 -------------------
#		begin				: 2023-09-15
#		git sha				: $Format:%H$
#		copyright			: (C) 2023 by Knowledge Integration
#		email				: samuel.scandrett@k-int.co.uk
# ***************************************************************************/
#
#/***************************************************************************
# *																		 *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or	 *
# *   (at your option) any later version.								   *
# *																		 *
# ***************************************************************************/

#################################################
# Edit the following to match your sources lists
#################################################


#Add iso code for any locales you want to support here (space separated)
# default is no locales
# LOCALES = af
LOCALES =

# If locales are enabled, set the name of the lrelease binary on your system. If
# you have trouble compiling the translations, you may have to specify the full path to
# lrelease
#LRELEASE = lrelease
#LRELEASE = lrelease-qt4

.PHONY: test

# translation
SOURCES = \
	__init__.py \
	arches_project/arches_project.py arches_project/ui/arches_project_dialog.py

PLUGINNAME = 

PY_FILES = \
	arches_project/__init__.py \
	arches_project/arches_project.py arches_project/ui/arches_project_dialog.py

UI_FILES = arches_project/ui/arches_project_dialog_base.ui

EXTRAS = metadata.txt arches_project/icons/arches.png

EXTRA_DIRS =

COMPILED_RESOURCE_FILES = arches_project/resources.py

PEP8EXCLUDE=pydev,resources.py,conf.py,third_party,ui

transup:
	@echo
	@echo "------------------------------------------------"
	@echo "Updating translation files with any new strings."
	@echo "------------------------------------------------"
	@chmod +x scripts/update-strings.sh
	@scripts/update-strings.sh $(LOCALES)

transcompile:
	@echo
	@echo "----------------------------------------"
	@echo "Compiled translation files to .qm files."
	@echo "----------------------------------------"
	@chmod +x scripts/compile-strings.sh
	@scripts/compile-strings.sh $(LRELEASE) $(LOCALES)

transclean:
	@echo
	@echo "------------------------------------"
	@echo "Removing compiled translation files."
	@echo "------------------------------------"
	rm -f i18n/*.qm


include test/arches/.env

setup-qgis-docker:
	@echo "--------------------------------------"
	@echo "Setting up QGIS testing environment..."
	@echo "--------------------------------------"
	docker run -dt --name qgis-testing-environment -v .:/tests_directory -e QT_QPA_PLATFORM="offscreen" qgis/qgis:3.40.10
	sleep 10 
	docker exec qgis-testing-environment bash -c "cp -a /tests_directory/test/scripts/. /usr/bin/"
	docker exec qgis-testing-environment bash -c "/tests_directory/test/scripts/qgis_setup.sh arches_project"
	docker exec qgis-testing-environment bash -c "rm -f  /root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/arches_project"
	docker exec qgis-testing-environment bash -c "ln -s /tests_directory/ /root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/arches_project"
# 	docker exec qgis-testing-environment bash -c "cd /tests_directory && qgis_testrunner.sh tests.plugin_tests"
	docker exec qgis-testing-environment bash -c "apt-get update && apt-get install -y pre-commit python3-coverage python3-dotenv"
	docker exec qgis-testing-environment bash -c "git config --global --add safe.directory /tests_directory"
	docker network connect arches-qgis-network qgis-testing-environment
	@echo "------------------------------------------"
	@echo "QGIS testing environment setup complete..."
	@echo "------------------------------------------"

shutdown-qgis-docker:
	@echo "-----------------------------------------"
	@echo "Shutting down QGIS testing environment..."
	@echo "-----------------------------------------"
	docker stop qgis-testing-environment
	docker rm qgis-testing-environment

test:
ifeq ($(file),)
	@echo "---------------------------------------"
	@echo "Running all Arches QGIS plugin tests..."
	@echo "---------------------------------------"
	docker exec qgis-testing-environment bash -c "cd /tests_directory \
	&& python3 -m coverage run -m unittest discover arches_project/tests \
	&& python3 -m coverage report -m || true"
else
	@echo "----------------------------------------------"
	@echo "Running Arches QGIS plugin test for $(file)..."
	@echo "----------------------------------------------"
	docker exec qgis-testing-environment bash -c "cd /tests_directory \
	&& python3 -m coverage run -m unittest $(file) \
	&& python3 -m coverage report -m || true"
endif

black:
	@echo "----------------------------------------------"
	@echo "Running Arches QGIS plugin black formatting..."
	@echo "----------------------------------------------"
	docker exec qgis-testing-environment bash -c "cd /tests_directory/arches_project && pre-commit run --all-files --verbose"

setup-arches-docker:
	@echo "----------------------------------------"
	@echo "Setting up Arches testing environment..."
	@echo "----------------------------------------"
	cd ./test/arches && docker compose up -d --build
	@echo "Waiting for Arches to start, this may take a few minutes..."
	@until curl -s http://localhost:$(DJANGO_PORT) > /dev/null; do \
		sleep 20; \
	done
	@echo "Arches setup has completed."

shutdown-arches-docker:
	@echo "-------------------------------------------"
	@echo "Shutting down Arches testing environment..."
	@echo "-------------------------------------------"
	cd ./test/arches && docker compose down -v

# Runs entire testing process
run-testing:
	$(MAKE) setup-arches-docker -s
	@echo "--------------------"
	@echo "Arches is available."
	@echo "--------------------"
	$(MAKE) setup-qgis-docker -s
	@echo "------------------"
	@echo "QGIS is available."
	@echo "------------------"
# 	$(MAKE) test
# 	$(MAKE) black
	$(MAKE) shutdown-qgis-docker
	$(MAKE) shutdown-arches-docker