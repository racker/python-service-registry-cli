# Copyright 2012 Rackspace
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from os.path import join as pjoin, expanduser
from datetime import datetime

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

from cliff.command import Command
from cliff.lister import Lister

from service_registry.client import Client

CREDENTIALS_FILE = '.raxrc'
CONFIG_PATH = pjoin(expanduser('~'), CREDENTIALS_FILE)

SERVICE_EVENTS = ['service.join', 'service.timeout', 'service.remove']


class BaseCommand(Command):
    def get_parser(self, prog_name):
        parser = super(BaseCommand, self).get_parser(prog_name=prog_name)
        parser.add_argument('--username', dest='username')
        parser.add_argument('--api-key', dest='api_key')
        parser.add_argument('--api-url', dest='api_url')
        parser.add_argument('--region', dest='region')
        return parser


class BaseListCommand(BaseCommand, Lister):
    def get_parser(self, prog_name):
        parser = super(BaseListCommand, self).get_parser(prog_name=prog_name)
        parser.add_argument('--limit', dest='limit')
        parser.add_argument('--marker', dest='marker')
        return parser

    @property
    def formatter_default(self):
        return 'paginated_table'


class BaseShowCommand(BaseCommand):
    def get_parser(self, prog_name):
        parser = super(BaseShowCommand, self).get_parser(prog_name=prog_name)
        parser.add_argument('--id', dest='object_id')
        return parser


def get_client(parsed_args):
    config = get_config()

    username = config['username']
    api_key = config['api_key']
    if parsed_args.username:
        username = parsed_args.username

    if parsed_args.api_key:
        api_key = parsed_args.api_key

    #username = parsed_args.username
    #api_key = parsed_args.api_key

    api_url = parsed_args.api_url
    region = parsed_args.region

    if not username:
        raise ValueError('Missing required argument: username')

    if not api_key:
        raise ValueError('Missing required argument: api-key')

    kwargs = {}

    if api_url is not None:
        kwargs['base_url'] = api_url

    if region is not None:
        kwargs['region'] = region

    c = Client(username=username, api_key=api_key, **kwargs)

    return c


def format_metadata(metadata_dict):
    metadata_str = ''

    count = len(metadata_dict)
    i = 0
    for key, value in metadata_dict.items():
        i += 1
        metadata_str += '%s: %s' % (key, value)

        if i < count:
            metadata_str += ', '

    return metadata_str


def format_timestamp(timestamp):
    if not timestamp:
        return ''

    return datetime.fromtimestamp(timestamp / 1000) \
                   .strftime('%Y-%m-%d %H:%M:%S')


def format_event_payload(event_response):
    event_payload_str = ''
    event_type = event_response['type']
    event_payload = event_response['payload']

    if not event_payload:
        return event_payload_str

    if event_type in SERVICE_EVENTS:
        for key, value in event_payload.iteritems():
            if key == 'metadata':
                metadata_str = format_metadata(value)
                event_payload_str += 'metadata: %s\n' % (metadata_str)
            elif key == 'tags':
                event_payload_str += '%s: %s\n' % (key, ', '.join(value))
            else:
                event_payload_str += '%s: %s\n' % (key, value)
    else:
        for key, value in event_payload.iteritems():
            event_payload_str += '%s: %s\n' % (key, value)
        event_payload_str = event_payload_str.strip(',\n')

    return event_payload_str


def get_config():
    keys = [['credentials', 'username', 'username'],
            ['credentials', 'api_key', 'api_key'],
            ['api', 'url', 'api_url'],
            ['auth_api', 'url', 'auth_url'],
            ['ssl', 'verify', 'ssl_verify']]

    result = {}

    result['username'] = os.getenv('RAXSR_USERNAME', None)
    result['api_key'] = os.getenv('RAXSR_API_KEY', None)
    result['api_url'] = os.getenv('RAXSR_API_URL', None)
    result['auth_url'] = os.getenv('RAXSR_AUTH_URL', None)
    result['ssl_verify'] = os.getenv('RAXSR_SSL_VERIFY', None)

    config = ConfigParser.ConfigParser()
    config.read(os.getenv('RAXSR_RAXRC') or CONFIG_PATH)

    for (config_section, config_key, key) in keys:
        if result[key]:
            # Already specified as an env variable
            continue

        try:
            value = config.get(config_section, config_key)
        except ConfigParser.Error:
            continue

        result[key] = value

    # convert "false" to False
    if result['ssl_verify']:
        result['ssl_verify'] = not (result['ssl_verify'].lower() == 'false')
    else:
        result['ssl_verify'] = True

    return result
