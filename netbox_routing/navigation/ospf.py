from netbox.plugins import PluginMenuButton, PluginMenuItem

__all__ = ('MENUITEMS',)

COL_ADD = 'mdi mdi-plus'
COL_IMPORT = 'mdi mdi-upload'

ospf_instance = PluginMenuItem(
    link='plugins:netbox_routing:ospfinstance_list',
    link_text='Instances',
    permissions=['netbox_routing.view_ospfinstance'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:ospfinstance_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_ospfinstance'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:ospfinstance_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.import_ospfinstance'],
        ),
    ),
)
ospf_area = PluginMenuItem(
    link='plugins:netbox_routing:ospfarea_list',
    link_text='Areas',
    permissions=['netbox_routing.view_ospfarea'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:ospfarea_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_ospfarea'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:ospfarea_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.import_ospfarea'],
        ),
    ),
)
ospf_interfaces = PluginMenuItem(
    link='plugins:netbox_routing:ospfinterface_list',
    link_text='Interfaces',
    permissions=['netbox_routing.view_ospfinterface'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:ospfinterface_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_ospfinterface'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:ospfinterface_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.import_ospfinterface'],
        ),
    ),
)

MENUITEMS = (ospf_instance, ospf_area, ospf_interfaces)
