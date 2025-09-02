def format_url(url_input):
    """
    Simple function to fix any possible user input errors.
    Strips any leading/trailing whitespace and a trailing slash.
    """

    formatted_url = url_input.strip()
    if formatted_url[-1] == "/":
        formatted_url = formatted_url[:-1]

    return formatted_url
