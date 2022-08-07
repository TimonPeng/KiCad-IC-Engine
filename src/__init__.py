import sys

if not sys.version_info >= (3, 7) or not sys.version_info < (4, 0):
    raise EnvironmentError("Python >=3.7 or <4.0 is required.")
