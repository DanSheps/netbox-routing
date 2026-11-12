# SPDX-License-Identifier: Apache-2.0

from django.test import SimpleTestCase

from netbox_routing.navigation.isis import MENUITEMS

__all__ = ('ISISNavigationTestCase',)


class ISISNavigationTestCase(SimpleTestCase):
    """The IS-IS menu is built by build_menus() over (model, label) rows.

    Guards the full set of menu items and that the Import button is gated by the real
    ``add`` permission, not a non-existent ``import_*`` one (a wrong slug is invisible
    against five lookalike menu blocks — the bug the loop replaces).
    """

    EXPECTED_MODELS = (
        'isisinstance',
        'isisinterface',
        'isissetting',
        'isislevel',
        'isissegmentrouting',
        'isisflexalgo',
        'isisprefixsid',
        'isissrv6locator',
    )

    def test_menu_items_cover_all_isis_models(self):
        links = {item.link for item in MENUITEMS}
        self.assertEqual(
            links,
            {f'plugins:netbox_routing:{m}_list' for m in self.EXPECTED_MODELS},
        )

    def test_import_button_uses_add_permission(self):
        for item in MENUITEMS:
            model = item.link.split(':')[-1].removesuffix('_list')
            import_buttons = [b for b in item.buttons if b.link.endswith('_bulk_import')]
            with self.subTest(model=model):
                self.assertEqual(len(import_buttons), 1)
                self.assertEqual(
                    list(import_buttons[0].permissions),
                    [f'netbox_routing.add_{model}'],
                )
