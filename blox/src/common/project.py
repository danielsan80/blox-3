import os

class Project:

    @staticmethod
    def project_dir() -> str:
        current_dir = os.getcwd()
        while not os.path.exists(os.path.join(current_dir, '.project_root')):
            current_dir = os.path.dirname(current_dir)
            if current_dir == '/':
                raise Exception('Could not find project root')
        return current_dir

    @staticmethod
    def build_dir() -> str:
        return os.path.join(Project.project_dir(), 'build')

    @staticmethod
    def stl_dir() -> str:
        return os.path.join(Project.build_dir(), 'stl')
