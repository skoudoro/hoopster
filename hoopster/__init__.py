from hoopster.api import hoopsterApi

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__all__ = ['hoopsterApi', __version__]