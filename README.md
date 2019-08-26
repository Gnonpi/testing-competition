# testing-competition
 
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

Inspired by Spotify's testing-game, discover who contributed most to your test base


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To start using `testing_competition`,
you're going to need at least:
- Git
- Python3.6+

You can find instructions on how to install Git [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git),
and instructions there for Python [here](https://www.python.org/downloads/).

If you want to use Poetry to install the dependencies 
(I recommend it),
you can find infos [here](https://poetry.eustace.io/docs/#installation).

### Installing

Assuming you're using Poetry 
(if you don't [pip](https://pip.pypa.io/en/stable/) can work with the `pyproject.toml`),
all you have to do to use it is:

```
$ cd testing_competition
$ poetry install --no-dev
```

End with an example of getting some data out of the system or using it for a little demo

Once you get all installed, you can use it like that:

```
# assuming /path/to/repo is the path to the git repository with the tests you wanna analyse
$ poetry run python testing_competition/entry_command /path/to/repo
INFO:testing_competition:Starting to look for tests at: /path/to/repo
INFO:testing_competition:Extracting test data from test_file_example.py
....
gnonpi:
Tests owned: 17 - 12.1%
Tests associated with: 17 - 12.1%
Written 178 test lines - 9.6%
vadim:
Tests owned: 0 - 0.0%
Tests associated with: 5 - 3.6%
Written 6 test lines - 0.3%
```

## Running the tests

Tests are meant to be via [pytest](https://pytest.org/en/latest/).
Let's install the needed dependencies with Poetry:

```
$ poetry install
```

Then, simply run:
```
$ poetry run pytest
```

## Built With

* [Git](https://git-scm.com/) - The distributed version control system
* [Poetry](https://git-scm.com/) - Python dependency management and packaging made easy
* [Pytest](https://pytest.org/en/latest/) - The pytest framework makes it easy to write small tests, yet scales to support complex functional testing for applications and libraries
* [Click](https://click.palletsprojects.com/en/7.x/) - Click is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## License

This project is licensed under the GNU GPL3 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

To the authors of https://github.com/spotify/testing-game,
I'm only retaking the idea at my sauce.

# TODOs
Personal list of things I'd like to add:
* [ ] a class that take ContributionCounter and do an output (stdout or file)
* [ ] more language identifiers: Java, C, JS ? different test frameworks?
* [ ] allow to tune language identifiers with config files (test_* vs *_test)
* [ ] add pytest-cov and more tests :)
* [ ] something better than parsing "git blame"?
* [ ] test with different python versions via tox
* [ ] provide a setup.py or requirements.txt (automated)
* [ ] make true entrypoints
* [ ] coding style
* [ ] add github badges
* [ ] generate and upload documentation
