# SPDX-License-Identifier: Apache-2.0

from netbox.plugins import PluginMenuButton, PluginMenuItem

__all__ = ('MENUITEMS',)

COL_ADD = 'mdi mdi-plus'
COL_IMPORT = 'mdi mdi-upload'

isis_instance = PluginMenuItem(
    link='plugins:netbox_routing:isisinstance_list',
    link_text='Instances',
    permissions=['netbox_routing.view_isisinstance'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:isisinstance_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_isisinstance'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:isisinstance_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.import_isisinstance'],
        ),
    ),
)
isis_interface = PluginMenuItem(
    link='plugins:netbox_routing:isisinterface_list',
    link_text='Interfaces',
    permissions=['netbox_routing.view_isisinterface'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:isisinterface_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_isisinterface'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:isisinterface_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.import_isisinterface'],
        ),
    ),
)

isis_setting = PluginMenuItem(
    link='plugins:netbox_routing:isissetting_list',
    link_text='Settings',
    permissions=['netbox_routing.view_isissetting'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:isissetting_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_isissetting'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:isissetting_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.import_isissetting'],
        ),
    ),
)

isis_level = PluginMenuItem(
    link='plugins:netbox_routing:isislevel_list',
    link_text='Levels',
    permissions=['netbox_routing.view_isislevel'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:isislevel_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_isislevel'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:isislevel_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.import_isislevel'],
        ),
    ),
)
isis_segment_routing = PluginMenuItem(
    link='plugins:netbox_routing:isissegmentrouting_list',
    link_text='Segment Routing',
    permissions=['netbox_routing.view_isissegmentrouting'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:isissegmentrouting_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_isissegmentrouting'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:isissegmentrouting_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.import_isissegmentrouting'],
        ),
    ),
)

isis_flex_algo = PluginMenuItem(
    link='plugins:netbox_routing:isisflexalgo_list',
    link_text='Flex-Algos',
    permissions=['netbox_routing.view_isisflexalgo'],
    buttons=(
        PluginMenuButton(
            link='plugins:netbox_routing:isisflexalgo_add',
            title='Add',
            icon_class=COL_ADD,
            permissions=['netbox_routing.add_isisflexalgo'],
        ),
        PluginMenuButton(
            link='plugins:netbox_routing:isisflexalgo_bulk_import',
            title='Import',
            icon_class=COL_IMPORT,
            permissions=['netbox_routing.import_isisflexalgo'],
        ),
    ),
)

# Primary objects first (instance, interface), then their EAV settings, then the
# per-instance detail tables (level, segment-routing, flex-algo).
MENUITEMS = (
    isis_instance,
    isis_interface,
    isis_setting,
    isis_level,
    isis_segment_routing,
    isis_flex_algo,
)
