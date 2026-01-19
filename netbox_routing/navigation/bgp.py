from netbox.plugins import PluginMenuButton, PluginMenuItem

__all__ = ('BGP_MENU',)


COL_ADD = 'mdi mdi-plus'
COL_IMPORT = 'mdi mdi-upload'


def build_menus():
    menus = []
    menu_items = (
        ('bgpsetting', 'Settings'),
        ('bgprouter', 'Routers'),
        ('bgpscope', 'Scopes'),
        ('bgpaddressfamily', 'Address Families'),
        ('bgppeer', 'Peers'),
        ('bgppeeraddressfamily', 'Peer Address Families'),
    )
    for model, name in menu_items:
        menu = PluginMenuItem(
            link=f'plugins:netbox_routing:{model}_list',
            link_text=f'{name}',
            permissions=[f'netbox_routing.view_{model}'],
            buttons=(
                PluginMenuButton(
                    link=f'plugins:netbox_routing:{model}_add',
                    title='Add',
                    icon_class=COL_ADD,
                    permissions=[f'netbox_routing.add_{model}'],
                ),
                # PluginMenuButton('plugins:netbox_routing:bgprouter_bulk_import', 'Import', COL_IMPORT),
            ),
        )
        menus.append(menu)

    return tuple(menus)


BGP_MENU = build_menus()
