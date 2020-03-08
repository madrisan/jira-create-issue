# Create new Jira issues at command-line

A Python script for creating new Jira issues (a task by default) at command-line.

## System Requirements

This script requires Python 3 and the [jira-python](https://pypi.org/project/jira/) library to be installed.

## Usage

```
./jira_new_issue.py \
    -a "the.assignee" \
    -s "A new jira task" \
    -d "A longer description follows here..."
```
