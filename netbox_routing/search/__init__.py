from .static import StaticRouteIndex
from .ospf import OSPFInstanceIndex, OSPFAreaIndex
from .eigrp import EIGRPRouterIndex, EIGRPAddressFamilyIndex

__all__ = (
    'StaticRouteIndex',

    'OSPFInstanceIndex',
    'OSPFAreaIndex',

    'EIGRPRouterIndex',
    'EIGRPAddressFamilyIndex'
)
