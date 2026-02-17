from netbox.plugins import PluginMenuButton, PluginMenuItem

__all__ = ('OBJECT_MENU',)


COL_ADD = 'mdi mdi-plus'
COL_IMPORT = 'mdi mdi-upload'


customprefix = PluginMenuItem(
    link='plugins:netbox_routing:customprefix_list',
    link_text='Custom Prefixes',
    permissions=['netbox_routing.view_customprefix'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:customprefix_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_customprefix'],
        ),
    ),
)
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
        # PluginMenuButton(
        #     link='plugins:netbox_routing:prefixlist_bulk_import',
        #     title='Import',
        #     icon_class=COL_IMPORT,
        #     permissions=['netbox_routing.add_prefixlist'],
        # ),
    ),
)
prefixlist_entry = PluginMenuItem(
    link='plugins:netbox_routing:prefixlistentry_list',
    link_text='Prefix List Entries',
    permissions=['netbox_routing.view_prefixlistentry'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:prefixlistentry_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_prefixlistentry'],
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
    ),
)
routemap_entry = PluginMenuItem(
    link='plugins:netbox_routing:routemapentry_list',
    link_text='Route Map Entries',
    permissions=['netbox_routing.view_routemapentry'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:routemapentry_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_routemapentry'],
        ),
    ),
)
aspath = PluginMenuItem(
    link='plugins:netbox_routing:aspath_list',
    link_text='AS Path',
    permissions=['netbox_routing.view_aspath'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:aspath_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_aspath'],
        ),
    ),
)
aspath_entry = PluginMenuItem(
    link='plugins:netbox_routing:aspathentry_list',
    link_text='AS Path Entries',
    permissions=['netbox_routing.view_aspathentry'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:aspathentry_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_aspathentry'],
        ),
        # PluginMenuButton(
        #     link='plugins:netbox_routing:aspathentry_bulk_import',
        #     title='Import',
        #     icon_class=COL_IMPORT,
        #     permissions=['netbox_routing.add_aspathentry'],
        # ),
    ),
)

OBJECT_MENU = (
    customprefix,
    prefixlist,
    prefixlist_entry,
    routemap,
    routemap_entry,
    aspath,
    aspath_entry,
)
