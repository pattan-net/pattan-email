import os
from pathlib import Path

#: Name of the application
APP_NAME = "pattanemail"

#: Prefix used for environment variables
ENV_PREFIX = "PATTAN_EMAIL_"

CONFIG_FILE_NAME = ".pattan-email.json"

CONFIG_FILE_HOME_DIR = Path(os.path.expanduser("~")) / CONFIG_FILE_NAME

#: Config files to be loaded. Order will be respected, which means that
#: the config file on the bottom will override locations on the top.
CONFIG_FILES = (
    CONFIG_FILE_HOME_DIR,
)
