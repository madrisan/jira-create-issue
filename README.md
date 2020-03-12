# Create new Jira issues at command-line

![Release Status](https://img.shields.io/badge/status-beta-yellow.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/08fcd94fc3f044d9a648bc69bcc03408)](https://www.codacy.com/manual/madrisan/jira-create-issue?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=madrisan/jira-create-issue&amp;utm_campaign=Badge_Grade)
[![Code Climate](https://api.codeclimate.com/v1/badges/0045dfe3c89b62e7a74b/maintainability)](https://codeclimate.com/github/madrisan/jira-create-issue/maintainability)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/madrisan/jira-create-issue.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/madrisan/jira-create-issue/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/madrisan/jira-create-issue.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/madrisan/jira-create-issue/context:python)

A Python script for creating new Jira issues (a task by default) at command-line.

## System Requirements

This script requires Python 3 and the [jira-python](https://pypi.org/project/jira/) library to be installed.

## Configuration

First the configuration file needs to be customized.
```
config:
  jira_ca_bundle: /etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt
  jira_default_assignee: me
  jira_default_project_id: 00001
  jira_password: 'TXlQQHNzdzByZA=='
  jira_server: https://jira.example.com
  jira_user: jira_login_name
  user_issue_type:
    infra:
      labels:
        - "Infrastructure"
    ci:
      jira_project_id: 00002
      labels:
        - "CI"
        - "Development"
```

The password must is masked using a standard base64 encoding:
```
$ python3
Python 3.7.6 (default, Jan 30 2020, 09:44:41)
[GCC 9.2.1 20190827 (Red Hat 9.2.1-1)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
>>> import base64
>>> print(base64.b64encode("MyP@ssw0rd".encode("utf-8")))
b'TXlQQHNzdzByZA=='
>>> exit()
```

## Usage

Here's an example of usage of the front-end script.
```
./jira_new_issue.py \
    --issue-type "ci" \
    --assignee "another.user" \
    --summary "This ia a new jira task" \
    --description "A longer description follows here..."
```

Optionally the command-line option `--in-progress` can be added, to switch the issue to the status `In Progress`.
