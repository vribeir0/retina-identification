import os


class FolderUtils:
    @staticmethod
    def create_if_not_exists(path):
        if not os.path.exists(path):
            os.makedirs(path)
