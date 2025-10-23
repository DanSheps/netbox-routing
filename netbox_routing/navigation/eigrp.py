from netbox.plugins import PluginMenuButton, PluginMenuItem

__all__ = ('eigrp',)


COL_ADD = 'mdi mdi-plus'
COL_IMPORT = 'mdi mdi-upload'


routers = PluginMenuItem(
    link='plugins:netbox_routing:eigrprouter_list',
    link_text='Routers',
    permissions=['netbox_routing.view_eigrprouter'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:eigrprouter_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_eigrprouter'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:eigrprouter_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.import_eigrprouter'],
        ),
    ),
)
address_families = PluginMenuItem(
    link='plugins:netbox_routing:eigrpaddressfamily_list',
    link_text='Address Families',
    permissions=['netbox_routing.view_eigrpaddressfamily'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:eigrpaddressfamily_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_eigrpaddressfamily'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:eigrpaddressfamily_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.import_eigrpaddressfamily'],
        ),
    ),
)
networks = PluginMenuItem(
    link='plugins:netbox_routing:eigrpnetwork_list',
    link_text='Networks',
    permissions=['netbox_routing.view_eigrpnetwork'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:eigrpnetwork_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_eigrpnetwork'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:eigrpnetwork_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.import_eigrpnetwork'],
        ),
    ),
)
interfaces = PluginMenuItem(
    link='plugins:netbox_routing:eigrpinterface_list',
    link_text='Interfaces',
    permissions=['netbox_routing.view_eigrpinterface'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:eigrpinterface_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_eigrpinterface'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:eigrpinterface_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.import_eigrpinterface'],
        ),
    ),
)

eigrp = (routers, address_families, networks, interfaces)
