def format_url(url_input):
    # formatted_url = self.dlg.arches_server_input.text().strip()
    formatted_url = url_input.strip()
    if formatted_url[-1] == "/":
        formatted_url = formatted_url[:-1]
    return formatted_url
