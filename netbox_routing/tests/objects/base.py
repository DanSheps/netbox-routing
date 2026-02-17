from netbox_routing.models.objects import *

__all__ = (
    'ParentObjectMixin',
    'ASPathMixin',
    'PrefixListMixin',
    'RouteMapMixin',
)


class ParentObjectMixin:
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()


class ASPathMixin:
    @classmethod
    def setUpTestData(cls):
        cls.aspath = ASPath.objects.create(name=f'{ASPath._meta.verbose_name}')


class PrefixListMixin:
    @classmethod
    def setUpTestData(cls):
        cls.prefix_list = PrefixList.objects.create(
            name=f'{PrefixList._meta.verbose_name}'
        )


class RouteMapMixin:
    @classmethod
    def setUpTestData(cls):
        cls.route_map = RouteMap.objects.create(name=f'{RouteMap._meta.verbose_name}')
