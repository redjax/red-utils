import pkgutil

## Use pkgutil to only load modules
#  if dependencies are met
if pkgutil.find_loader("arrow"):
    from . import arrow_utils

if pkgutil.find_loader("pendulum"):
    from . import pendulum_utils

if pkgutil.find_loader("loguru"):
    from . import loguru_utils
