from abc import ABC, abstractmethod
from typing import Generator, List

from testing_competition.custom_types import BlameLine


class LanguageTestIdentifier(ABC):
    """
    Abstract class so that each language can specify how to recognize its tests
    """

    @abstractmethod
    def file_glob_pattern(self) -> str:
        pass

    @abstractmethod
    def is_a_test_file(self, filename: str) -> bool:
        pass

    @abstractmethod
    def extract_test_functions(self, line_generator: Generator[BlameLine, None, None]) -> List[List[str]]:
        pass


class PythonTestIdentifier(LanguageTestIdentifier):
    """
    Identify Python test "à la" pytest
    """

    def file_glob_pattern(self) -> str:
        return '*.py'

    def is_a_test_file(self, filename):
        if filename.startswith('test_') and filename.endswith('.py'):
            return True
        return False

    def extract_test_functions(self, blame_line_generator: Generator[BlameLine, None, None]) -> List[List[BlameLine]]:
        def get_line_indent(raw_line):
            return len(raw_line) - len(raw_line.lstrip())
        result_tests = []
        current_test_block = []
        current_test_block_indent = None
        has_started_test = False
        for line in blame_line_generator:
            stripped_line = line.content.lstrip()
            if stripped_line.startswith('def test_'):
                has_started_test = True
                current_test_block = [line]
                current_test_block_indent = get_line_indent(line.content)
                continue
            if has_started_test:
                if get_line_indent(line.content) < current_test_block_indent or get_line_indent(line.content) == 0:
                    has_started_test = False
                    result_tests.append(current_test_block)
                    current_test_block = []
                    current_test_block_indent = None
                else:
                    current_test_block.append(line)

        return result_tests

