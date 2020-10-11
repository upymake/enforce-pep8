#!/usr/bin/env bats


setup() {
:<<DOC
  Installs package via pip
DOC
  pip install ${PACKAGE_NAME}
}


teardown() {
:<<DOC
  Removes package via pip
DOC
  pip uninstall -y ${PACKAGE_NAME}
}


@test "package name" {
:<<DOC
  Test package name
DOC
  pip list | grep ${PACKAGE_NAME}
  [ "$?" -eq 0 ]
}


@test "package version" {
:<<DOC
  Test package version
DOC
  pip list | grep ${PACKAGE_VERSION}
  [ "$?" -eq 0 ]
}
