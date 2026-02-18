from arches_project.core.views.stylesheets.arches import ArchesStylesheet
from arches_project.core.views.stylesheets.default import DefaultStylesheet


class Stylesheets:
    def __init__(self, dlg, dlg_resource_confirmation, plugin_dir):
        self.dlg = dlg
        self.dlg_resource_confirmation = dlg_resource_confirmation
        self.plugin_dir = plugin_dir

        self.default_stylesheet = DefaultStylesheet(
            dlg=self.dlg,
            dlg_resource_confirmation=self.dlg_resource_confirmation,
        )

        self.arches_stylesheet = ArchesStylesheet(
            dlg=self.dlg,
            dlg_resource_confirmation=self.dlg_resource_confirmation,
            plugin_dir=self.plugin_dir,
        )

        # Set as default
        self.arches_stylesheet.arches_stylesheet()

    def stylesheet_changed(self):
        if not self.dlg.useStylesheetCheckbox.isChecked():
            self.default_stylesheet.default_stylesheet()
        elif self.dlg.useStylesheetCheckbox.isChecked():
            self.arches_stylesheet.arches_stylesheet()
