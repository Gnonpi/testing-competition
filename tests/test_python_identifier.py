from pathlib import Path

from testing_competition.custom_types import BlameLine, FunctionTest
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


class TestExtractFunction:
    fake_hash = ''
    fake_author = 'test_author'
    fake_timestamp = ''
    fake_line_number = 1

    @staticmethod
    def _create_list_of_blames(t_content: str):
        list_blames = []
        for line in t_content.splitlines():
            list_blames.append(BlameLine(
                hash_commit=TestExtractFunction.fake_hash,
                author=TestExtractFunction.fake_author,
                timestamp=TestExtractFunction.fake_timestamp,
                line_number=TestExtractFunction.fake_line_number,
                content=line
            ))
        return list_blames

    def test_contain_no_test(self):
        t_content = """
import pytest

def one_function(a):
    return a + 1 
"""
        p = PythonTestIdentifier()
        blames = TestExtractFunction._create_list_of_blames(t_content)
        res = p.extract_test_functions(blames)
        assert res == list()

    def test_contain_one_test(self):
        t_content = """
import os
import pytest

def test_a():
    a = 1
    assert a == 1
"""
        p = PythonTestIdentifier()
        blames = TestExtractFunction._create_list_of_blames(t_content)
        res = p.extract_test_functions(blames)
        expected_function = FunctionTest(name_test='test_a', list_lines=blames[4:9])
        assert len(res) == 1
        assert res[0].name_test == expected_function.name_test
        assert res[0].list_lines == expected_function.list_lines

