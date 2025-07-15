from netbox.choices import ButtonColorChoices as ColorChoices
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
            'plugins:netbox_routing:prefixlist_add', 'Add', COL_ADD, ColorChoices.GREEN
        ),
        PluginMenuButton(
            'plugins:netbox_routing:prefixlist_bulk_import',
            'Import',
            COL_IMPORT,
            ColorChoices.CYAN,
        ),
    ),
)
routemap = PluginMenuItem(
    link='plugins:netbox_routing:routemap_list',
    link_text='Route Maps',
    permissions=['netbox_routing.view_routemap'],
    buttons=(
        PluginMenuButton(
            'plugins:netbox_routing:routemap_add', 'Add', COL_ADD, ColorChoices.GREEN
        ),
        PluginMenuButton(
            'plugins:netbox_routing:routemap_bulk_import',
            'Import',
            COL_IMPORT,
            ColorChoices.CYAN,
        ),
    ),
)

MENUITEMS = (prefixlist, routemap)
