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


class UpdateLogin:
    def __init__(self, dlg_label, step=0, substep=0):
        self.updateTextLabel = dlg_label
        self.step = step
        self.substep = substep

    def update_login_progress(self, text):
        """
        Simple function just used as a signal connection to update the loading ui with helpful info, 
        as a spinning wheel look like no progress is being made. 

        Must hard-code x number of steps in order to get percentage completion.
        1. clientid
        2. permissions
        3. graphs
        4. token
        """
        self.updateTextLabel.setText(text)
        self.step+=1
        print(self.step)


class LoginProgress:
    """
    Percentage progress for login - dynamic based on x no. graphs
    """
