#!/usr/bin/python3

# Create new Jira issues at command-line.
# Copyright (C) 2020 Davide Madrisan <davide.madrisan@gmail.com>
# SPDX-License-Identifier: Apache-2.0

import argparse
import simplejira

__author__ = "Davide Madrisan"
__copyright__ = "Copyright (C) 2020 Davide Madrisan"
__license__ = "Apache License 2.0 (Apache-2.0)"
__version__ = "1"
__email__ = "davide.madrisan@gmail.com"
__status__ = "stable"

def argparser():
    """This function parses and return arguments passed in"""
    descr = ("Open a new Jira task.")
    parser = argparse.ArgumentParser(
                 formatter_class = argparse.RawDescriptionHelpFormatter,
                 description = copyleft(descr))

    parser.add_argument(
        "-a", "--assignee",
        action="store", dest="assignee",
        help="Assignee of the issue")
    parser.add_argument(
        "-d", "--description",
        action="store", dest="description",
        help="Long descripion for the issue to be created")
    parser.add_argument(
        "--in-progress",
        action="store", dest="status_in_progress",
        help="Change the ticket status to 'In Progress'")
    parser.add_argument(
        "-s", "--summary",
        action="store", dest="summary", required=True,
        help="Summary of the new issue")
    parser.add_argument(
        "-t", "--issue-type",
        action="store", dest="issue_type",
        help="Optional type of the issue to be created")

    return parser.parse_args()

def copyleft(descr):
    """Print the Copyright message and License """

    return ("{0} -- v{1}\n{2} <{3}>\nLicense: {4}"
        .format(descr, __version__, __copyright__, __email__, __license__))

if __name__ == '__main__':
    args = argparser()
    jira = simplejira.Jira()

    options = {
       'assignee': args.assignee if args.assignee else jira.default_assignee,
       'description': args.description,
       'summary': args.summary
    }
    if args.issue_type:
        options['labels'] = jira.issue_labels(args.issue_type)
        options['project_id'] = jira.issue_project_id(args.issue_type)

    new_issue = jira.create_issue(**options)

    print(('Ticket URL : {}/browse/{}'
           .format(jira.server_url, new_issue)))
    print(('Ticket Status : {}'
           .format(jira.status(new_issue))))

    if status_in_progress:
        jira.transition(new_issue, 'In Progress')
        print(('New Ticket Status : {}'
               .format(jira.status(new_issue))))
