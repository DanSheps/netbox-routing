# SPDX-License-Identifier: Apache-2.0

from django.test import SimpleTestCase

from netbox_routing.ui.panels.isis import (
    ISISInstanceSettingsPanel,
    ISISInterfacePanel,
    ISISInterfaceSettingsPanel,
    ISISLevelPanel,
)

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

    def test_interface_panel_includes_device(self):
        # The interface detail page must show/link the owning device (via
        # instance.device), mirroring the OSPF interface panel — otherwise an
        # operator can't see or click through to the device from an IS-IS interface.
        self.assertIn('device', ISISInterfacePanel._attrs)

    def test_interface_settings_panel_includes_hello_auth(self):
        # hello_auth_type/key are model-backed and render on the interface *settings*
        # panel; assert them so a regression dropping either from the panel (hiding a
        # saved interface authentication value) is caught.
        for name in ('hello_auth_type', 'hello_auth_key'):
            with self.subTest(field=name):
                self.assertIn(name, ISISInterfaceSettingsPanel._attrs)

    def test_interface_settings_panel_includes_bfd_enabled(self):
        # bfd_enabled is a model-backed BooleanField; it must appear on the interface
        # settings panel so the BFD toggle is visible on the detail page, not only in
        # the list view.
        self.assertIn('bfd_enabled', ISISInterfaceSettingsPanel._attrs)
