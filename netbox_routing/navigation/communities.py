from netbox.choices import ButtonColorChoices
from netbox.plugins import PluginMenuButton, PluginMenuItem


__all__ = (
    'communities',
)


communitylist = PluginMenuItem(
    link='plugins:netbox_routing:communitylist_list',
    link_text='Community List',
    permissions=['netbox_routing.view_communitylist'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:communitylist_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        PluginMenuButton('plugins:netbox_routing:communitylist_bulk_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)
community = PluginMenuItem(
    link='plugins:netbox_routing:community_list',
    link_text='Community',
    permissions=['netbox_routing.view_community'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:community_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        PluginMenuButton('plugins:netbox_routing:community_bulk_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)

communities = (community, communitylist)
