# -*- coding: utf-8 -*-
""" An example of how to use Hansoft's GraphQL API

Copies bugs from one project to another (just name).
"""
import sys
import getopt

from graphqlclient import HansoftGraphQLClient
import settings

FIND_QUERY = "itemtype=Bug"  # Use Helix Plan's Query Language
MAX = 10  # Maximum number of bugs cloned
ENV = 'dev'

if ENV not in settings.CONNECTION:
    print("Unknown ENV. Check settings.py")
    sys.exit(0)

client = HansoftGraphQLClient(settings.CONNECTION[ENV]["URL"],
                              settings.CONNECTION[ENV]["USER"],
                              settings.CONNECTION[ENV]["PASSWORD"])

project_source = None
project_target = None

# Check for command line arguments
opts, args = getopt.getopt(sys.argv[1:], "hs:t:", ["source=", "target="])
for opt, arg in opts:
    if opt == '-h':
        print('clonebugs.py -s <source project> -t <target project>')
        sys.exit()
    elif opt in ("-s", "--source"):
        project = arg
    elif opt in ("-t", "--target"):
        outputfile = arg

if not project_source:
    project_source = input("Source Project Name: ")
if not project_target:
    project_target = input("Target Project Name: ")

if project_source == project_target:
    print("Target and source is identical.")
    sys.exit()

projects = client.listProjectsQA()
if project_source not in list(projects.keys()):
    print("Source Project does not exist")
    sys.exit(0)
if project_target not in list(projects.keys()):
    print("Target Project does not exist")
    sys.exit(0)

project_source_id = projects[project_source]
project_target_id = projects[project_target]

# Get all bugs
print("Listing items...")
items = client.listItems(project_source_id, FIND_QUERY)

if len(items) > MAX:
    print("Too many bugs")
    sys.exit(0)

# Create bugs
for item in items:
    print("Creating bug:", items[item])
    response = client.createBug(project_target_id, items[item])

print("Cloning completed")
sys.exit(0)
