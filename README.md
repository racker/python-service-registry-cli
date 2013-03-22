# Rackspace Service Registry CLI

Command line client for Rackspace Service Registry. The client currently allows
users to:

* view account limits
* vite active services
* view events
* view, set and remove configuration values

## Installation

`pip install --upgrade service-registry-cli`

## Settings Credentials

Credentials can be set (in order of precedence) as environment variables (RAXSR_USERNAME,
RAXSR_API_KEY, RAXSR_API_URL, RAXSR_AUTH_URL), in a configuration file or you can pass 
them manually to each command.

Default configuration file path is `~/.raxrc` but you can overrride it by
setting the `RAXSR_RAXRC` environment variable. For example:

`RAXSR_RAXRC=~/.raxrc.uk raxsr services list`

### Example Configuration File

```
[credentials]
username=foo
api_key=bar

[api]
url=https://dfw.registry.api.rackspacecloud.com/v1.0

[auth_api]
url=https://identity.api.rackspacecloud.com/v2.0

[ssl]
verify=true
```

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
