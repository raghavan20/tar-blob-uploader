from unittest import TestCase
from backup import Backup


class TestBackup(TestCase):

    def test_finds_correct_location_to_store_backup_file(self):
        tmp_path = '/tmp'

        actual = Backup.find_path_to_backup_file('/Users/rob/test/googledrive/sports',
                                                 '/Users/rob/test/googledrive/sports/notes.md', tmp_path)
        self.assertEquals(('/tmp/sports', '/tmp/sports/notes.md'), actual)

        actual = Backup.find_path_to_backup_file('/Users/rob/test/googledrive/technical',
                                                 '/Users/rob/test/googledrive/technical/java/notes.md', tmp_path)
        self.assertEquals(('/tmp/technical/java', '/tmp/technical/java/notes.md'), actual)

    def test_backup(self):
        from config_reader import ConfigReader
        from backup import Backup
        from storageprovider.dummy_storage_provider import DummyStorageProvider

        import logging
        import sys
        from shutil import rmtree

        # set up logger
        logger = logging.getLogger('tar-blob-uploader')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler(sys.stdout))

        # clean up tmp dir
        rmtree('../tmp', ignore_errors=True)

        # config
        config = ConfigReader.get_config("files/test_config.yaml")

        # storage provider
        storage_provider = DummyStorageProvider()

        # backup as tar
        backup = Backup(config, storage_provider=storage_provider)
        backup.get_files_to_copy()
        backup.copy_files_to_tmp_dir(create_only_dirs=False)
        backup.tar_destination_dir()

        # assert tar exists with expected files and folders
        import tarfile
        tar = tarfile.open(config['tmp_tar_file_path'])
        found = [m.name for m in tar.getmembers()]
        self.assertTrue('tmp/technical/security/security.md' in found)
        self.assertTrue('tmp/technical/cloud/cloud.md' in found)
        self.assertFalse('tmp/technical/security/a.png' in found)

