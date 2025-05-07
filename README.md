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

## Tips for developing
If you wish to develop with the QGIS Arches plugin, below are some helpful tips that will help, and make life easier.
- Installation via GitHub is the easiest method to develop.  This can be done by git cloning in the plugins path (shown above) and (optionally) creating a symbolic link to somewhere much easier to find e.g. your home directory.
- The QGIS plugin "Plugin Reloader" is incredibly useful for reloading plugins to reflect code changes.  This can be found on the QGIS plugins repository, and configured to reload specific plugins with Ctrl+F5.
- If you wish to develop UI elements, you'll need Qt Creator installed: https://doc.qt.io/qtcreator/.
