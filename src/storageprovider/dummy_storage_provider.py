from storageprovider.storage_provider import StorageProvider
import logging

logger = logging.getLogger('cloud-backup-utility')


class DummyStorageProvider(StorageProvider):

    def upload(self, local_file_path, target_location=None):
        logger.debug('Not uploading')
