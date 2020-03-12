#!/usr/bin/python3

# A simple library for opening new jira issues
# Copyright (C) 2020 Davide Madrisan <davide.madrisan@gmail.com>
# SPDX-License-Identifier: Apache-2.0

from jira.client import JIRA
import base64
import logging
import os
import yaml

log = logging.getLogger(__name__)

class Jira():
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(self.path, 'config.yaml')

        if not os.path.exists(self.config_file):
            raise RuntimeError(
                'No such file: {0}'.format(self.config_file))
        try:
            with open(self.config_file, 'r') as fp_:
                try:
                    data = yaml.safe_load(fp_)
                except yaml.YAMLError as exc:
                    raise ValueError((
                        "Error while parsing {0}: {1}"
                        .format(self.config_file, exc)))
        except os.error as exc:
            raise RuntimeError(
                'Failed to read {0}: {1}'.format(self.config_file, exc))

        self.config = data['config']
        self._default_assignee = self.config.get('jira_default_assignee', None)
        self._default_project_id = self.config.get('jira_default_project_id', None)
        self._server_url = self.config['jira_server']
        self._user_issue_type = self.config.get('user_issue_type', {})

        options = {
            'server': self.config['jira_server'],
            'verify': self.config['jira_ca_bundle']
        }
        try:
            jira_user = self.config['jira_user']
            jira_password = (base64.b64decode(self.config['jira_password'])
                                   .decode('utf-8'))
            basic_auth = (jira_user, jira_password)
            self.instance = JIRA(basic_auth=basic_auth,
                                 logging=False,
                                 max_retries=1,
                                 options=options)
        except Exception as err:
            raise RuntimeError((
                "Failed to establish a new connection to JIRA: {}: {}"
                .format(type(err).__name__, err)))

    @property
    def default_assignee(self):
        '''
        Return the default assignee set in the configuration.
        '''
        return self._default_assignee

    @property
    def default_project_id(self):
        '''
        Return the default project ID set in the configuration.
        '''
        return self._default_project_id

    def issue_project_id(self, user_issue_type):
        '''
        Return the Jira project ID associated to the given user issue type
        or the default one if not configured.
        '''
        try:
            project_id = self._user_issue_type[user_issue_type]['jira_project_id']
        except:
            project_id = self._default_project_id

        return project_id

    def issue_labels(self, user_issue_type):
        '''
        Return the labels configured for the given user issue type.
        Rise an exception if this setting is not found in the configuration.
        '''
        try:
            return self._user_issue_type[user_issue_type]['labels']
        except Exception as err:
            raise RuntimeError((
                'Failed to find the issue labels for "{}" in the configuration file'
                .format(issue_type)))

    @property
    def server_url(self):
        '''
        Return the Jira server URL.
        '''
        return self._server_url

    def create_issue(self, summary, description=None, assignee=None, issuetype='Task', labels=[], project_id=None):
        '''
        Create a new Jira issue of type 'Task' by default.
        '''
        if not project_id:
            project_id = self.default_project_id
            if not project_id:
                raise Exception(
                    'neither project_id arg, nor jira_default_project_id in config are defined')
        data = {
            'issuetype': {
                'name': issuetype
            },
            'project': {
                   'id': project_id
            },
            'summary': summary
        }

        if assignee:
            data['assignee'] = {
                'name': assignee
        }
        if description:
            data['description'] = description
        if labels:
            data['labels'] = labels

        new_issue = self.instance.create_issue(fields=data)
        return new_issue

    def projects(self):
        '''
        Return the list of all the project objects.
        '''
        return self.instance.projects()

    def project(self, project_name):
        '''
        Return the list of all the projects
        '''
        return self.instance.project(project_name)

    def status(self, issue_id):
        '''
        Get the current status of the given issue.
        '''
        issue = self.instance.issue(issue_id)
        return issue.fields.status

    def transition(self, issue_id, new_status):
        '''
        Switch the issue 'issue_id' to the new status 'new_status'.
        '''
        issue = self.instance.issue(issue_id)
        transitions = self.instance.transitions(issue)

        transition_names = [t['name'] for t in transitions]
        if new_status not in transition_names:
            raise RuntimeError((
                'Invalid transition status \'{}\', can be one of the following: {}'
                .format(new_status,
                        ', '.join(transition_names))))

        r_json = self.instance.transition_issue(issue, new_status)
        return r_json

    def transitions(self, issue_id):
        '''
        Return the list of the available transitions for the given issue.
        '''
        issue = self.instance.issue(issue_id)
        transitions = self.instance.transitions(issue)
        return [(t['id'], t['name']) for t in transitions]
