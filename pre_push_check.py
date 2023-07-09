#!/usr/bin/env python3

import tomlkit
import requests

# load the project file
with open("pyproject.toml", "r") as f:
    doc = tomlkit.parse(f.read())

# extract the current version
current_version = doc["tool"]["poetry"]["version"]

# get the package name
package_name = doc["tool"]["poetry"]["name"]

# check PyPI for this version
resp = requests.get(f"https://pypi.org/pypi/{package_name}/{current_version}/json")

if resp.status_code == 200:
    print(f"Version {current_version} of {package_name} already exists on PyPI!")
    exit(1)
