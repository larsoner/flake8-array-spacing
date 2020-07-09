import re
import tokenize

from pycodestyle import (extraneous_whitespace, whitespace_around_operator,
                         whitespace_around_comma)
from flake8.defaults import NOQA_INLINE_REGEXP

__version__ = '0.1.dev0'

# This could almost certainly be better, it just checks for [...]
# (no pairing within, or checking that i/j are attached to a number, etc.)
ARRAY_LIKE_REGEX = re.compile(
    r'[\[(][0-9 ij,+\-*^\/&|\[\]]*[\]),;]'
)
FUNC_KINDS = (
    (extraneous_whitespace, ('E201', 'E202')),
    (whitespace_around_operator, ('E221', 'E222')),
    (whitespace_around_comma, ('E241',)),
)


class ArraySpacing(object):
    """Checker for E2XX variants, ignoring array-like."""

    name = 'array-spacing'
    version = __version__

    def __init__(self, logical_line, tokens):
        self.logical_line = logical_line
        self.tokens = tokens
        self._array_ranges = None  # only compute if necessary

    def in_array_like(self, idx):
        """Determine if in array like range."""
        if self._array_ranges is None:
            self._array_ranges = [
                (match.start() + 1, match.end() + 1)
                for match in ARRAY_LIKE_REGEX.finditer(self.logical_line)]
        return any(start <= idx <= end for start, end in self._array_ranges)

    def ignoring(self, kind):
        """Determine if a kind is being ignored."""
        for token in self.tokens:
            if token.type == tokenize.COMMENT:
                codes = NOQA_INLINE_REGEXP.match(token.string).group('codes')
                if codes is not None and kind in codes:
                    return True
        return False

    def __iter__(self):
        """Iterate over errors."""
        for func, kinds in FUNC_KINDS:
            for found, msg in func(self.logical_line):
                found_kind = msg[:4]
                if found_kind in kinds and \
                        (not self.in_array_like(found)) and \
                        (not self.ignoring(found_kind)):
                    yield found, 'A' + msg[1:]
