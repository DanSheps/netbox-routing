# Netbox Routing

[![PyPI](https://img.shields.io/pypi/v/netbox-routing.svg)](https://pypi.org/project/netbox-routing/)
[![Python](https://img.shields.io/pypi/pyversions/netbox-routing.svg)](https://pypi.org/project/netbox-routing/)
[![NetBox](https://img.shields.io/badge/NetBox-4.7%2B-success.svg)](https://github.com/netbox-community/netbox)
[![CI](https://github.com/dansheps/netbox-routing/actions/workflows/ci.yml/badge.svg)](https://github.com/dansheps/netbox-routing/actions/workflows/ci.yml)
[![License: AGPL-3.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A plugin for tracking all kinds of routing information

## Features

### Current features

* Static routing
* Dynamic routing
  * EIGRP
  * BGP
    * Templates/Group inheritance
    * IPv4/IPv46 AF VRF support
    * VPNv4 support
  * OSPF

### Under development


### Roadmapped

* Dynamic Routing
  * IS-IS

# Requirements

* Netbox 4.5+
* Python 3.12+

## Compatibility Matrix

|       | Netbox 3.2.x   | NetBox 4.1.x   | Netbox 4.2.x   | NetBox 4.3.x - 4.4.x | NetBox 4.5.x   | NetBox 4.6.x   | NetBox 4.7.x   |
|-------|----------------|----------------|----------------|----------------------|----------------|----------------|----------------|
| 0.1.x | Compatible     | Not Compatible | Not Compatible | Not Compatible       | Not Compatible | Not Compatible | Not Compatible |
| 0.2.x | Not Compatible | Compatible     | Not Compatible | Not Compatible       | Not Compatible | Not Compatible | Not Compatible |
| 0.3.0 | Not Compatible | Not Compatible | Compatible     | Not Compatible       | Not Compatible | Not Compatible | Not Compatible |
| 0.3.1 | Not Compatible | Not Compatible | Not Compatible | Compatible           | Not Compatible | Not Compatible | Not Compatible |
| 0.3.2 | Not Compatible | Not Compatible | Not Compatible | Not Compatible       | Compatible     | Not Compatible | Not Compatible |
| 0.4.x | Not Compatible | Not Compatible | Not Compatible | Not Compatible       | Compatible     | Not Compatible | Not Compatible |
| 0.5.0 | Not Compatible | Not Compatible | Not Compatible | Not Compatible       | Not Compatible | Compatible     | Not Compatible |
| 0.5.x | Not Compatible | Not Compatible | Not Compatible | Not Compatible       | Not Compatible | Compatible     | Compatible     |

## Installation

Install the python module

`pip install netbox-routing`

To install, simply include this plugin in the plugins configuration section of netbox.

Example:
```python
    PLUGINS = [
        'netbox_routing'
    ],
```

> [!NOTE]
> If you utilize netbox-bgp this plugin is not compatible, however there is now a migration tool built in.
> 
> You will need to remove `netbox-bgp` from the plugin list, and make sure `netbox-routing` is installed.

Once installed, run the migrations:

`python netbox/manage.py migrate`

Run the static collections:

`python netbox/manage.py collectstatic --no-input`

If migrating from `netbox-bgp` run migrate-netbox-bgp:

`python netbox/manage.py migrate-netbox-bgp`

## Configuration

None

## Usage

TBD

## Additional Notes

TBD

## Contribute

Contributions are always welcome!  Please open an issue first before contributing as the scope is going to be kept
intentionally narrow


