# SPDX-License-Identifier: Apache-2.0

from django.test import SimpleTestCase

from netbox_routing.ui.panels.isis import ISISInstanceSettingsPanel, ISISLevelPanel

__all__ = ('ISISPanelAuthFieldsTestCase',)


class ISISPanelAuthFieldsTestCase(SimpleTestCase):
    """Model-backed IS-IS auth fields must be declared on the detail panels.

    A panel renders only the attributes it collects in `_attrs`; an omitted field means a
    saved authentication value is invisible on the object detail page.
    """

    def test_level_panel_includes_auth_key(self):
        self.assertIn('auth_type', ISISLevelPanel._attrs)
        self.assertIn('auth_key', ISISLevelPanel._attrs)

    def test_instance_settings_panel_includes_area_and_domain_auth(self):
        for name in (
            'area_auth_type',
            'area_auth_key',
            'domain_auth_type',
            'domain_auth_key',
        ):
            with self.subTest(field=name):
                self.assertIn(name, ISISInstanceSettingsPanel._attrs)
