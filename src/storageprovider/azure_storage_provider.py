from storageprovider.storage_provider import StorageProvider
from azure.storage.blob import BlockBlobService
import os
import logging

logger = logging.getLogger('cloud-backup-utility')


class AzureStorageProvider(StorageProvider):

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.block_blob_service = BlockBlobService(connection_string=connection_string,
                                                   socket_timeout=60)
        self.container_name = 'backup'

    def upload(self, local_file_path, target_location=None):
        logger.info("Uploading file={} to Azure".format(local_file_path))
        file_name = os.path.basename(local_file_path)

        self.block_blob_service.create_blob_from_path(
            container_name=self.container_name,
            blob_name=file_name,
            file_path=local_file_path,
            timeout=60)
