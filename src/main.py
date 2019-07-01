from config_reader import ConfigReader
from backup import Backup
from storageprovider.azure_storage_provider import AzureStorageProvider

import logging
import sys

# set up logger
verbose_format = logging.Formatter('%(asctime)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s')
logger = logging.getLogger('cloud-backup-utility')
logger.setLevel(logging.DEBUG)
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(verbose_format)
logger.addHandler(stdout_handler)


# backup
config = ConfigReader.get_config("../config.yaml")

storage_provider = AzureStorageProvider(config['azure_sa_connection_string'])

backup = Backup(config, storage_provider=storage_provider)
backup.get_files_to_copy()
backup.copy_files_to_tmp_dir(create_only_dirs=False)
backup.tar_destination_dir()
backup.upload_to_cloud()


