# Cloud Backup Utility

A stand-alone Python app that can tar selective folders and files and can backup to a storage location. The backup storage location is provided by a Storage Provider. The current supported Storage Provider is Azure. 

**Filtering support**

-   by file extension
-   by sub folders; yet to be implemented


## Development Environment

Prerequisite:

-   *nix environment (mainly for running tests; have not tested other than OS X)
-   Python 3.6
-   virtualenvwrapper or equivalent


Create virtual environment

      mkvirtualenv -p `which python3.6` cloud-backup-utility
      pip install -r requirements.txt


## Configuration

The application is configured with `config.yaml`. It is expected to be in application's current working directory. Look at sample `config.yaml.template`


## How to execute

Run main.py which tars and uploads to Azure. It is expected to pass valid Azure Storage account connection string in Yaml key `azure_sa_connection_string`.

Look at [test](test/test_backup.py) for sample usage.


## Features / tasks planned


-   [x] include only marked extensions
-   [ ] filter out excluded dirs
-   [x] tar the target folder
-   [x] use Azure blob storage to store
-   [x] delete tmp dir only if it is non empty
-   [x] integration test
-   [ ] versioned blob files / blob rotation