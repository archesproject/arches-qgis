def enable_logging(self):
    if self.dlg.enableLoggingCheckbox.isChecked():
        self.dlg.tabWidget.setTabVisible(5, True)

    elif not self.dlg.enableLoggingCheckbox.isChecked():
        self.dlg.tabWidget.setTabVisible(5, False)


#TODO needs expanding into class and functionality 