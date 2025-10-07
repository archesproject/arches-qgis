#!/bin/bash

# APP and YARN folder locations
# ${WEB_ROOT} and ${ARCHES_ROOT} is defined in the Dockerfile, ${ARCHES_PROJECT} in env_file.env
if [[ -z ${ARCHES_PROJECT} ]]; then
	APP_FOLDER=${ARCHES_ROOT}
	PACKAGE_JSON_FOLDER=${ARCHES_ROOT}
else
	APP_FOLDER=${WEB_ROOT}/${ARCHES_PROJECT}
	PACKAGE_JSON_FOLDER=${ARCHES_ROOT}
fi

# SET DEFAULT WORKING DIRECTORY
if [[ -d ${APP_FOLDER} ]]; then
	cd ${APP_FOLDER}
fi

#Utility functions that check db status
wait_for_db() {
	echo "Testing if database server is up..."
	while [[ ! ${return_code} == 0 ]]
	do
        psql --host=${PGHOST} --port=${PGPORT_CONTAINER} --user=${PGUSERNAME} --dbname=postgres -c "select 1" >&/dev/null
		return_code=$?
		sleep 3
	done
	echo "Database server is up"

    echo "Testing if Elasticsearch is up..."
    while [[ ! ${return_code} == 0 ]]
    do
        curl -s "http://${ESHOST}:${ESPORT_HOST}/_cluster/health?wait_for_status=green&timeout=60s" >&/dev/null
        return_code=$?
        sleep 3
    done
	sleep 5 # add extra sleep just to ensure ES is up
    echo "Elasticsearch is up"
}

db_exists() {
	echo "Checking if database "${ARCHES_PROJECT}" exists..."
	count=`psql --host=${PGHOST} --port=${PGPORT_CONTAINER} --user=${PGUSERNAME} --dbname=postgres -Atc "SELECT COUNT(*) FROM pg_catalog.pg_database WHERE datname='${ARCHES_PROJECT}'"`

	# Check if returned value is a number and not some error message
	re='^[0-9]+$'
	if ! [[ ${count} =~ $re ]] ; then
	   echo "Error: Something went wrong when checking if database "${ARCHES_PROJECT}" exists..." >&2;
	   echo "Exiting..."
	   exit 1
	fi

	# Return 0 (= true) if database exists
	if [[ ${count} > 0 ]]; then
		echo "Checking if database is setup "${ARCHES_PROJECT}"..."
		tcount=`psql --host=${PGHOST} --port=${PGPORT_CONTAINER} --user=${PGUSERNAME} --dbname=${ARCHES_PROJECT} -Atc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'nodes'"`
		# Check if returned value is a number and not some error message
		re='^[0-9]+$'
		if ! [[ ${tcount} =~ $re ]] ; then
		echo "Error: Something went wrong when checking if tables exists in database "${ARCHES_PROJECT}"..." >&2;
		echo "Exiting..."
		exit 1
		fi

		# Return 0 (= true) if table exists
		if [[ ${tcount} > 0 ]]; then
			return 0
		else
			return 1
		fi
	else
		return 1
	fi
}


#### Install
init_arches() {
	echo "Checking if Arches project "${ARCHES_PROJECT}" exists..."
	if [[ ! -d ${APP_FOLDER}/${ARCHES_PROJECT} ]] || [[ ! "$(ls ${APP_FOLDER}/${ARCHES_PROJECT})" ]]; then
		echo ""
		echo "----- Custom Arches project '${ARCHES_PROJECT}' does not exist. -----"
		echo ""
		create_arches_project
	else
		echo "Custom Arches project '${ARCHES_PROJECT}' exists."
	fi

	wait_for_db
	if db_exists; then
		echo "Database ${ARCHES_PROJECT} already exists."
		echo "Skipping Package Loading"
	else
		echo "Database ${ARCHES_PROJECT} does not exists yet."
		run_setup_db
	fi
}

create_arches_project() {
	echo "Checking if Arches project "${ARCHES_PROJECT}" exists..."
	if [[ ! -d ${APP_FOLDER}/${ARCHES_PROJECT} ]] || [[ ! "$(ls ${APP_FOLDER}/${ARCHES_PROJECT})" ]]; then
		echo ""
		echo "----- Creating '${ARCHES_PROJECT}'... -----"
		echo ""

		cd ${WEB_ROOT}
		arches-admin startproject ${ARCHES_PROJECT}
		APP_FOLDER=${WEB_ROOT}/${ARCHES_PROJECT}

		copy_project_files
		run_setup_db

		exit_code=$?
		if [[ ${exit_code} != 0 ]]; then
			echo "Something went wrong when creating your Arches project: ${ARCHES_PROJECT}."
			echo "Exiting..."
			exit ${exit_code}
		fi
	else
		echo "Arches project '${ARCHES_PROJECT}' exists."
	fi
}

#### Misc
copy_project_files() {
	echo "Copying files to project..."
	yes | cp ${WEB_ROOT}/settings_local.py ${APP_FOLDER}/${ARCHES_PROJECT}/settings_local.py
	yes | cp ${WEB_ROOT}/project_setup.py ${APP_FOLDER}/${ARCHES_PROJECT}/management/commands/project_setup.py
}

#### Run commands
run_migrations() {
	echo ""
	echo "----- RUNNING DATABASE MIGRATIONS -----"
	echo ""
	cd ${APP_FOLDER}
	python3 manage.py migrate
}

run_setup_db() {
	echo ""
	echo "----- RUNNING SETUP_DB -----"
	echo ""

    cd ${WEB_ROOT}/${ARCHES_PROJECT}
	python3 manage.py setup_db --force
}

run_django_server() {
	echo ""
	echo "----- *** RUNNING DJANGO DEVELOPMENT SERVER *** -----"
	echo ""
	cd ${APP_FOLDER}
    echo "Running Django"
	exec sh -c "pip install debugpy -t /tmp && python3 /tmp/debugpy --listen 0.0.0.0:5678 manage.py runserver 0.0.0.0:${DJANGO_PORT}"
}

run_project_commands() {
	echo ""
	echo "----- *** RUNNING MANAGEMENT COMMANDS TO SET UP PROJECT *** -----"
	echo ""
	cd ${APP_FOLDER}
	python3 manage.py project_setup
}

#### Main commands
run_arches() {
	init_arches
	run_project_commands
	run_django_server
}


### Starting point ###


# Use -gt 1 to consume two arguments per pass in the loop
# (e.g. each argument has a corresponding value to go with it).
# Use -gt 0 to consume one or more arguments per pass in the loop
# (e.g. some arguments don't have a corresponding value to go with it, such as --help ).

# If no arguments are supplied, assume the server needs to be run
if [[ $#  -eq 0 ]]; then
	echo "No arguments supplied, running Arches server..."
	wait_for_db
	run_arches
fi

# Else, process arguments
echo "Full command: $@"
while [[ $# -gt 0 ]]
do
	key="$1"
	echo "Command: ${key}"

	case ${key} in
		run_arches)
			wait_for_db
			run_arches
		;;
		run_migrations)
			wait_for_db
			run_migrations
		;;
		*)
            cd ${APP_FOLDER}
			"$@"
			exit 0
		;;
	esac
	shift # next argument or value
done