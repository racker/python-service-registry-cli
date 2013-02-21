# Rackspace Service Registry CLI

Command line client for Rackspace Service Registry. The client currently allows
users to:

* view account limits
* view display active sessions
* vite active services
* view events
* view, set and remove configuration values

## Installation

`pip install --upgrade service-registry-cli`

## Usage

`raxsr <resource> <action> [options]`

For example:

`raxsr services list`

### Viewing Command Options

`raxsr help services list`

### Custom Output Formatter

To specify a custom formatter, use `-f` option. For example:

`raxsr services list -f json`

#### Available Formatters

* table
* csv
* json
* yaml
* html

# License

Library is distributed under the [Apache license](http://www.apache.org/licenses/LICENSE-2.0.html).
