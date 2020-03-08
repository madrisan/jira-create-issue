#!/usr/bin/python3

# Common functions for Jira issues creation.
# Copyright (C) 2020 Davide Madrisan <davide.madrisan@gmail.com>
# SPDX-License-Identifier: Apache-2.0

__author__ = "Davide Madrisan"
__copyright__ = "Copyright (C) 2020 Davide Madrisan"
__license__ = "Apache License 2.0 (Apache-2.0)"
__version__ = "1"
__email__ = "davide.madrisan@gmail.com"
__status__ = "stable"

import argparse

def copyleft(descr):
    """Print the Copyright message and License """

    return ("{0} -- v{1}\n{2} <{3}>\nLicense: {4}"
        .format(descr, __version__, __copyright__, __email__, __license__))

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
        "-s", "--summary",
        action="store", dest="summary", required=True,
        help="Summary of the new issue")

    return parser.parse_args()
