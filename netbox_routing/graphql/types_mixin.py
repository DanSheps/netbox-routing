from typing import List, Annotated

import strawberry


class BGPSettingsMixin:
    settings: List[
        Annotated['BGPSettingsType', strawberry.lazy('netbox_routing.graphql.types')]
    ]
