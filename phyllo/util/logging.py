"""Support for nicer logging."""

# Builtins

# Packages

import logging
from logging.config import dictConfig


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'f': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'h': {
            'class': 'logging.StreamHandler',
            'formatter': 'f',
            'level': logging.INFO
        }
    },
    'root': {
        'handlers': ['h'],
        'level': logging.INFO
    }
}


def config_logging(config=LOGGING_CONFIG):
    """Configure logging with a dict."""
    dictConfig(config)


class IndentedLogger(logging.LoggerAdapter):
    """Support for logging with indentation."""

    INDENTATION = '| '
    HALF_INDENTATION = '├-'

    @property
    def indentation(self):
        """Generate the indentation string."""
        base_indentation = ''.join(
            self.INDENTATION for i in range(int(self.extra['indentation']) - 1)
        )
        final_indentation = self.INDENTATION
        if self.extra['indentation'] > int(self.extra['indentation']):
            final_indentation = self.HALF_INDENTATION
        return base_indentation + final_indentation

    def indent(self, message):
        """Indent a logging message."""
        return '{}{}'.format(self.indentation, message)

    def process(self, msg, kwargs):
        """Format the logging message."""
        return (
            self.indent('[{}] {}'.format(self.extra['class'], msg)),
            kwargs
        )
