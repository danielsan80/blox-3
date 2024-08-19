def dirs():
    return ["north","east","south","west"]

def isValidDir(dir):
    return dir in dirs()

def assertIsValidDir(dir):
    assert isValidDir(dir), f"{dir} must be in {dirs()}"
