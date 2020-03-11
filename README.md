# Create new Jira issues at command-line

A Python script for creating new Jira issues (a task by default) at command-line.

## System Requirements

This script requires Python 3 and the [jira-python](https://pypi.org/project/jira/) library to be installed.

## Usage

First the configuration file needs to be customized.
```
config:
  jira_ca_bundle: /etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt
  jira_default_assignee: me
  jira_default_project_id: 00001
  jira_password: MyP@ssw0rd
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
Here's an example of usage of the front-end script.
```
./jira_new_issue.py \
    --issue-type "ci" \
    --assignee "another.user" \
    --summary "This ia a new jira task" \
    --description "A longer description follows here..."
```
