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

from cliff.show import ShowOne

from service_registry_cli.utils import (
    BaseShowCommand,
    get_client,
    format_metadata
)


class GetCommand(BaseShowCommand, ShowOne):
    """
    Return a single service.
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        client = get_client(parsed_args)
        value = client.services.get(parsed_args.object_id)
        metadata_str = format_metadata(value['metadata'])
        service_tuple = (value['id'],
                         value['heartbeat_timeout'],
                         value['last_seen'],
                         ', '.join(value['tags']),
                         metadata_str)
        return (('Service ID', 'Heartbeat Timeout', 'Last Seen', 'Tags',
                 'Metadata'), service_tuple)
