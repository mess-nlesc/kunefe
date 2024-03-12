"""Documentation about kunefe."""
import logging
from .kunefe import Kunefe

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = "Faruk D."
__email__ = "f.diblen@esciencecenter.nl"
__version__ = "0.3.0"

__all__ = [
    "Kunefe"
]
