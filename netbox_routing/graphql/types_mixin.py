from typing import Annotated

import strawberry


class BGPSettingsMixin:
    settings: list[
        Annotated['BGPSettingsType', strawberry.lazy('netbox_routing.graphql.types')]
    ]
