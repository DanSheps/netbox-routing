from netbox.api.viewsets import NetBoxModelViewSet
from netbox_routing import filtersets
from netbox_routing.api.serializers import StaticRouteSerializer
from netbox_routing.models import StaticRoute


class StaticRouteViewSet(NetBoxModelViewSet):
    queryset = StaticRoute.objects.all()
    serializer_class = StaticRouteSerializer
    filterset_class = filtersets.StaticRouteFilterSet
