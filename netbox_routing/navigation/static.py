from netbox.plugins import PluginMenuButton, PluginMenuItem

__all__ = ('MENUITEMS',)

static = PluginMenuItem(
    link='plugins:netbox_routing:staticroute_list',
    link_text='Static Route',
    permissions=['netbox_routing.view_staticroute'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:staticroute_add',
            title='Add',
            icon_class='mdi mdi-plus',
            permissions=['netbox_routing.add_staticroute'],
        ),
        # PluginMenuButton(
        #    'plugins:netbox_routing:staticroute_bulk_import',
        #    'Import',
        #    'mdi mdi-upload',
        # ),
    ),
)

MENUITEMS = (static,)
