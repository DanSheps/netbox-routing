from .ospf import *
from .eigrp import *
from .static import *

__all__ = (
    # Static
    'StaticRouteImportForm',
    # OSPF
    'OSPFInstanceImportForm',
    'OSPFAreaImportForm',
    'OSPFInterfaceImportForm',
    # EIGRP
    'EIGRPRouterImportForm',
    'EIGRPAddressFamilyImportForm',
    'EIGRPNetworkImportForm',
    'EIGRPInterfaceImportForm',
)
