#!/usr/bin/python3

# Create new Jira issues at command-line.
# Copyright (C) 2020 Davide Madrisan <davide.madrisan@gmail.com>
# SPDX-License-Identifier: Apache-2.0

import simplejira
from utils import argparser

if __name__ == '__main__':
    args = argparser()
    jira = simplejira.Jira()

    assignee = args.assignee if args.assignee else jira.default_assignee
    # labels of the new jira task
    labels = [
        "Infrastructure"
    ]

    description = args.description
    summary = args.summary
    new_issue = jira.create_issue(summary,
                                  description,
                                  assignee=assignee,
                                  labels=labels)
    print(('{}/browse/{}'
           .format(jira.server_url, new_issue)))
