import copy
from abc import ABC, abstractmethod
from typing import Generator, List, Iterable

from testing_competition.custom_types import BlameLine, FunctionTest


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
    def extract_test_functions(self, line_generator: Iterable[BlameLine]) -> List[FunctionTest]:
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

    def extract_test_functions(self, blame_line_generator: Iterable[BlameLine]) -> List[FunctionTest]:
        def get_line_indent(raw_line):
            return len(raw_line) - len(raw_line.lstrip())

        result_tests = []
        current_test_name = None
        current_test_block = []
        current_test_block_indent = 0
        has_started_test = False

        for line in blame_line_generator:
            stripped_line = line.content.lstrip()

            # closing test function
            if has_started_test and get_line_indent(line.content) <= current_test_block_indent and stripped_line != '':
                has_started_test = False
                reverse_last_lines = copy.deepcopy(current_test_block)
                reverse_last_lines.reverse()
                for r in reverse_last_lines:
                    if r.content.strip() == '':
                        current_test_block.pop(-1)
                    else:
                        break
                result_tests.append(FunctionTest(
                    name_test=current_test_name,
                    list_lines=current_test_block)
                )
                current_test_block = []
                current_test_block_indent = None

            # opening new test function
            if stripped_line.startswith('def test_'):
                current_test_name = stripped_line.replace('def ', '')
                current_test_name = current_test_name[:current_test_name.index('(')]
                has_started_test = True
                current_test_block = [line]
                current_test_block_indent = get_line_indent(line.content)
                continue

            # adding line to current test function
            if has_started_test:
                current_test_block.append(line)

        # add remaining lines
        if has_started_test:
            reverse_last_lines = copy.deepcopy(current_test_block)
            reverse_last_lines.reverse()
            for r in reverse_last_lines:
                if r.content.strip() == '':
                    current_test_block.pop(-1)
                else:
                    break
            result_tests.append(FunctionTest(
                name_test=current_test_name,
                list_lines=current_test_block)
            )
        return result_tests
