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

### setup.py
```python
from setuptools import find_packages, setup

setup(
    name='netbox-plugin-extensions',
    version='1.0.6',
    description='NetBox Plugin Extensions',
    long_description='Wrappers for Netbox Generic Objects',
    url='https://github.com/dansheps/netbox-plugin-extensions/',
    download_url='https://pypi.org/project/netbox-plugin-extensions/',
    author='Daniel Sheppard',
    author_email='dans@dansheps.com',
    maintainer='Daniel Sheppard',
    maintainer_email='dans@dansheps.com',
    license='All rights reserved',
    platform=[],
    keywords=['netbox', 'netbox-plugin'],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'importlib',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
```

### __init__.py
```python
from extras.plugins import PluginConfig


try:
    from importlib.metadata import metadata
except ModuleNotFoundError:
    from importlib_metadata import metadata

plugin = metadata('netbox_plugin_extensions')


class NetboxPluginExtensions(PluginConfig):
    name = plugin.get('Name').replace('-', '_')
    verbose_name = plugin.get('Summary')
    description = plugin.get('Description')
    version = plugin.get('Version')
    author = plugin.get('Author')
    author_email = plugin.get('Author-email')
    base_url = 'netbox-plugin-extensions'
    min_version = '3.0'
    required_settings = []
    caching_config = {}
    default_settings = {}


config = NetboxPluginExtensions

```

## Contribute

Contributions are always welcome!  Please open an issue first before contributing as the scope is going to be kept
intentionally narrow


