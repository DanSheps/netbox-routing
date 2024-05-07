from netbox.choices import ButtonColorChoices
from netbox.plugins import PluginMenuItem, PluginMenuButton


__all__ = (
    'MENUITEMS',
)


ospf_instance = PluginMenuItem(
    link='plugins:netbox_routing:ospfinstance_list',
    link_text='Instances',
    permissions=['netbox_routing.view_ospfinstance'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:ospfinstance_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        PluginMenuButton(
            'plugins:netbox_routing:ospfinstance_import',
            'Import',
            'mdi mdi-upload',
            ButtonColorChoices.CYAN
        ),
    )
)
ospf_area = PluginMenuItem(
    link='plugins:netbox_routing:ospfarea_list',
    link_text='Areas',
    permissions=['netbox_routing.view_ospfarea'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:ospfarea_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        PluginMenuButton(
            'plugins:netbox_routing:ospfarea_import',
            'Import',
            'mdi mdi-upload',
            ButtonColorChoices.CYAN
        ),
    )
)
ospf_interfaces = PluginMenuItem(
    link='plugins:netbox_routing:ospfinterface_list',
    link_text='Interfaces',
    permissions=['netbox_routing.view_ospfinterface'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:ospfinterface_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        PluginMenuButton(
            'plugins:netbox_routing:ospfinterface_import',
            'Import',
            'mdi mdi-upload',
            ButtonColorChoices.CYAN
        ),
    )
)

MENUITEMS = (ospf_instance, ospf_area, ospf_interfaces)
