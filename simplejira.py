#!/usr/bin/python3

# A simple library for opening new jira issues
# Copyright (C) 2020 Davide Madrisan <davide.madrisan@gmail.com>
# SPDX-License-Identifier: Apache-2.0

from jira.client import JIRA
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
                    data = yaml.load(fp_, Loader=yaml.FullLoader)
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

        options = {
            'server': self.config['jira_server'],
            'verify': self.config['jira_ca_bundle']
        }
        try:
            basic_auth = (self.config['jira_user'],
                          self.config['jira_password'])
            self.instance = JIRA(basic_auth=basic_auth,
                                 logging=False,
                                 max_retries=1,
                                 options=options)
        except Exception as err:
            raise RuntimeError("Failed to establish a new connection to JIRA: %s: %s",
                               type(err).__name__, err)

    @property
    def default_assignee(self):
        return self._default_assignee

    @property
    def default_project_id(self):
        return self._default_project_id

    @property
    def server_url(self):
        return self._server_url

    def create_issue(self, summary, description=None, assignee=None, issuetype='Task', labels=[], project_id=None):
        if not project_id:
            project = self.default_project_id
            if not project:
                raise Exception(
                    'neither project_id arg, nor jira_default_project_id in config are defined')
        data = {
            'issuetype': {
                'name': issuetype
            },
            'project': {
                   'id': project
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
        return self.instance.projects()

    def project(self, project_name):
        return self.instance.project(project_name)
