from .static import *
from .objects import *
from .ospf import OSPFInterfaceBulkEditForm


__all__ = (
    # Staticroute
    'StaticRouteBulkEditForm',
    
    # OSPF
    'OSPFInterfaceBulkEditForm',

    # Route Objects
    'PrefixListEntryBulkEditForm',
    'RouteMapEntryBulkEditForm'
)

