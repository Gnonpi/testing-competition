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

    def test_contain_multiple_tests(self):
        t_content = """
def test_first_test():
    a = 1

    assert a == 1
    
def test_second_test():
    s = 0 
    for i in range(4):
        s += i  
    assert s == 6
    assert s == 5 + 1
def test_third():
    assert True
"""
        p = PythonTestIdentifier()
        blames = TestExtractFunction._create_list_of_blames(t_content)
        res = p.extract_test_functions(blames)
        first_function = FunctionTest(name_test='test_first_test',
                                      list_lines=blames[1:5])
        second_function = FunctionTest(name_test='test_second_test',
                                       list_lines=blames[6:12])
        third_function = FunctionTest(name_test='test_third',
                                      list_lines=blames[12:])

        assert len(res) == 3
        assert res[0].name_test == first_function.name_test
        assert res[0].list_lines == first_function.list_lines

        assert res[1].name_test == second_function.name_test
        assert res[1].list_lines == second_function.list_lines

        assert res[2].name_test == third_function.name_test
        assert res[2].list_lines == third_function.list_lines

    def test_contain_test_class(self):
        t_content = """
import pytest

print('ok')

class TestSomething:
    def test_first(self):
        assert 1
    
    def test_second(self, client_fixture):
        a = 1

        b = 2
                 
        assert a + b == 3 
        """
        p = PythonTestIdentifier()
        blames = TestExtractFunction._create_list_of_blames(t_content)
        res = p.extract_test_functions(blames)
        first_function = FunctionTest(name_test='test_first',
                                      list_lines=blames[6:8])
        second_function = FunctionTest(name_test='test_second',
                                       list_lines=blames[9:15])
        assert len(res) == 2
        assert res[0].name_test == first_function.name_test
        assert res[0].list_lines == first_function.list_lines
        assert res[1].name_test == second_function.name_test
        assert res[1].list_lines == second_function.list_lines
