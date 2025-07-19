from netbox.plugins import PluginMenuItem, PluginMenuButton


__all__ = (
    'MENUITEMS',
)


COL_ADD = 'mdi mdi-plus'
COL_IMPORT = 'mdi mdi-upload'


router = PluginMenuItem(
    link='plugins:netbox_routing:bgprouter_list',
    link_text='BGP Router',
    permissions=['netbox_routing.view_bgprouter'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:bgprouter_add', 'Add', COL_ADD),
        # PluginMenuButton('plugins:netbox_routing:bgprouter_bulk_import', 'Import', COL_IMPORT),
    )
)


scope = PluginMenuItem(
    link='plugins:netbox_routing:bgpscope_list',
    link_text='BGP Scope',
    permissions=['netbox_routing.view_bgpscope'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:bgpscope_add', 'Add', COL_ADD),
        # PluginMenuButton('plugins:netbox_routing:bgpscope_bulk_import', 'Import', COL_IMPORT),
    )
)


address_family = PluginMenuItem(
    link='plugins:netbox_routing:bgpaddressfamily_list',
    link_text='BGP Address Family',
    permissions=['netbox_routing.view_bgpaddressfamily'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:bgpaddressfamily_add', 'Add', COL_ADD),
        # PluginMenuButton('plugins:netbox_routing:bgpaf_bulk_import', 'Import', COL_IMPORT),
    )
)

MENUITEMS = (router, scope, address_family, )
