from .static import StaticRouteFilterForm
from .objects import PrefixListFilterForm, PrefixListEntryFilterForm, RouteMapFilterForm,\
    RouteMapEntryFilterForm
from .ospf import OSPFAreaFilterForm, OSPFInstanceFilterForm, OSPFInterfaceFilterForm

__all__ = (
    # Static
    'StaticRouteFilterForm',

    # OSPF
    'OSPFAreaFilterForm',
    'OSPFInstanceFilterForm',
    'OSPFInterfaceFilterForm',

    # Routing Objects
    'PrefixListFilterForm',
    'PrefixListEntryFilterForm',
    'RouteMapFilterForm',
    'RouteMapEntryFilterForm'
)
