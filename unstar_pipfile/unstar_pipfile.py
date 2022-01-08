"""This module contains main codebase for unstar_pipfile tool."""

import json
import os.path
import sys

import click
from tomlkit import dumps, parse

PIPFILE = "Pipfile"
PIPFILE_LOCK = "Pipfile.lock"


@click.command()
def unstar():
    """Scan Pipfile.lock and replace any stars in Pipfile with precise versions from the lock file."""

    # check that required files exist in current working directory
    check_status, message = check_files()
    if not check_status:
        click.echo(message=message, err=True)
        sys.exit(1)

    amend_pipfile()


def amend_pipfile():
    """Amend Pipfile with versions."""

    with open(PIPFILE, "r") as pipfile:
        # read Pipfile and parse into a toml document
        pipfile_text = pipfile.read()
        toml_doc = parse(pipfile_text)
        new_toml_doc = parse(pipfile_text)

        # update dependency versions
        packages = get_packages_and_versions()
        for package_name, version in toml_doc["packages"].items():
            if version == "*" and package_name.lower() in packages:
                new_toml_doc["packages"][package_name] = packages[package_name.lower()]
            elif (
                isinstance(version, dict)
                and "version" in version
                and version["version"] == "*"
            ):
                new_toml_doc["packages"][package_name]["version"] = packages[
                    package_name.lower()
                ]

        # update dev dependency versions
        dev_packages = get_packages_and_versions("develop")
        for package_name, version in toml_doc["dev-packages"].items():
            if version == "*" and package_name.lower() in dev_packages:
                new_toml_doc["dev-packages"][package_name] = dev_packages[
                    package_name.lower()
                ]
            elif (
                isinstance(version, dict)
                and "version" in version
                and version["version"] == "*"
            ):
                new_toml_doc["dev-packages"][package_name]["version"] = dev_packages[
                    package_name.lower()
                ]

    with open(PIPFILE, "w") as new_pipfile:
        new_pipfile.write(dumps(new_toml_doc))


def check_files() -> tuple[bool, str]:
    """Check if necessary files are present in current working directory."""
    files = (PIPFILE, PIPFILE_LOCK)
    for file in files:
        if not os.path.isfile(file):
            return False, f"Can't find {file}"
    return True, ""


def get_packages_and_versions(package_type: str = "default") -> dict:
    """Parse Pipfile.lock and extract package names and versions."""
    ret = {}
    with open(PIPFILE_LOCK, "r") as pipfile:
        packages = json.load(pipfile)[package_type]
        for package_name, package_data in packages.items():
            if "version" in package_data:
                ret[package_name] = package_data["version"]
    return ret
