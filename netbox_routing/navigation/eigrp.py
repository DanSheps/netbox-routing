from netbox.plugins import PluginMenuItem, PluginMenuButton


__all__ = (
    'eigrp',
)


COL_ADD = 'mdi mdi-plus'
COL_IMPORT = 'mdi mdi-upload'


routers = PluginMenuItem(
    link='plugins:netbox_routing:eigrprouter_list',
    link_text='Routers',
    permissions=['netbox_routing.view_eigrprouter'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:eigrprouter_add', 'Add', COL_ADD),
        PluginMenuButton('plugins:netbox_routing:eigrprouter_bulk_import', 'Import', COL_IMPORT),
    )
)
address_families = PluginMenuItem(
    link='plugins:netbox_routing:eigrpaddressfamily_list',
    link_text='Address Families',
    permissions=['netbox_routing.view_eigrpaddressfamily'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:eigrpaddressfamily_add', 'Add', COL_ADD),
    )
)
networks = PluginMenuItem(
    link='plugins:netbox_routing:eigrpnetwork_list',
    link_text='Networks',
    permissions=['netbox_routing.view_eigrpnetwork'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:eigrpnetwork_add', 'Add', COL_ADD),
    )
)
interfaces = PluginMenuItem(
    link='plugins:netbox_routing:eigrpinterface_list',
    link_text='Interfaces',
    permissions=['netbox_routing.view_eigrpinterface'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:eigrpinterface_add', 'Add', COL_ADD),
    )
)

eigrp = (routers, address_families, networks, interfaces)
