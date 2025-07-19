from netbox.plugins import PluginMenu
from netbox.plugins.utils import get_plugin_config

# from .bgp import MENUITEMS as BGP_MENU
# from .objects import MENUITEMS as OBJECT_MENU
from .ospf import MENUITEMS as OSPF_MENU
from .eigrp import eigrp
from .static import MENUITEMS as STATIC_MENU


__all__ = (
    'menu',
)

menu = PluginMenu(
    label=get_plugin_config('netbox_routing', 'menu_name'),
    groups=(
        # ('Routing Objects', OBJECT_MENU),
        ('Static', STATIC_MENU),
        # ('BGP', BGP_MENU),
        ('OSPF', OSPF_MENU),
        ('EIGRP', eigrp),
    ),
    icon_class='mdi mdi-router'
)
