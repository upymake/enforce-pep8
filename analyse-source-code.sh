#!/usr/bin/env bash

PACKAGE="punish"


pretty-printer-box() {
:<<DOC
    Provides pretty-printer check box
DOC
    echo "Start ${1} analysis ..."
}


remove-pycache() {
:<<DOC
    Removes python cache directories
DOC
    ( find . -depth -name __pycache__ | xargs rm -r )
}


check-black() {
:<<DOC
    Runs "black" code analyser
DOC
    pretty-printer-box "black" && ( black --check ${PACKAGE} )
}


check-flake8() {
:<<DOC
    Runs "flake8" code analysers
DOC
    pretty-printer-box "flake" && ( flake8 ./  )
}


check-pylint() {
:<<DOC
    Runs "pylint" code analyser
DOC
    pretty-printer-box "pylint" && ( pylint $(find "${PACKAGE}/") )
}


check-mypy() {
:<<DOC
    Runs "mypy" code analyser
DOC
    pretty-printer-box "mypy" && ( mypy --package "${PACKAGE}" )
}


check-docstrings() {
:<<DOC
     Runs "pydocstyle" static documentation code style formatter
DOC
    pretty-printer-box "pydocstyle" && ( pydocstyle --explain --count ${PACKAGE} )
    pretty-printer-box "interrogate" && interrogate --config pyproject.toml ${PACKAGE}
}


check-unittests() {
:<<DOC
    Runs unittests using "pytest" framework
DOC
    pretty-printer-box "unitests" && pytest
}


main() {
:<<DOC
    Runs "main" code analyser
DOC
    (
      remove-pycache
      check-black && \
      check-mypy && \
      check-pylint && \
      check-docstrings && \
      check-flake8 && \
      check-unittests
    )
}

main