from django.test import SimpleTestCase

from netbox_routing.tests.community.test_models import *
from netbox_routing.tests.eigrp.test_models import *
from netbox_routing.tests.isis.test_models import *
from netbox_routing.tests.ospf.test_models import *
from netbox_routing.tests.static.test_models import *

__all__ = (
    'StaticRouteTestCase',
    'OSPFInstanceTestCase',
    'OSPFAreaTestCase',
    'OSPFInterfaceTestCase',
    'ISISInstanceModelTestCase',
    'ISISInterfaceModelTestCase',
    'ISISSettingModelTestCase',
    'EIGRPRouterTestCase',
    'EIGRPAddressFamilyTestCase',
    'EIGRPNetworkTestCase',
    'EIGRPInterfaceTestCase',
    'CommunityTestCase',
    'CommunityListTestCase',
    'CommunityListEntryTestCase',
    'AggregateModelTestExportsTestCase',
)


class AggregateModelTestExportsTestCase(SimpleTestCase):
    """Guard that this aggregate re-exports every model TestCase from the submodules
    it wildcard-imports, so ``from netbox_routing.tests.test_models import *`` (used for
    test discovery) cannot silently drop one — e.g. ISISSettingModelTestCase."""

    SUBMODULES = ('community', 'eigrp', 'isis', 'ospf', 'static')

    def test_all_submodule_testcases_reexported(self):
        import importlib

        missing = {}
        for name in self.SUBMODULES:
            sub = importlib.import_module(f'netbox_routing.tests.{name}.test_models')
            for cls_name in getattr(sub, '__all__', ()):
                if cls_name not in __all__:
                    missing.setdefault(name, []).append(cls_name)
        self.assertEqual(
            missing, {}, f'aggregate __all__ omits submodule exports: {missing}'
        )
