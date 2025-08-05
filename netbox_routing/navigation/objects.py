from netbox.choices import ButtonColorChoices
from netbox.plugins import PluginMenuButton, PluginMenuItem


__all__ = (
    'MENUITEMS',
)


prefixlist = PluginMenuItem(
    link='plugins:netbox_routing:prefixlist_list',
    link_text='Prefix Lists',
    permissions=['netbox_routing.view_prefixlist'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:prefixlist_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        PluginMenuButton('plugins:netbox_routing:prefixlist_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)
routemap = PluginMenuItem(
    link='plugins:netbox_routing:routemap_list',
    link_text='Route Maps',
    permissions=['netbox_routing.view_routemap'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:routemap_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        PluginMenuButton('plugins:netbox_routing:routemap_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)

MENUITEMS = (prefixlist, routemap)
