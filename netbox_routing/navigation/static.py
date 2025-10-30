from netbox.plugins import PluginMenuButton, PluginMenuItem

__all__ = ('MENUITEMS',)

COL_ADD = 'mdi mdi-plus'
COL_IMPORT = 'mdi mdi-upload'

static = PluginMenuItem(
    link='plugins:netbox_routing:staticroute_list',
    link_text='Static Routes',
    permissions=['netbox_routing.view_staticroute'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:staticroute_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_staticroute'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:staticroute_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.import_staticroute'],
        ),
    ),
)

MENUITEMS = (static,)
