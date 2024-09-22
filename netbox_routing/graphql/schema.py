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


schema = [
    StaticRouteQuery,
    OSPFQuery
]
