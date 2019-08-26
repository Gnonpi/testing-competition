from subprocess import SubprocessError

import pytest

from testing_competition.analyse_repo import get_git_blame
from testing_competition.custom_types import BlameLine


class TestGetGitBlame:
    def test_not_a_git_folder(self, tmpdir, monkeypatch):
        directory = tmpdir.mkdir('not-a-git-repo')
        path_to_test = directory / 'test_a.py'

        class FakePopen:
            def __init__(self, list_args, stdout, stderr):
                pass

            def communicate(self, timeout=None):
                out = str.encode('')
                err = str.encode(f"fatal: '{directory}' is outside repository")
                return out, err

        monkeypatch.setattr('testing_competition.analyse_repo.Popen',
                            FakePopen)
        res = get_git_blame(directory, path_to_test)
        assert res == list()

    def test_error_while_doing_git_blame(self, tmpdir, monkeypatch):
        directory = tmpdir.mkdir('not-a-git-repo')
        path_to_test = directory / 'test_a.py'

        class FakePopen:
            def __init__(self, list_args, stdout, stderr):
                pass

            def communicate(self, timeout=None):
                raise SubprocessError('test-error')

        monkeypatch.setattr('testing_competition.analyse_repo.Popen',
                            FakePopen)
        with pytest.raises(SubprocessError):
            get_git_blame(directory, path_to_test)

    def test_small_output(self, tmpdir, monkeypatch):
        directory = tmpdir.mkdir('not-a-git-repo')
        path_to_test = directory / 'test_a.py'
        sample_git_blame = """d95fe604 (Nacho libre 2019-02-12 23:15:09 +0100  7) 
b95fe604 (nikola-tesla-home 2019-02-12 23:15:09 +0100  8) from invoke import task
d95fb604 (Nacho libre 2019-02-12 23:15:09 +0100  9) from invoke.util import cd
c95fe604 (denis-vivies-home 2019-02-12 23:15:09 +0100 10) from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer
"""

        class FakePopen:
            def __init__(self, list_args, stdout, stderr):
                pass

            def communicate(self, timeout=None):
                out = str.encode(sample_git_blame)
                err = str.encode('')
                return out, err

        monkeypatch.setattr('testing_competition.analyse_repo.Popen',
                            FakePopen)

        res = get_git_blame(directory, path_to_test)
        assert len(res) == len(sample_git_blame.splitlines())
        parsed_lines = [
            BlameLine(
                hash_commit='d95fe604',
                author='Nacho libre',
                timestamp='2019-02-12 23:15:09',
                line_number=7,
                content=''),
            BlameLine(
                hash_commit='b95fe604',
                author='nikola-tesla-home',
                timestamp='2019-02-12 23:15:09',
                line_number=8,
                content='from invoke import task'),
            BlameLine(
                hash_commit='d95fb604',
                author='Nacho libre',
                timestamp='2019-02-12 23:15:09',
                line_number=9,
                content='from invoke.util import cd'),
            BlameLine(
                hash_commit='c95fe604',
                author='denis-vivies-home',
                timestamp='2019-02-12 23:15:09',
                line_number=10,
                content='from pelican.server import ComplexHTTPRequestHandler, RootedHTTPServer'),
        ]
        for parsed, expected in zip(res, parsed_lines):
            assert parsed == expected
