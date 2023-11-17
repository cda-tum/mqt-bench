Development Guide
=================

Ready to contribute to the project? Here is how to set up a local development environment.

Initial Setup
#############

1. Fork the `cda-tum/mqt-bench <https://github.com/cda-tum/mqt-bench>`_ repository on GitHub (see https://docs.github.com/en/get-started/quickstart/fork-a-repo).

2. Clone your fork locally

    .. code-block:: console

        $ git clone git@github.com:your_name_here/mqt-bench


3. Change into the project directory

    .. code-block:: console

        $ cd mqt-bench

4. Create a branch for local development

    .. code-block:: console

        $ git checkout -b name-of-your-bugfix-or-feature

    Now you can make your changes locally.

5. (Optional, **highly recommended**) Set up a virtual environment

    .. code-block:: console

        $ python3 -m venv venv
        $ source venv/bin/activate

    .. note::

        If you are using Windows, you can use the following command instead:

        .. code-block:: console

            $ python3 -m venv venv
            $ venv\Scripts\activate.bat

    Ensure that pip, setuptools, and wheel are up to date:

    .. code-block:: console

        (venv) $ pip install --upgrade pip setuptools wheel


6. (Optional) Install `pre-commit <https://pre-commit.com/>`_ to automatically run a set of checks before each commit.

    .. code-block:: console

        (venv) $ pipx install pre-commit
        (venv) $ pre-commit install

    If you use macOS, then pre-commit is in brew, use :code:`brew install pre-commit`.

Building the Python module
##########################

The recommended way of building the Python module is to perform an editable install using `pip <https://pip.pypa.io/en/stable/>`_.

    .. code-block:: console

        (venv) $ pip install -e .

The :code:`--editable` flag ensures that changes in the Python code are instantly available without re-running the command.

Running Python Tests
--------------------

The Python part of the code base is tested by unit tests using the `pytest <https://docs.pytest.org/en/latest/>`_ framework.
The corresponding test files can be found in the :code:`tests/` directory.

    .. code-block:: console

        (venv) $ pip install -e ".[test]"
        (venv) $ pytest

This installs all dependencies necessary to run the tests in an isolated environment, builds the Python package, and then runs the tests.

Python Code Formatting and Linting
----------------------------------

The Python code is formatted and linted using a collection of `pre-commit hooks <https://pre-commit.com/>`_.
This collection includes:

- `ruff <https://docs.astral.sh/ruff/>`_ -- an extremely fast Python linter and formatter, written in Rust.
- `mypy <http://mypy-lang.org/>`_ -- a static type checker for Python code


You can install the hooks manually by running :code:`pre-commit install` in the project root directory.
The hooks will then be executed automatically when committing changes.

    .. code-block:: console

        (venv) $ pre-commit run -a
