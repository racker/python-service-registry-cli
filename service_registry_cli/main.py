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
import logging
import sys
from os.path import join as pjoin

import libcloud.security
from cliff.app import App
from cliff_rackspace.command_manager import CommandManager
from cliff_rackspace.commands.help import HelpAction

from service_registry_cli import __version__

CA_CERT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            'data/cacert.pem')
COMMANDS_PATH = pjoin(os.path.dirname(__file__), 'commands/')

libcloud.security.CA_CERTS_PATH.insert(0, CA_CERT_PATH)


class ServiceRegistryApp(App):

    log = logging.getLogger(__name__)

    DEFAULT_VERBOSE_LEVEL = 0

    def __init__(self):
        super(ServiceRegistryApp, self).__init__(
            description='Rackspace Service Registry Command Line Client',
            version=__version__,
            command_manager=CommandManager('service_registry_cli',
                                           COMMANDS_PATH),
        )

    def build_option_parser(self, description, version):
        # Replace HelpAction with the one which supports sub-commands
        argparse_kwargs = {'conflict_handler': 'resolve'}
        parser = super(ServiceRegistryApp, self).\
            build_option_parser(description,
                                version,
                                argparse_kwargs=argparse_kwargs)
        parser.add_argument(
            '-h', '--help',
            action=HelpAction,
            nargs=0,
            default=self,
            help='show this help message and exit',
        )
        return parser


def main(argv=sys.argv[1:]):
    myapp = ServiceRegistryApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
