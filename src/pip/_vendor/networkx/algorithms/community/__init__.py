"""Functions for computing and measuring community structure.

The ``community`` subpackage can be accessed by using :mod:`networkx.community`, then accessing the
functions as attributes of ``community``. For example::

    >>> import networkx as nx
    >>> G = nx.barbell_graph(5, 1)
    >>> communities_generator = nx.community.girvan_newman(G)
    >>> top_level_communities = next(communities_generator)
    >>> next_level_communities = next(communities_generator)
    >>> sorted(map(sorted, next_level_communities))
    [[0, 1, 2, 3, 4], [5], [6, 7, 8, 9, 10]]

"""

from pip._vendor.networkx.algorithms.community.asyn_fluid import *
from pip._vendor.networkx.algorithms.community.centrality import *
from pip._vendor.networkx.algorithms.community.divisive import *
from pip._vendor.networkx.algorithms.community.kclique import *
from pip._vendor.networkx.algorithms.community.kernighan_lin import *
from pip._vendor.networkx.algorithms.community.label_propagation import *
from pip._vendor.networkx.algorithms.community.lukes import *
from pip._vendor.networkx.algorithms.community.modularity_max import *
from pip._vendor.networkx.algorithms.community.quality import *
from pip._vendor.networkx.algorithms.community.community_utils import *
from pip._vendor.networkx.algorithms.community.louvain import *
