from typing import List

import strawberry
import strawberry_django

from .types import *


@strawberry.type(name="Query")
class StaticRouteQuery:
    static_route: StaticRouteType = strawberry_django.field()
    static_route_list: List[StaticRouteType] = strawberry_django.field()


@strawberry.type(name="Query")
class OSPFQuery:
    ospf_instance: OSPFInstanceType = strawberry_django.field()
    ospf_instance_list: List[OSPFInstanceType] = strawberry_django.field()

    ospf_area: OSPFAreaType = strawberry_django.field()
    ospf_area_list: List[OSPFAreaType] = strawberry_django.field()

    ospf_interface: OSPFInterfaceType = strawberry_django.field()
    ospf_interface_list: List[OSPFInterfaceType] = strawberry_django.field()


@strawberry.type(name="Query")
class EIGRPQuery:
    eigrp_router: EIGRPRouterType = strawberry_django.field()
    eigrp_router_list: List[EIGRPRouterType] = strawberry_django.field()

    eigrp_address_family: EIGRPAddressFamilyType = strawberry_django.field()
    eigrp_address_family_list: List[EIGRPAddressFamilyType] = strawberry_django.field()

    eigrp_network: EIGRPNetworkType = strawberry_django.field()
    eigrp_network_list: List[EIGRPNetworkType] = strawberry_django.field()

    eigrp_interface: EIGRPInterfaceType = strawberry_django.field()
    eigrp_interface_list: List[EIGRPInterfaceType] = strawberry_django.field()


schema = [
    StaticRouteQuery,
    OSPFQuery,
    EIGRPQuery,
]
