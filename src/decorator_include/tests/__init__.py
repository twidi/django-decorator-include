from django import VERSION

if VERSION < (1, 6):
    # Before django 1.6, Django was not able to find tests in tests/tests.py
    from .tests import *
