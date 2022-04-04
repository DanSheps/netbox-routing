from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_routing:staticroute_list',
        link_text='Static Route',
        buttons=(
            PluginMenuButton('plugins:netbox_routing:staticroute_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
            PluginMenuButton('plugins:netbox_routing:staticroute_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
        )
    ),
    PluginMenuItem(
        link='plugins:netbox_routing:prefixlist_list',
        link_text='Prefix Lists',
        buttons=(
            PluginMenuButton('plugins:netbox_routing:prefixlist_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
            PluginMenuButton('plugins:netbox_routing:prefixlist_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
        )
    ),
    PluginMenuItem(
        link='plugins:netbox_routing:routemap_list',
        link_text='Route Maps',
        buttons=(
            PluginMenuButton('plugins:netbox_routing:routemap_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
            PluginMenuButton('plugins:netbox_routing:routemap_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
        )
    ),
)