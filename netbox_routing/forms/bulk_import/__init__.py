from .ospf import *
from .eigrp import EIGRPRouterImportForm, EIGRPAddressFamilyImportForm, EIGRPNetworkImportForm, EIGRPInterfaceImportForm
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

