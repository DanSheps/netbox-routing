# Netbox Routing
A plugin for tracking all kinds of routing information

## Features

### Current features

* Static routing

### Under development

* Dynamic routing
  * BGP
    * Templates/Group inheritance
  * OSPF

### Roadmapped

* Dynamic Routing
  * BGP
    * IPv4/IPv46 AF VRF support
    * VPNv4 support
  * EIGRP
  * IS-IS

# Requirements

* Netbox 3.2+
* Python 3.8+

## Compatibility Matrix

|       | Netbox 3.2.x | 
|-------|--------------|
| 1.0.0 | X            |

## Installation

To install, simply include this plugin in the plugins configuration section of netbox.

Example:
```python
    PLUGINS = [
        'netbox_routing'
    ],
```

## Configuration

None

## Usage

TBD

## Additional Notes

TBD

## Contribute

Contributions are always welcome!  Please open an issue first before contributing as the scope is going to be kept
intentionally narrow


