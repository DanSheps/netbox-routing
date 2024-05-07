from netbox.plugins import PluginMenu

from .bgp import MENUITEMS as BGP_MENU
from .objects import MENUITEMS as OBJECT_MENU
from .ospf import MENUITEMS as OSPF_MENU
from .static import MENUITEMS as STATIC_MENU


__all__ = (
    'menu',
)

menu = PluginMenu(
    label='Netbox Routing',
    groups=(
        # ('Routing Objects', OBJECT_MENU),
        ('Static', STATIC_MENU),
        # ('BGP', BGP_MENU),
        ('OSPF', OSPF_MENU),
    ),
    icon_class='mdi mdi-router'
)