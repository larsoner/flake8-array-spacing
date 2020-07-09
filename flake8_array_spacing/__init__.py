import re
from pycodestyle import (
    extraneous_whitespace,  # 201, 202
    whitespace_around_operator,  # 221, 222
    whitespace_around_comma,  # 241
)

__version__ = '0.1.dev0'

# This could almost certainly be better, it just checks for [...]
# (no pairing within, or checking that i/j are attached to a number, etc.)
ARRAY_LIKE_REGEX = re.compile(
    r'[\[(][0-9 ij,+\-*^\/&|\[\]]*[\]),;]'
)


class ArraySpacing(object):
    name = 'array-spacing'
    version = __version__

    def __init__(self, logical_line):
        self.logical_line = logical_line
        self._array_ranges = None  # only compute if necessary

    def in_array_like(self, idx):
        if self._array_ranges is None:
            self._array_ranges = [
                (match.start() + 1, match.end() + 1)
                for match in ARRAY_LIKE_REGEX.finditer(self.logical_line)]
        return any(start <= idx <= end for start, end in self._array_ranges)

    def __iter__(self):
        for found, msg in extraneous_whitespace(self.logical_line):
            if msg[:4] in ('E201', 'E202') and not self.in_array_like(found):
                yield found, 'A' + msg[1:]
        for found, msg in whitespace_around_operator(self.logical_line):
            if msg[:4] in ('E221', 'E222') and not self.in_array_like(found):
                yield found, 'A' + msg[1:]
        for found, msg in whitespace_around_comma(self.logical_line):
            if msg[:4] == 'E241' and not self.in_array_like(found):
                yield found, 'A' + msg[1:]
