from netbox.choices import ButtonColorChoices
from netbox.plugins import PluginMenuItem, PluginMenuButton


__all__ = (
    'MENUITEMS',
)


router = PluginMenuItem(
    link='plugins:netbox_routing:bgprouter_list',
    link_text='BGP Router',
    permissions=['netbox_routing.view_bgprouter'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:bgprouter_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        #PluginMenuButton('plugins:netbox_routing:bgprouter_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)


scope = PluginMenuItem(
    link='plugins:netbox_routing:bgpscope_list',
    link_text='BGP Scope',
    permissions=['netbox_routing.view_bgpscope'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:bgpscope_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        #PluginMenuButton('plugins:netbox_routing:bgpscope_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)


address_family = PluginMenuItem(
    link='plugins:netbox_routing:bgpaddressfamily_list',
    link_text='BGP Address Family',
    permissions=['netbox_routing.view_bgpaddressfamily'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:bgpaddressfamily_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        #PluginMenuButton('plugins:netbox_routing:bgpaddressfamily_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)

MENUITEMS = (router, scope, address_family, )