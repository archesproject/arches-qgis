class UpdateLogin:
    def __init__(self, dlg_label):
        self.updateTextLabel = dlg_label

    def update_login_progress(self, text):
        """
        Simple function just used as a signal connection to update the loading ui with helpful info, 
        as a spinning wheel look like no progress is being made. 
        """
        self.updateTextLabel.setText(text)
