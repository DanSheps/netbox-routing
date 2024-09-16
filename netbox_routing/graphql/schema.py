from typing import List

import strawberry
import strawberry_django

from .types import *


@strawberry.type(name="Query")
class StaticRouteQuery:
    static_route: StaticRouteType = strawberry_django.field()
    static_route_list: List[StaticRouteType] = strawberry_django.field()


schema = [
    StaticRouteQuery,
]
