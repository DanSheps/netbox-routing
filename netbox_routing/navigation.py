from extras.plugins import PluginMenuButton, PluginMenuItem, PluginMenu
from utilities.choices import ButtonColorChoices

static = PluginMenuItem(
    link='plugins:netbox_routing:staticroute_list',
    link_text='Static Route',
    permissions=['netbox_routing.view_staticroute'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:staticroute_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        PluginMenuButton(
            'plugins:netbox_routing:staticroute_import',
            'Import',
            'mdi mdi-upload',
            ButtonColorChoices.CYAN
        ),
    )
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

menu = PluginMenu(
    label='Netbox Routing',
    groups=(
        ('Routing Objects', (prefixlist, routemap)),
        ('Static Routing', (static,)),
        ('OSPF', (ospf_instance, ospf_area, ospf_interfaces)),
    ),
    icon_class='mdi mdi-router'
)
