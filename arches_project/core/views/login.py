from arches_project.core.arches.api import arches_api


class LoggedIn:
    """
    Class for logged in/user profile view
    """

    def __init__(self, dlg, username, url, arches_user_info):
        self.dlg = dlg
        self.username = username
        self.url = url

    def update_logged_in_view(self):
        full_name = ""
        if arches_api.arches_user_info["first_name"]:
            full_name = f'{arches_api.arches_user_info["first_name"]} {arches_api.arches_user_info["last_name"]}'

        # if there isn't a first/last name, replace main text with the username & hide sub
        if not full_name:
            self.dlg.displayUsernameLabel.hide()
            self.dlg.displayUsernameFrame.hide()
            self.dlg.displayFullNameLabel.setText(self.username)
        else:
            self.dlg.displayFullNameLabel.setText(full_name)
            self.dlg.displayUsernameLabel.setText(self.username)

        self.dlg.displayConnectionInfoLabel.setText(f"You are connected to {self.url}.")


class UpdateLoginProgress:
    def __init__(self, dlg_label, step=0):
        self.updateTextLabel = dlg_label
        self.total_number_steps = 4
        self.percentage_chunks = (1 / self.total_number_steps) * 100
        self.percent_progress = 0
        self.step = step

    def update_login_progress(self, text):
        """
        Simple function just used as a signal connection to update the loading ui with helpful info,
        as a spinning wheel look like no progress is being made.
        """
        self.updateTextLabel.setText(text)

    def update_percent(self, main, inner_iter=None, inner_total=None):
        """
        Must hard-code x number of steps in order to get percentage completion.
        1. clientid 25
        2. permissions 50
        3. graphs 75
        4. token 100
        """
        if main:
            self.step += 1
            self.percent_progress = (self.step / self.total_number_steps) * 100
            self.updateTextLabel.setText(f"{round(self.percent_progress)}%")

        if inner_iter and inner_total:
            sub_percent_progress = (
                self.percent_progress
                + (self.percentage_chunks / inner_total) * inner_iter
            )
            self.updateTextLabel.setText(f"{round(sub_percent_progress)}%")
