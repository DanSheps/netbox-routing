from netbox.plugins import PluginMenuButton, PluginMenuItem

__all__ = ('MENUITEMS',)


COL_ADD = 'mdi mdi-plus'
COL_IMPORT = 'mdi mdi-upload'


prefixlist = PluginMenuItem(
    link='plugins:netbox_routing:prefixlist_list',
    link_text='Prefix Lists',
    permissions=['netbox_routing.view_prefixlist'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:prefixlist_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_prefixlist'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:prefixlist_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.add_prefixlist'],
        ),
    ),
)
routemap = PluginMenuItem(
    link='plugins:netbox_routing:routemap_list',
    link_text='Route Maps',
    permissions=['netbox_routing.view_routemap'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:routemap_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_routemap'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:routemap_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.add_routemap'],
        ),
    ),
)

MENUITEMS = (prefixlist, routemap)
