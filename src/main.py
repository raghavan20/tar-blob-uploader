import yaml
import logging
import sys
import os

logger = logging.getLogger('tar-blob-uploader')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

config = None
with open("../config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as ex:
        logger.exception(ex)

logger.debug(config)

for path_config in config['paths']:
    if 'ignore' in path_config and path_config['ignore']:
        continue
    logger.debug('processing path config: {}'.format(path_config))
    for root, subdirs, files in os.walk(path_config['path']):
        logger.debug('root:' + root)
        # logger.debug('subdirs: {}'.format(subdirs))
        # logger.debug('files: {}'.format(files))

