def success(iface_object, msg, duration=5):
    # Level 3 - Success message
    iface_object.messageBar().pushMessage("Success", f"{msg}", level=3, duration=duration) 

def error(iface_object, msg, duration=5):
    # Level 2 - Critical error 
    iface_object.messageBar().pushMessage("Error", f"{msg}", level=2, duration=duration) 

def warning(iface_object, msg, duration=5):
    # Level 1 - Warning error
    iface_object.messageBar().pushMessage("Warning", f"{msg}", level=1, duration=duration) 

def information(iface_object, msg, duration=5):
    # Level 0 - Information message
    iface_object.messageBar().pushMessage("Information", f"{msg}", level=0, duration=duration) 

