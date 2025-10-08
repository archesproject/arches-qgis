# Arches QGIS Plugin

The Arches QGIS plugin allows you to connect to your Arches project and create new resources or edit existing Arches resource geometries using QGIS layers.

The plugin is still in development and thus marked as "experimental". 
Be aware that since the plugin is currently experimental, there may be some unknown issues/bugs and the creators of the plugin can not be held accountable for any problems that may occur.

If you encounter any issues, don't hesitate to create a new GitHub issue or contact the plugin creators.

## Pre-requirements
1. A running Arches instance, accessible via a public domain or IP.
2. An Arches user login with permissions to enter data or create resources.
3. A registered oauth application and client ID entered into settings.py (or settings_local.py) - see the [following documentation link](https://arches.readthedocs.io/en/stable/developing/reference/api/#register-an-oauth-application) for more information on registering oauth2 applications.  
4. If you wish to edit existing Arches resources, a database connection with [spatial views](https://arches.readthedocs.io/en/stable/administering/spatial-views/#spatial-views-preview) added as QGIS layers is required.

## Installation via the QGIS Plugins Repository
Since the plugin is experimental, to install the plugin through the QGIS plugins repository you will need to ensure that experimental plugins are enabled.
### Installation from within QGIS
1. Navigate to the Plugins tab, then "Manage and Install Plugins".
2. Navigate to "Settings".
3. Tick "Show also Experimental Plugins".
Once enabled, head back to all plugins, search for "Arches Project" and hit "Install Experimental Plugin".
### Installation from the QGIS plugins website
All QGIS plugins can be viewed and downloaded from the [QGIS website](https://plugins.qgis.org/plugins/)
1. Search for the "Arches Project" plugin on the website, or go directly here https://plugins.qgis.org/plugins/arches_project/.
2. Download the plugin zip.
3. Extract the folder, and move it to your local QGIS installation path (see below).

## Installation via GitHub (for developers)
Note that the entire arches-qgis git repository is not the QGIS plugin, only the `arches_project/` directory should be added to the QGIS plugins path. If the entire directory is added to the QGIS plugin path it will not be recognised and produce errors.
1. Find your local path for the QGIS installation:
    If on Windows, this should look similar to `C:\Users\USERNAME\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`   
    If on MacOS, this should look similar to `/Users/USERNAME/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
2. Clone the arches-qgis repository in your working directory.
    ```
    git clone https://github.com/archesproject/arches-qgis.git
    ```
    
3. Create a symbolic link from `arches-qgis/arches_project` to the QGIS plugins path.   

    On ubuntu this can be done with the following:
    ```
    ln -s arches-qgis/arches_project/ /PATH/TO/QGIS/PLUGINS/arches_project/
    ```
    On windows (or WSL), this must be done using powershell (as administrator) and the arches-qgis repository must be cloned on the mounted c drive rather than the Ubuntu virtual drive, as sym links from WSL to Windows do not work. e.g.
    ```
    cmd /c mklink /d "C:\PATH\TO\QGIS\PLUGINS\arches_project" "C:\arches-qgis\arches_project"
    ``` 
3. Head to the QGIS Plugins tab and select "Manage and Install Plugins".
4. Search for and select "Arches Project" from the list of all plugins.

## Information for developers
If you wish to develop with the QGIS Arches plugin, below are some helpful tips that will help and make life easier.
- Installation via GitHub is the easiest method to develop.  This can be done by git cloning in the plugins path (shown above) and (optionally) creating a symbolic link to somewhere much easier to find e.g. your home directory.
- The QGIS plugin "Plugin Reloader" is incredibly useful for reloading plugins to reflect code changes.  This can be found on the QGIS plugins repository, and configured to reload specific plugins with Ctrl+F5.

### Developing the user interface
QGIS uses PyQt as the framework for UI, specifically Qt 5.15.   
**Note:** Qt 5.15 binaries do not appear to be available for ARM Macs. The following instructions should work for Windows and Linux users.

If you wish to develop UI elements for the arches-qgis plugin you'll need to install [Qt Creator](https://doc.qt.io/qtcreator/), an IDE for Qt applications.   
It's recommended to install Qt and QtCreator using the online installer found here: https://www.qt.io/download-qt-installer-oss. Bundled is a Maintenance Tool that makes updating, and installing/uninstalling additional components very easy.  
Offline, version-specific packages for Qt and QtCreator can be downloaded here: https://www.qt.io/offline-installers.

QtCreator uses Qt6 out the box, so you'll need to use the Qt Mainentance Tool to install the archived version of Qt 5.15.   
- In the top right "Show" dropdown ensure that "Archive" is selected in order to see all historical versions of Qt. 
- Locate and expand Qt 5.15.2, and ensure only the "MinGW 8.1.0" compiler is checked.    

Once installed, add the new version of Qt as a kit in the QtCreator preferences, see the documentation for more information: https://doc.qt.io/qtcreator/creator-targets.html.

Open a new project in QtCreator by selecting the .pro file found in `arches_project/ui/arches_project_ui.pro`, and Qt 5.15.   
This .pro file will load all plugin `.ui` files into the project tree found in the Edit tab (on the left side of QtCreator) where they can be easily opened and switched between. 

## Testing
The Arches QGIS plugin includes tests found in `arches_project/tests/`.    
The root `test/` directory contains scripts for setting up the Arches testing environment.   

### Interacting with the testing suite
Docker needs to be installed, as the testing environment uses docker to build QGIS and Arches containers. See here to install docker: https://docs.docker.com/engine/install/ubuntu/.

Various functions are set up in the [Makefile](/Makefile) which can be used to interact with the testing suite:
- `make run-testing` - this runs the entire testing process and shuts down, removes containers and volumes at the end. This command runs the following functions in the order below.
- `make setup-arches-docker` - this runs the docker-compose file found in `test/arches` and spins up Arches, postgres and elasticsearch containers. In the Arches container, the project is created and run. This does not include webpack as Arches is only being fetched via API, thus in a partially headless state.
- `make setup-qgis-docker` - runs various docker run commands to spin up the QGIS testing container. This is placed on the same network as the Arches container, therefore should be run after.
- `make test` - runs all the plugin tests in the QGIS environment. Displays coverage at the end.
- `make test file=path/to/file` - runs the specified plugin test. Displays coverage at the end.
- `make black` - runs black formatting on all python files in the plugin.
- `make shutdown-arches-docker` - runs docker compose down and removes volumes.
- `make shutdown-qgis-docker` - stops and removes the QGIS docker container.
