from netbox.plugins import PluginConfig
from importlib.metadata import metadata


plugin = metadata('netbox_routing')


class NetboxRouting(PluginConfig):
    name = plugin.get('Name').replace('-', '_')
    verbose_name = plugin.get('Name').replace('-', ' ').title()
    description = plugin.get('Summary')
    version = plugin.get('Version')
    author = plugin.get('Author')
    author_email = plugin.get('Author-email')
    base_url = 'routing'
    min_version = '4.5.0'
    required_settings = []
    caching_config = {}
    default_settings = {}
    graphql_schema = 'graphql.schema.schema'

    def ready(self):
        super().ready()
        from netbox_routing.templatetags.entries import get_entry_url  # noqa: F401

        from netbox_routing.fields.generic import NetBoxGenericRelation
        from dcim.models import Region, SiteGroup, Site, Location, Device
        from virtualization.models import ClusterGroup, Cluster, VirtualMachine
        from netbox_routing.models import BGPRouter

        # Add Generic Relations to appropriate models
        models = (
            ('region', Region),
            ('site_group', SiteGroup),
            ('site', Site),
            ('location', Location),
            ('device', Device),
            ('cluster_group', ClusterGroup),
            ('cluster', Cluster),
            ('virtual_machine', VirtualMachine),
        )
        for name, model in models:
            NetBoxGenericRelation(
                to=BGPRouter,
                content_type_field='assigned_object_type',
                object_id_field='assigned_object_id',
                related_name=name,
                related_query_name=name,
            ).contribute_to_class(model, 'bgp_router')


config = NetboxRouting
