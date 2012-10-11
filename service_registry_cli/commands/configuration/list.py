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

import logging

from cliff.lister import Lister

from service_registry_cli.utils import BaseListCommand, get_client


class ListCommand(BaseListCommand, Lister):
    """
    Return a list of the configuration values.
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        client = get_client(parsed_args)
        marker = parsed_args.marker if parsed_args.marker else None
        limit = parsed_args.limit if parsed_args.limit else None
        values = client.configuration.list(marker=marker, limit=limit)['values']

        result = [(value['id'], value['value'])
                  for value in values]
        return (('ID', 'Value'), result)
