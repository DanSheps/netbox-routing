from netbox.choices import ButtonColorChoices as ColorChoices
from netbox.plugins import PluginMenuItem, PluginMenuButton

__all__ = (
    'MENUITEMS',
)

static = PluginMenuItem(
    link='plugins:netbox_routing:staticroute_list',
    link_text='Static Route',
    permissions=['netbox_routing.view_staticroute'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:staticroute_add', 'Add', 'mdi mdi-plus', ColorChoices.GREEN),
        # PluginMenuButton(
        #    'plugins:netbox_routing:staticroute_bulk_import',
        #    'Import',
        #    'mdi mdi-upload',
        #    ColorChoices.CYAN
        # ),

    )
)

MENUITEMS = (static,)
