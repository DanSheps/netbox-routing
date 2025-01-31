from netbox.plugins import PluginMenu

from .bgp import MENUITEMS as BGP_MENU
from .objects import MENUITEMS as OBJECT_MENU
from .ospf import MENUITEMS as OSPF_MENU
from .eigrp import eigrp
from .static import MENUITEMS as STATIC_MENU
from .communities import communities


__all__ = (
    'menu',
)

menu = PluginMenu(
    label='Netbox Routing',
    groups=(
        ('BGP', BGP_MENU),
        ('EIGRP', eigrp),
        ('OSPF', OSPF_MENU),
        ('Static', STATIC_MENU),

        ('Filtering', OBJECT_MENU),
        ('Communities', communities),
    ),
    icon_class='mdi mdi-router'
)