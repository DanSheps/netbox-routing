from netbox.views.generic import (
    ObjectView,
    ObjectEditView,
    ObjectListView,
    ObjectDeleteView,
)
from netbox_routing.filtersets import (
    BGPRouterFilterSet,
    BGPScopeFilterSet,
    BGPAddressFamilyFilterSet,
)
from netbox_routing.forms import (
    BGPRouterForm,
    BGPScopeForm,
    BGPRouterFilterForm,
    BGPAddressFamilyForm,
    BGPScopeFilterForm,
    BGPAddressFamilyFilterForm,
)
from netbox_routing.models import BGPRouter, BGPScope, BGPAddressFamily
from netbox_routing.tables.bgp import (
    BGPRouterTable,
    BGPScopeTable,
    BGPAddressFamilyTable,
)
from utilities.views import register_model_view


__all__ = (
    'BGPRouterListView',
    'BGPRouterView',
    'BGPRouterEditView',
    'BGPRouterDeleteView',
    'BGPScopeListView',
    'BGPScopeView',
    'BGPScopeEditView',
    'BGPScopeDeleteView',
    'BGPAddressFamilyListView',
    'BGPAddressFamilyView',
    'BGPAddressFamilyEditView',
    'BGPAddressFamilyDeleteView',
)


#
# BGP Router Views
#
@register_model_view(BGPRouter, name='list', path='', detail=False)
class BGPRouterListView(ObjectListView):
    queryset = BGPRouter.objects.all()
    table = BGPRouterTable
    filterset = BGPRouterFilterSet
    filterset_form = BGPRouterFilterForm


@register_model_view(BGPRouter)
class BGPRouterView(ObjectView):
    queryset = BGPRouter.objects.all()
    template_name = 'netbox_routing/bgprouter.html'


@register_model_view(BGPRouter, name='add', detail=False)
@register_model_view(BGPRouter, name='edit')
class BGPRouterEditView(ObjectEditView):
    queryset = BGPRouter.objects.all()
    form = BGPRouterForm


@register_model_view(BGPRouter, name='delete')
class BGPRouterDeleteView(ObjectDeleteView):
    queryset = BGPRouter.objects.all()


#
# BGP Scope Views
#
@register_model_view(BGPScope, name='list', path='', detail=False)
class BGPScopeListView(ObjectListView):
    queryset = BGPScope.objects.all()
    table = BGPScopeTable
    filterset = BGPScopeFilterSet
    filterset_form = BGPScopeFilterForm


@register_model_view(BGPScope)
class BGPScopeView(ObjectView):
    queryset = BGPScope.objects.all()
    template_name = 'netbox_routing/bgpscope.html'


@register_model_view(BGPScope, name='add', detail=False)
@register_model_view(BGPScope, name='edit')
class BGPScopeEditView(ObjectEditView):
    queryset = BGPScope.objects.all()
    form = BGPScopeForm


@register_model_view(BGPScope, name='delete')
class BGPScopeDeleteView(ObjectDeleteView):
    queryset = BGPScope.objects.all()


#
# BGP Scope Views
#
@register_model_view(BGPAddressFamily, name='list', path='', detail=False)
class BGPAddressFamilyListView(ObjectListView):
    queryset = BGPAddressFamily.objects.all()
    table = BGPAddressFamilyTable
    filterset = BGPAddressFamilyFilterSet
    filterset_form = BGPAddressFamilyFilterForm


@register_model_view(BGPAddressFamily)
class BGPAddressFamilyView(ObjectView):
    queryset = BGPAddressFamily.objects.all()
    template_name = 'netbox_routing/bgpaddressfamily.html'


@register_model_view(BGPAddressFamily, name='add', detail=False)
@register_model_view(BGPAddressFamily, name='edit')
class BGPAddressFamilyEditView(ObjectEditView):
    queryset = BGPAddressFamily.objects.all()
    form = BGPAddressFamilyForm


@register_model_view(BGPAddressFamily, name='delete')
class BGPAddressFamilyDeleteView(ObjectDeleteView):
    queryset = BGPAddressFamily.objects.all()
