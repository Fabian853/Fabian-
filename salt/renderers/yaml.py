from __future__ import absolute_import

# Import Python Modules
import logging
import warnings

# Import Salt libs
from salt.utils.yaml import CustomLoader, load


log = logging.getLogger(__name__)


HAS_ORDERED_DICT = True

# code fragment taken from https://gist.github.com/844388
try:
    # included in standard lib from Python 2.7
    from collections import OrderedDict
except ImportError:
    # try importing the backported drop-in replacement
    # it's available on PyPI
    try:
        from ordereddict import OrderedDict
    except ImportError:
        HAS_ORDERED_DICT = False



def get_yaml_loader(argline):
    # since -o is currently the only option, we parse argline the simple way.
    if argline == '-o':
        if HAS_ORDERED_DICT:
            def Loader(*args):
                return CustomLoader(*args, dictclass=OrderedDict)
            return Loader
        else:
            log.warn("OrderedDict not available! "
                     "NOT enabling implicit state ordering for YAML!")
    return CustomLoader


def render(yaml_data, env='', sls='', argline='', **kws):
    if not isinstance(yaml_data, basestring):
        yaml_data = yaml_data.read()
    with warnings.catch_warnings(record=True) as warn_list:
        data = load(yaml_data, Loader=get_yaml_loader(argline))
        if len(warn_list) > 0:
            for item in warn_list:
                log.warn(
                    "{warn} found in salt://{sls} environment={env}".format(
                    warn=item.message, sls=sls, env=env))
        return data if data else {}
