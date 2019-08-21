from pathlib import Path

from testing_competition.language_identifier import PythonTestIdentifier


class TestIsATestFile:
    def test_not_exist_file(self):
        p = PythonTestIdentifier()
        not_exist_path = 'this-wont-ever-exist.py'
        assert not p.is_a_test_file(str(not_exist_path))

    def test_not_a_test_file(self):
        p = PythonTestIdentifier()
        not_a_test_file = 'not_a_test_file.py'
        assert not p.is_a_test_file(str(not_a_test_file))

    def test_is_a_test_file(self):
        p = PythonTestIdentifier()
        not_a_test_file = 'test_a_file.py'
        assert p.is_a_test_file(str(not_a_test_file))
