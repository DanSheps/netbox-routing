from netbox.choices import ButtonColorChoices as ColorChoices
from netbox.plugins import PluginMenuItem, PluginMenuButton


__all__ = (
    'MENUITEMS',
)


ospf_instance = PluginMenuItem(
    link='plugins:netbox_routing:ospfinstance_list',
    link_text='Instances',
    permissions=['netbox_routing.view_ospfinstance'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:ospfinstance_add', 'Add', 'mdi mdi-plus', ColorChoices.GREEN),
        PluginMenuButton(
            'plugins:netbox_routing:ospfinstance_bulk_import',
            'Import',
            'mdi mdi-upload',
            ColorChoices.CYAN
        ),
    )
)
ospf_area = PluginMenuItem(
    link='plugins:netbox_routing:ospfarea_list',
    link_text='Areas',
    permissions=['netbox_routing.view_ospfarea'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:ospfarea_add', 'Add', 'mdi mdi-plus', ColorChoices.GREEN),
        PluginMenuButton('plugins:netbox_routing:ospfarea_bulk_import', 'Import', 'mdi mdi-upload', ColorChoices.CYAN),
    )
)
ospf_interfaces = PluginMenuItem(
    link='plugins:netbox_routing:ospfinterface_list',
    link_text='Interfaces',
    permissions=['netbox_routing.view_ospfinterface'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:ospfinterface_add', 'Add', 'mdi mdi-plus', ColorChoices.GREEN),
        PluginMenuButton(
            'plugins:netbox_routing:ospfinterface_bulk_import',
            'Import',
            'mdi mdi-upload',
            ColorChoices.CYAN
        ),
    )
)

MENUITEMS = (ospf_instance, ospf_area, ospf_interfaces)
