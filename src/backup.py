import logging
import os
import pathlib
from shutil import copyfile
from storageprovider.storage_provider import StorageProvider
import tarfile

logger = logging.getLogger('cloud-backup-utility')


class Backup:

    def __init__(self, config, storage_provider:StorageProvider):
        self.config = config
        self.files_to_copy = {}
        self.storage_provider = storage_provider
        self.tmp_tar_file_path = self.config['tmp_tar_file_path']

        # tmp dir
        self.tmp_dir = self.config['tmp_dir']
        if not os.path.exists(self.tmp_dir):
            logger.info('Creating tmp dir={}'.format(self.tmp_dir))
            pathlib.Path(self.tmp_dir).mkdir(parents=True, exist_ok=True)
        else:
            if len(os.listdir(self.tmp_dir)) > 0:
                raise Exception('tmp_dir should be empty')
        logger.info('Using tmp dir={}'.format(self.tmp_dir))

    def get_files_to_copy(self):
        for path_config in self.config['paths']:

            # ignore processing paths that are marked to be ignored
            if 'ignore' in path_config and path_config['ignore']:
                continue

            # create top dirs
            top_dir_path = path_config['path']
            self.files_to_copy[top_dir_path] = []

            # filter out files that need to be copied
            for root, subdirs, files in os.walk(path_config['path']):
                # logger.debug('root:' + root)
                for file in files:
                    file_full_path = os.path.join(root, file)
                    if not Backup.is_file_extension_allowed(file_full_path, path_config):
                        continue

                    if not Backup.is_subdir_allowed(file_full_path, path_config):
                        continue

                    self.files_to_copy[top_dir_path].append(file_full_path)

    def copy_files_to_tmp_dir(self, create_only_dirs=False):
        for top_dir_path, files in self.files_to_copy.items():

            for file_to_copy_path in files:
                dest_dir_path, dest_file_path = Backup.find_path_to_backup_file(top_dir_path, file_to_copy_path, self.tmp_dir)

                pathlib.Path(dest_dir_path).mkdir(parents=True, exist_ok=True)
                if not create_only_dirs:
                    copyfile(file_to_copy_path, dest_file_path)

    def tar_destination_dir(self):
        logger.info('Tar\'ing the tmp dir contents to file={}'.format(self.tmp_tar_file_path))
        with tarfile.open(self.tmp_tar_file_path, 'w:gz') as tar:
            tar.add(self.tmp_dir, arcname=os.path.basename(self.tmp_dir))

    def upload_to_cloud(self):
        self.storage_provider.upload(self.tmp_tar_file_path)

    @staticmethod
    def is_file_extension_allowed(file_full_path, path_config):
        filename, file_extension = os.path.splitext(file_full_path)
        # print(file_extension)
        if file_extension in path_config['include_extensions']:
            return True
        return False

    @staticmethod
    def find_path_to_backup_file(backup_dir_path, backup_file_path, tmp_dir_path):
        # print('finding for {}, {}, {}'.format(backup_dir_path, backup_file_path, tmp_dir_path))
        t1, last_sub_dir = os.path.split(backup_dir_path)
        non_base_sub_path = os.path.relpath(backup_file_path, backup_dir_path)
        t2 = os.path.join(tmp_dir_path, last_sub_dir)
        destination_file_path = os.path.join(t2, non_base_sub_path)

        return os.path.dirname(destination_file_path), destination_file_path

    @staticmethod
    def is_subdir_allowed(file_full_path, path_config):
        return True


