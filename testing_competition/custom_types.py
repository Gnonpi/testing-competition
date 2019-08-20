from typing import NamedTuple


class ContributorResult(NamedTuple):
    """
    Summary of contribution of one author
    """
    name: str
    number_of_tests: int
    percentage_of_tests: float


class BlameLine(NamedTuple):
    hash: str
    author: str
    timestamp: str
    line_number: int
    content: str
