from netbox.plugins import PluginMenuItem, PluginMenuButton

__all__ = (
    'MENUITEMS',
)

static = PluginMenuItem(
    link='plugins:netbox_routing:staticroute_list',
    link_text='Static Route',
    permissions=['netbox_routing.view_staticroute'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:staticroute_add', 'Add', 'mdi mdi-plus'),
        # PluginMenuButton(
        #    'plugins:netbox_routing:staticroute_bulk_import',
        #    'Import',
        #    'mdi mdi-upload',
        # ),

    )
)

MENUITEMS = (static,)
