from netbox.choices import ButtonColorChoices
from netbox.plugins import PluginMenuItem, PluginMenuButton


__all__ = (
    'eigrp',
)


routers = PluginMenuItem(
    link='plugins:netbox_routing:eigrprouter_list',
    link_text='Routers',
    permissions=['netbox_routing.view_eigrprouter'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:eigrprouter_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        PluginMenuButton(
            'plugins:netbox_routing:eigrprouter_import',
            'Import',
            'mdi mdi-upload',
            ButtonColorChoices.CYAN
        ),
    )
)
address_families = PluginMenuItem(
    link='plugins:netbox_routing:eigrpaddressfamily_list',
    link_text='Address Families',
    permissions=['netbox_routing.view_eigrpaddressfamily'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:eigrpaddressfamily_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
    )
)
networks = PluginMenuItem(
    link='plugins:netbox_routing:eigrpnetwork_list',
    link_text='Networks',
    permissions=['netbox_routing.view_eigrpnetwork'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:eigrpnetwork_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
    )
)
interfaces = PluginMenuItem(
    link='plugins:netbox_routing:eigrpinterface_list',
    link_text='Interfaces',
    permissions=['netbox_routing.view_eigrpinterface'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:eigrpinterface_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
    )
)

eigrp = (routers, address_families, networks, interfaces)
