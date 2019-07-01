import yaml
import logging

logger = logging.getLogger('cloud-backup-utility')


class ConfigReader:

    @staticmethod
    def get_config(file_path):
        with open(file_path, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as ex:
                logger.exception(ex)

        return config
