"""
NetworkX
========

NetworkX is a Python package for the creation, manipulation, and study of the
structure, dynamics, and functions of complex networks.

See https://networkx.org for complete documentation.
"""

__version__ = "3.4.2"


# These are imported in order as listed
from pip._vendor.networkx.lazy_imports import _lazy_import

from pip._vendor.networkx.exception import *

from pip._vendor.networkx import utils
from pip._vendor.networkx.utils import _clear_cache, _dispatchable

# load_and_call entry_points, set configs
config = utils.backends._set_configs_from_environment()
utils.config = utils.configs.config = config  # type: ignore[attr-defined]

from pip._vendor.networkx import classes
from pip._vendor.networkx.classes import filters
from pip._vendor.networkx.classes import *

from pip._vendor.networkx import convert
from pip._vendor.networkx.convert import *

from pip._vendor.networkx import convert_matrix
from pip._vendor.networkx.convert_matrix import *

from pip._vendor.networkx import relabel
from pip._vendor.networkx.relabel import *

from pip._vendor.networkx import generators
from pip._vendor.networkx.generators import *

from pip._vendor.networkx import readwrite
from pip._vendor.networkx.readwrite import *

# Need to test with SciPy, when available
from pip._vendor.networkx import algorithms
from pip._vendor.networkx.algorithms import *

from pip._vendor.networkx import linalg
from pip._vendor.networkx.linalg import *

from pip._vendor.networkx import drawing
from pip._vendor.networkx.drawing import *
