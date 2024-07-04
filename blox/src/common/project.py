import os

class Project:

    def project_dir():
        current_dir = os.getcwd()
        while not os.path.exists(os.path.join(current_dir, '.project_root')):
            current_dir = os.path.dirname(current_dir)
            if current_dir == '/':
                return None
        return current_dir

    def build_dir():
        if Project.project_dir() is None:
            return None
        else:
            return os.path.join(Project.project_dir(), 'build')

    def stl_dir():
        if Project.build_dir() is None:
            return None
        else:
            return os.path.join(Project.build_dir(), 'stl')
