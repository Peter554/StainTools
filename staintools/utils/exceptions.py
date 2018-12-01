"""
Exceptions
"""


class TissueMaskException(Exception):
    def __init__(self, *args, **kwargs):
        super(TissueMaskException, self).__init__(*args, **kwargs)
