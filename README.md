# NetBox Routing

[![PyPI](https://img.shields.io/pypi/v/netbox-routing.svg)](https://pypi.org/project/netbox-routing/)
[![Python](https://img.shields.io/pypi/pyversions/netbox-routing.svg)](https://pypi.org/project/netbox-routing/)
[![NetBox](https://img.shields.io/badge/NetBox-4.7%2B-success.svg)](https://github.com/netbox-community/netbox)
[![CI](https://github.com/dansheps/netbox-routing/actions/workflows/ci.yml/badge.svg)](https://github.com/dansheps/netbox-routing/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

A plugin for tracking all kinds of routing information

## Features

### Current features

* **Static routing**
    * Define IPv4 or IPv6 routes for devices, optionally scoped to a VRF.
    * Choose an IP address or an interface as the next hop, and set route metrics, tags, names, or permanence.
* **EIGRP**
    * Model named or traditional routers with process identifiers and router IDs.
    * Organize networks and interfaces by address family and optional VRF; configure interface passivity, BFD, and
      authentication.
* **OSPF**
    * Track device instances with router IDs, process IDs, and optional VRFs, and organize them into typed areas.
    * Assign interfaces to areas and record passive mode, priority, BFD, and authentication settings. Interfaces are
      not restricted to a single IP version.
* **BGP**
    * Define routers and address-family scopes for the default routing table or individual VRFs, then associate peers
      with peer and source addresses and local or remote ASNs.
    * Configure address-family policy with prefix lists and route maps; use peer ("peer groups"), session, and policy
      templates to
      share settings and inherit configuration.
    * Supports IPv4, IPv6, and VPNv4 address families.
* **BFD profiles**
    * Set minimum transmit and receive intervals, a detection multiplier, and an optional hold time. Profiles can be
      assigned to BGP peers and session templates.
* **IS-IS**
    * Configure device instances and optional VRFs, NETs, IS types, metric styles, authentication, timers, overload
      behavior, and traffic-engineering settings.
    * Set interface address families, circuit and network types, metrics, passive mode, hello authentication, and BFD;
      configure additional metrics and timers per level.
    * Manage level-specific metrics and authentication, SR-MPLS settings and prefix SIDs, Flex-Algo constraints, and
      SRv6 locators.

### Roadmapped

* MPLS (LDP and Segment Routing)

# Requirements

* NetBox 4.7+
* Python 3.12+

See the [compatibility matrix](COMPATABILITY.md) for supported NetBox versions by plugin release.

## Installation

Install the Python package:

`pip install netbox-routing`

Enable the plugin in NetBox's plugin configuration:

Example:

```python
PLUGINS = [
    'netbox_routing',
]
```

Once installed, run the migrations:

`python netbox/manage.py migrate`

Run the static collections:

`python netbox/manage.py collectstatic --no-input`

## Usage

After installing and enabling `netbox-routing`, use the **Routing** section in the NetBox UI to manage routing
objects. The plugin also provides REST API endpoints under `/api/plugins/routing/`.

### Migrating from netbox-bgp

`netbox-bgp` is not compatible with `netbox-routing`. To migrate its data, install `netbox-routing`, remove
`netbox-bgp` from the NetBox plugin configuration, and run NetBox's migrations. Then run the built-in migration
command:

`python netbox/manage.py migrate-netbox-bgp`

## Contribute

Contributions are always welcome!  Please open an issue first before contributing as the scope is going to be kept
intentionally narrow


