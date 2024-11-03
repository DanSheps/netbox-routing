from netbox.choices import ButtonColorChoices
from netbox.plugins import PluginMenuItem, PluginMenuButton


__all__ = (
    'MENUITEMS',
)


router = PluginMenuItem(
    link='plugins:netbox_routing:bgprouter_list',
    link_text='Router',
    permissions=['netbox_routing.view_bgprouter'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:bgprouter_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        #PluginMenuButton('plugins:netbox_routing:bgprouter_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)


scope = PluginMenuItem(
    link='plugins:netbox_routing:bgpscope_list',
    link_text='Scope',
    permissions=['netbox_routing.view_bgpscope'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:bgpscope_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        #PluginMenuButton('plugins:netbox_routing:bgpscope_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)


session_template = PluginMenuItem(
    link='plugins:netbox_routing:bgpsessiontemplate_list',
    link_text='Session Template',
    permissions=['netbox_routing.view_bgpsessiontemplate'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:bgpsessiontemplate_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        #PluginMenuButton('plugins:netbox_routing:bgpscope_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)


policy_template = PluginMenuItem(
    link='plugins:netbox_routing:bgppolicytemplate_list',
    link_text='Policy Template',
    permissions=['netbox_routing.view_bgppolicytemplate'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:bgppolicytemplate_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        #PluginMenuButton('plugins:netbox_routing:bgpscope_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)


peer_template = PluginMenuItem(
    link='plugins:netbox_routing:bgppeertemplate_list',
    link_text='Peer Template',
    permissions=['netbox_routing.view_bgppeertemplate'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:bgppeertemplate_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        #PluginMenuButton('plugins:netbox_routing:bgpscope_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)


address_family = PluginMenuItem(
    link='plugins:netbox_routing:bgpaddressfamily_list',
    link_text='Address Family',
    permissions=['netbox_routing.view_bgpaddressfamily'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:bgpaddressfamily_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        #PluginMenuButton('plugins:netbox_routing:bgpaddressfamily_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)


peer = PluginMenuItem(
    link='plugins:netbox_routing:bgppeer_list',
    link_text='Peer',
    permissions=['netbox_routing.view_bgppeer'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:bgppeer_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        #PluginMenuButton('plugins:netbox_routing:bgpscope_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)


peer_af = PluginMenuItem(
    link='plugins:netbox_routing:bgppeeraddressfamily_list',
    link_text='Peer Address Families',
    permissions=['netbox_routing.view_bgppeeraddressfamily'],
    buttons=(
        PluginMenuButton('plugins:netbox_routing:bgppeeraddressfamily_add', 'Add', 'mdi mdi-plus', ButtonColorChoices.GREEN),
        #PluginMenuButton('plugins:netbox_routing:bgpscope_import', 'Import', 'mdi mdi-upload', ButtonColorChoices.CYAN),
    )
)

MENUITEMS = (router, scope, session_template, policy_template, peer_template, address_family, peer, peer_af, )
