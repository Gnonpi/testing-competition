from typing import NamedTuple, List


class ContributorResult:
    """
    Summary of contribution of one author
    """
    def __init__(self, name):
        self.name = name
        self.number_of_tests_owned = 0
        self.percentage_of_tests_owned = 0.

        self.number_of_tests_associated = 0
        self.percentage_of_tests_associated = 0.

        self.number_of_lines_written = 0
        self.percentage_of_lines_written = 0.

    def __str__(self):
        res = f"{self.name}:\nTests owned: {self.number_of_tests_owned} - {self.percentage_of_tests_owned:.1f}%\n"
        res += f"Tests associated with: {self.number_of_tests_associated} - {self.percentage_of_tests_associated:.1f}%\n"
        res += f"Written {self.number_of_lines_written} test lines - {self.percentage_of_lines_written:.1f}%"
        return res


class BlameLine(NamedTuple):
    """
    One line output from git blame
    """
    hash_commit: str
    author: str
    timestamp: str
    line_number: int
    content: str


class FunctionTest(NamedTuple):
    """
    The lines making up the test content
    """
    name_test: str
    list_lines: List[BlameLine]
