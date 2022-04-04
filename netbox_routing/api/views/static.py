from netbox.api.viewsets import ModelViewSet
from netbox_routing.api.serializers import StaticRouteSerializer
from netbox_routing.models import StaticRoute


class StaticRouteViewSet(ModelViewSet):
    queryset = StaticRoute.objects.all()
    serializer_class = StaticRouteSerializer
