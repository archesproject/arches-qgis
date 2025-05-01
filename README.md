# Arches QGIS Plugin

The Arches QGIS plugin allows you to connect to your Arches project and create new resources or edit existing Arches resource geometries using QGIS layers.

The plugin is still in development and thus marked as "experimental". 
Be aware that since the plugin is currently experimental, there may be some unknown issues/bugs and the creators of the plugin can not be held accountable for any problems that may occur.

If you encounter any issues, don't hesitate to create a new GitHub issue or contact the plugin creators.

## Pre-requirements
1. A running Arches instance, accessible via a public domain or IP.
2. An Arches user login with permissions to enter data or create resources.
3. A registered oauth application and client ID entered into settings.py (or settings_local.py) - see the [following documentation link](https://arches.readthedocs.io/en/stable/developing/reference/api/#register-an-oauth-application) for more information on registering oauth2 applications.  
4. If you wish to edit existing Arches resources, a database connection with spatial views added as QGIS layers is required.

## Installation via QGIS repository
Since the plugin is experimental, to install the plugin through the QGIS plugins repository you will need to ensure that experimental plugins are enabled.
1. Navigate to the Plugins tab, then "Manage and Install Plugins".
2. Navigate to "Settings".
3. Tick "Show also Experimental Plugins".
Once enabled, head back to all plugins, search for "Arches Project" and hit "Install Experimental Plugin".

## Installation via GitHub
1. Find your local path for the QGIS installation:
    If on Windows, this should look similar to `C:\Users\USERNAME\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
    If on MacOS, this should look similar to `/Users/USERNAME/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/`
2. Clone this repository under the respective plugins path.
```
git clone https://github.com/archesproject/arches-qgis.git
```
3. Head to the QGIS Plugins tab and select "Manage and Install Plugins".
4. Search for and select "Arches Project" from the list of all plugins.