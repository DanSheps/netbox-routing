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

* Netbox 4.5+
* Python 3.12+

## Compatibility Matrix

|       | Netbox 3.2.x   | NetBox 4.1.x   | Netbox 4.2.x   | NetBox 4.3.x - 4.4.x | NetBox 4.5.x   |  
|-------|----------------|----------------|----------------|----------------------|----------------|
| 0.1.x | Compatible     | Not Compatible | Not Compatible | Not Compatible       | Not Compatible |
| 0.2.x | Not Compatible | Compatible     | Not Compatible | Not Compatible       | Not Compatible |
| 0.3.0 | Not Compatible | Not Compatible | Compatible     | Not Compatible       | Not Compatible |
| 0.3.1 | Not Compatible | Not Compatible | Not Compatible | Compatible           | Not Compatible |
| 0.3.2 | Not Compatible | Not Compatible | Not Compatible | Not Compatible       | Compatible     |

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


