from abc import ABC, abstractmethod


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
    def is_line_test_definition(self, file_line: str) -> bool:
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

    def is_line_test_definition(self, file_line):
        if file_line.startswith('def test_'):
            return True
        return False

