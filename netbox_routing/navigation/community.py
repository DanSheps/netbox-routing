from netbox.plugins import PluginMenuButton, PluginMenuItem

__all__ = ('COMMUNITY_MENU',)


COL_ADD = 'mdi mdi-plus'
COL_IMPORT = 'mdi mdi-upload'


def build_menus():
    menus = []
    menu_items = (
        ('communitylist', 'Community List'),
        ('community', 'Community'),
        ('communitylistentry', 'Community List Entry'),
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


COMMUNITY_MENU = build_menus()
