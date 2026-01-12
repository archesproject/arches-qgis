# Arches QGIS Plugin

The Arches QGIS plugin is a plugin for the open-source [QGIS](https://qgis.org/) software, built to integrate with your Arches implementation and streamline the process of using a GIS with Arches data.

The plugin allows users to authenticate using their Arches project URL, username and password, granting the ability to create new resources or edit existing Arches resource geometries using features from the QGIS map interface.

Bug reports and feature proposals are encouraged! File a GitHub ticket [here](https://github.com/archesproject/arches-qgis/issues/new).

##### Table of Contents  
[Installation](#installation)  
[Configuration](#configuration)  
[User Guide](#user-guide)  
[Information for Developer](#information-for-developers)  
[Testing](#testing)

## Installation 

### Pre-requirements
1. A running Arches instance, accessible via a public domain or IP address.
2. A registered oauth application and client ID entered into settings.py (or settings_local.py) - see the [following documentation link](https://arches.readthedocs.io/en/stable/developing/reference/api/#register-an-oauth-application) for more information on registering oauth2 applications.
3. An Arches user login with permissions to enter data or create resources.
4. If you wish to edit existing Arches resources see the section on [Using Arches map layers to edit resources](#using-arches-map-layers-to-edit-resources).

### Installation via the QGIS Plugins Repository
Since the plugin is experimental, to install the plugin through the QGIS plugins repository you will need to ensure that experimental plugins are enabled.

#### Installation from within QGIS
1. Navigate to the Plugins tab, then "Manage and Install Plugins".
2. Navigate to "Settings".
3. Tick "Show also Experimental Plugins".
Once enabled, head back to all plugins, search for "Arches Project" and hit "Install Experimental Plugin".

#### Installation from the QGIS plugins website
All QGIS plugins can be viewed and downloaded from the [QGIS website](https://plugins.qgis.org/plugins/)
1. Search for the "Arches Project" plugin on the website, or go directly here https://plugins.qgis.org/plugins/arches_project/.
2. Download the plugin zip.
3. Extract the folder, and move it to your local QGIS installation path (see below).

### Installation via GitHub
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

## Configuration

### Using Arches map layers to edit resources

In order to edit Arches resources using the Arches QGIS plugin and successfully interact with the Arches API, a layer must contain the following Arches attributes: 
- `resourceinstanceid`
- `nodeid`
- `tileid`. 

Arches resource layers can be set up using PostgreSQL, a web service, or using the core Arches [spatial views](https://arches.readthedocs.io/en/stable/administering/spatial-views/#spatial-views-preview) functionality.

The method of serving the layer is not strict, including methods such as a direct database connection or via a service (e.g. [pg_featureserv](https://github.com/CrunchyData/pg_featureserv)).

**Note**:  the plugin does not act to modify the resource instance loaded in QGIS but rather the source Arches resource using the Arches API, therefore if your Arches QGIS layer is static and does not update when changes are made to the source Arches data then you risk managing outdated geometry data. Live sources such as services or Arches spatial views are recommended to ensure you are always using the latest data, since they update based on changes to Arches.

### Stylesheets

The plugin comes with a custom stylesheet to mimic the user interface design of the Arches software. These stylings can be disabled in the settings tab. Disabling the Arches stylings enables the "default" stylesheet which matches the default QGIS appearance.

## User Guide

### Tabs

![](/media/plugin-tabs.gif)

The Arches QGIS Plugin is composed of 5 tabs:
- Sign In
- Create Resource
- Edit Resource
- Activity Log
- Settings

All tabs, aside from Settings, become enabled upon successful user authentication.

### Authentication

![](/media/plugin-login.gif)

To authenticate with the QGIS plugin, you must supply the URL to your Arches instance (ensuring the language code is included in the URL if your Arches implementation is internationalised), your username and password.

A successful log in will replace the login tab with a User Profile tab. Here you have options to:
- Refresh the fetched Arches resource models and nodes - this is useful if your Arches data models have changed in any way since the last authentication with the Arches QGIS plugin.
- Log out of the plugin, and return to the log in tab.

An unsuccessful log in will return an error message and could be due to a number of factors. Checking the logs in your Arches implementation will provide more information.

### Create a resource

![](/media/plugin-create-resource.gif)

To create an Arches resource with the plugin, select feature(s) from the QGIS map - the text box will inform you of the number of selected features. To advance, select the "Create Resource" button. This will display a confirmation pop-up where you can cancel or confirm to send the data to Arches.

A successful resource creation will display a message with a hyperlink to your new Arches resource. A record of this action will be recorded in the [Activity Log](#activity-log).

An unsuccessful resource creation will result in an error message displayed.

### Edit a resource

![](/media/plugin-edit-resource.gif)

To edit an Arches resource with the plugin, select an Arches resource from the QGIS map and register the resource with the plugin by clicking the "Register resource for editing" button. An Arches resource is successfully identified fields outlined in the [Using Arches map layers to edit resources](#using-arches-map-layers-to-edit-resources) section. 

If the selected feature is not recognised as an Arches resource, a message will be displayed and the resource will not be successfullly registered with the plugin.

Once a resource is successfully registered, the resource instance UUID and a table with all attribute data will be displayed.

The Arches resource can be edited by appending (add) or replacing (replace) the selected geometries to the feature collection of the registered Arches resource tile.

A successful resource edit will display a message with a hyperlink to your Arches resource. A record of this action will be recorded in the [Activity Log](#activity-log).

An unsuccessful resource edit will result in an error message displayed.


### Activity log

![](/media/plugin-activity-log.png)

The Activity Log stores a sortable history of all operations by the Arches QGIS Plugin in the current QGIS session. 

A QGIS session is defined as the instance of the QGIS application running and the period it is open for. It is not specific to the authentication of the plugin, and the Activity Log will persist after plugin log outs. 

The Activity Log will be cleared if the QGIS application is closed and re-opened.

### Settings

![](/media/plugin-settings.png)

The Settings tab currently has one entry, a checkbox option for disabling and enabling the Arches stylings.

Read more about the plugin's stylesheets [here](#stylesheets). 


## Information for developers
If you wish to develop with the QGIS Arches plugin, below are some helpful tips that will make life easier.
- Installation via GitHub is the easiest method to develop.  This can be done by following the [instructions above](#installation-via-github).
- The QGIS plugin "[Plugin Reloader](https://plugins.qgis.org/plugins/plugin_reloader/)" is incredibly useful for reloading plugins to reflect code changes.  This can be found on the QGIS plugins repository, and configured to reload specific plugins using Ctrl+F5.

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
- `make test <file=path/to/file>` - runs all (or a specified) plugin tests in the QGIS environment. Displays coverage at the end.
- `make black` - runs black formatting on all python files in the plugin.
- `make shutdown-qgis-docker` - stops and removes the QGIS docker container.
- `make shutdown-arches-docker <remove_volumes=true|false>` - runs docker compose down for the Arches testing environment and optionally removes volumes.