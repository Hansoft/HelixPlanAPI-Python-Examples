# Helix Plan API Python Examples

Examples to explore the Helix Plan API using Python.

## GraphQL Client

* Simple implementation of various useful queries and mutations used by the other scripts.

## Test Data Creator

* Generates users, groups and projects with real-looking names
* Sets user permissions
* Add users to groups and projects

## Calendar Exporter

* Exports all releases from provided project to an .ics file
* Depends on:
	* ics v. 0.7.2

## Copy Bugs

* Simple copy of bugs between projects (just item name)

## Dependencies

* Python 3.8
* [Helix Plan Server 2024.1/013 or later](https://www.perforce.com/downloads/hansoft-server)
* [Helix Plan API 2024.1/001](https://www.perforce.com/downloads/helix-plan-api) or [Helix Plan Web 2024.1/001](https://www.perforce.com/downloads/helix-plan-web-client)
* Helix Plan license with the SDK enabled

## Quick Start

* Download and install the dependencies
* Modify the URL, USER and PASSWORD in `settings.py` with your login details
* Run `python3 testdatacreator.py` and follow the instructions.
