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

from cliff.formatters.table import TableFormatter

__all__ = [
    'PaginatedListFormatter'
]


class PaginatedListFormatter(TableFormatter):
    def add_argument_group(self, parser):
        pass

    def emit_list(self, column_names, data, stdout, parsed_args):
        super(PaginatedListFormatter, self).emit_list(column_names, data,
                                                      stdout, parsed_args)

        if len(data) >= 1 and parsed_args.returned_limit:
            print ''

        if parsed_args.returned_limit:
            print 'Limit: %s' % (parsed_args.returned_limit)

        if parsed_args.returned_marker:
            print 'Marker in use: %s' % (parsed_args.returned_marker)

        if parsed_args.returned_next_marker:
            print 'Next marker: %s' % (parsed_args.returned_next_marker)

        return
