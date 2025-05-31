import logging
from validating.ValidateFiles import Validator

v = Validator()
v.validate_log_file()
path = v.log_path

# Define the logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.FileHandler',
                'filename': str(path),
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
}

# Apply the logging configuration
import logging.config

logging.config.dictConfig(LOGGING_CONFIG)