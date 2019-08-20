from pathlib import Path

import pytest

from testing_competition.language_identifier import PythonTestIdentifier


class TestIsATestFile:
    def test_not_exist_file(self):
        p = PythonTestIdentifier()
        not_exist_path = Path(__file__).parent.joinpath('this-wont-ever-exist.py')
        with pytest.raises(FileNotFoundError):
            p.is_a_test_file(not_exist_path)

    def test_not_a_test_file(self):
        p = PythonTestIdentifier()
        not_a_test_file = Path(__file__).parent.joinpath('not_a_test_file.py')
        assert not p.is_a_test_file(not_a_test_file)

    def test_is_a_test_file(self):
        p = PythonTestIdentifier()
        not_a_test_file = Path(__file__).parent.joinpath('test_a_file.py')
        assert p.is_a_test_file(not_a_test_file)
