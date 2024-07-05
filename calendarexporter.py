# -*- coding: utf-8 -*-
""" An example of how to use Hansoft's GraphQL API

Exports all releases from provided project to an .ics file.
Depends on:
-- ics v. 0.7.2
"""
import sys
import getopt
from ics import Calendar, Event

from graphqlclient import HansoftGraphQLClient
import settings

ENV = 'dev'

if ENV not in settings.CONNECTION:
    print("Unknown ENV. Check settings.py")
    sys.exit(0)

client = HansoftGraphQLClient(settings.CONNECTION[ENV]["URL"],
                              settings.CONNECTION[ENV]["USER"],
                              settings.CONNECTION[ENV]["PASSWORD"])

outputfile = None
project = None

# Check for command line arguments
opts, args = getopt.getopt(sys.argv[1:], "hp:o:", ["project=", "ofile="])
for opt, arg in opts:
    if opt == '-h':
        print('calendarimport.py -p <projectname> -o <output file>')
        sys.exit()
    elif opt in ("-p", "--project"):
        project = arg
    elif opt in ("-o", "--ofile"):
        outputfile = arg

if not project:
    project = input("Project Name: ")

if not outputfile:
    outputfile = project + ".ics"

projects = client.listProjects()
if project not in list(projects.keys()):
    print("Project does not exist")
    sys.exit(0)

project_id = projects[project]

releases = client.listReleases(project_id)

c = Calendar()

for r in releases:
    e = Event()
    e.name = r
    e.begin = releases[r]
    c.events.add(e)
c.events
with open(outputfile, 'w') as my_file:
    my_file.writelines(c.serialize_iter())

print("Exported to:", outputfile)
sys.exit(0)
