#!/usr/bin/python3

#!/usr/bin/python3

# Print the list of the Jira Projects in tabular form.
# Copyright (C) 2020 Davide Madrisan <davide.madrisan@gmail.com>
# SPDX-License-Identifier: Apache-2.0

from tabulate import tabulate
import simplejira

if __name__ == '__main__':
    jira = simplejira.Jira()
    projects = jira.projects()

    #data = [[0 for x in range(projects)] for y in [project.id, project.key, project.name]]

    data = []
    for project in projects:
        row = [ project.id, project.key, project.name ]
        data.append(row)

    table = tabulate(data,
                     headers=['ID', 'Key', 'Name'],
                     tablefmt='simple')
    print(table)
