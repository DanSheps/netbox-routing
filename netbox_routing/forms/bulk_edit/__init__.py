from .static import *
from .objects import *
from .ospf import *


__all__ = (
    # Staticroute
    'StaticRouteBulkEditForm',
    
    # OSPF
    'OSPFInstanceBulkEditForm',
    'OSPFInterfaceBulkEditForm',
    'OSPFAreaBulkEditForm',

    # Route Objects
    'PrefixListEntryBulkEditForm',
    'RouteMapEntryBulkEditForm'
)

