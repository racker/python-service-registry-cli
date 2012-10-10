# Rackspace Service Registry CLI

Command line client for Rackspace Service Registry. The client currenty
only offers read-only functionality and allows users to:

* view account limits
* view display active sessions
* vite active services
* view events
* view configuration values

## Installation

`pip install --upgrade service-registry-cli`

## Usage

`raxsr <resource> <action> [options]`

For example:

`raxsr services list`

### Viewing Command Options

`raxsr help services list`

# License

Library is distributed under the [Apache license](http://www.apache.org/licenses/LICENSE-2.0.html).
