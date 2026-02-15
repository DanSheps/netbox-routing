from .static import *
from .objects import *
from .ospf import *
from .eigrp import *
from .bgp import *

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
    'RouteMapEntryBulkEditForm',
    'ASPathBulkEditForm',
    'ASPathEntryBulkEditForm',
    # BFD
    'BFDProfileBulkEditForm',
    # BGP
    'BGPPeerTemplateBulkEditForm',
    'BGPPolicyTemplateBulkEditForm',
    'BGPSessionTemplateBulkEditForm',
    'BGPRouterBulkEditForm',
    'BGPScopeBulkEditForm',
    'BGPAddressFamilyBulkEditForm',
    'BGPPeerBulkEditForm',
    'BGPPeerAddressFamilyBulkEditForm',
    'BGPSettingBulkEditForm',
)
