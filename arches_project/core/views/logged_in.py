class LoggedIn:
    """ 
    Class for logged in/user profile view
    """
    def __init__(self, dlg, username, url, arches_user_info):
        self.dlg = dlg
        self.username = username
        self.url = url
        self.arches_user_info = arches_user_info

    def update_logged_in_view(self):
        full_name = ""
        if self.arches_user_info["first_name"]:
            full_name = f'{self.arches_user_info["first_name"]} {self.arches_user_info["last_name"]}'

        # if there isn't a first/last name, replace main text with the username & hide sub 
        if not full_name:
            self.dlg.displayUsernameLabel.hide()
            self.dlg.displayUsernameFrame.hide()
            self.dlg.displayFullNameLabel.setText(self.username)
        else:
            self.dlg.displayFullNameLabel.setText(full_name)
            self.dlg.displayUsernameLabel.setText(self.username)

        self.dlg.displayConnectionInfoLabel.setText(f"You are connected to {self.url}.")