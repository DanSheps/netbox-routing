from netbox_routing.forms.bulk_edit.bgp import *
from netbox_routing.forms.bulk_import.bgp import *
from netbox_routing.forms.filtersets.bgp import *
from netbox_routing.forms.model_objects.bgp import *


__all__ = (
    # Object Edit Forms
    'BGPSettingForm',
    'BGPRouterForm',
    'BGPScopeForm',
    'BGPAddressFamilyForm',
    'BGPPeerTemplateForm',
    'BGPPolicyTemplateForm',
    'BGPSessionTemplateForm',
    'BGPPeerForm',
    'BGPPeerAddressFamilyForm',

    'BGPRouterImportForm',
    'BGPScopeImportForm',
    'BGPAddressFamilyImportForm',
    'BGPPeerTemplateImportForm',
    'BGPPolicyTemplateImportForm',
    'BGPSessionTemplateImportForm',
    'BGPPeerImportForm',
    'BGPPeerAddressFamilyImportForm',

    'BGPRouterBulkEditForm',
    'BGPScopeBulkEditForm',
    'BGPAddressFamilyBulkEditForm',
    'BGPPeerTemplateBulkEditForm',
    'BGPPolicyTemplateBulkEditForm',
    'BGPSessionTemplateBulkEditForm',
    'BGPPeerBulkEditForm',
    'BGPPeerAddressFamilyBulkEditForm',

    # FilterSets
    'BGPRouterFilterForm',
    'BGPScopeFilterForm',
    'BGPSessionTemplateFilterForm',
    'BGPPolicyTemplateFilterForm',
    'BGPPeerTemplateFilterForm',
    'BGPAddressFamilyFilterForm',
    'BGPPeerFilterForm',
    'BGPPeerAddressFamilyFilterForm',
    'BGPSettingFilterForm',
)


