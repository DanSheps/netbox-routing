from netbox.choices import ButtonColorChoices
from netbox.plugins import PluginMenuButton, PluginMenuItem


__all__ = (
    'MENUITEMS',
)


prefixlist = PluginMenuItem(
    link='plugins:netbox_routing:prefixlist_list',
    link_text='Prefix List',
    permissions=['netbox_routing.view_prefixlist'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:prefixlist_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        # PluginMenuButton('plugins:netbox_routing:prefixlist_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)
prefixlistentry = PluginMenuItem(
    link='plugins:netbox_routing:prefixlistentry_list',
    link_text='Prefix List Entry',
    permissions=['netbox_routing.view_prefixlistentry'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:prefixlistentry_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        # PluginMenuButton('plugins:netbox_routing:prefixlistentry_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)
routemap = PluginMenuItem(
    link='plugins:netbox_routing:routemap_list',
    link_text='Route Map',
    permissions=['netbox_routing.view_routemap'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:routemap_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        # PluginMenuButton('plugins:netbox_routing:routemap_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)
routemapentry = PluginMenuItem(
    link='plugins:netbox_routing:routemapentry_list',
    link_text='Route Map Entry',
    permissions=['netbox_routing.view_routemapentry'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:routemapentry_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        # PluginMenuButton('plugins:netbox_routing:routemapentry_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)

MENUITEMS = (prefixlist, prefixlistentry, routemap, routemapentry)
