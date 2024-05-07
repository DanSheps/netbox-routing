from netbox.plugins import PluginConfig
from importlib.metadata import metadata


plugin = metadata('netbox_routing')


class NetboxRouting(PluginConfig):
    name = plugin.get('Name').replace('-', '_')
    verbose_name = plugin.get('Summary')
    description = plugin.get('Description')
    version = plugin.get('Version')
    author = plugin.get('Author')
    author_email = plugin.get('Author-email')
    base_url = 'routing'
    min_version = '3.5.0'
    required_settings = []
    caching_config = {}
    default_settings = {}


config = NetboxRouting
