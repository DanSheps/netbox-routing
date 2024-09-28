from .static import *
from .objects import *
from .ospf import *
from .eigrp import *


__all__ = (
    # Staticroute
    'StaticRouteBulkEditForm',
    
    # OSPF
    'OSPFInstanceBulkEditForm',
    'OSPFInterfaceBulkEditForm',
    'OSPFAreaBulkEditForm',

    # EIGRP
    'EIGRPRouterBulkEditForm',
    'EIGRPAddressFamilyBulkEditForm',
    'EIGRPNetworkBulkEditForm',
    'EIGRPInterfaceBulkEditForm',

    # Route Objects
    'PrefixListEntryBulkEditForm',
    'RouteMapEntryBulkEditForm'
)

