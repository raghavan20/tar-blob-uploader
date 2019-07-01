from abc import ABC


class StorageProvider(ABC):

    def upload(self, local_file_path, target_location=None):
        pass