from django.test import TestCase

__all__ = ()


class URLTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.patterns = sorted(
            [
                'staticroute_list',
                'staticroute_add',
                'staticroute_bulk_edit',
                'staticroute_bulk_delete',
                'staticroute_bulk_import',
                'staticroute',
                'staticroute_edit',
                'staticroute_devices',
                'staticroute_delete',
                'staticroute_changelog',
                'staticroute_journal',
                'ospfinstance_list',
                'ospfinstance_add',
                'ospfinstance_bulk_edit',
                'ospfinstance_bulk_delete',
                'ospfinstance_bulk_import',
                'ospfinstance',
                'ospfinstance_edit',
                'ospfinstance_interfaces',
                'ospfinstance_delete',
                'ospfinstance_changelog',
                'ospfinstance_journal',
                'ospfarea_list',
                'ospfarea_add',
                'ospfarea_bulk_edit',
                'ospfarea_bulk_delete',
                'ospfarea_bulk_import',
                'ospfarea',
                'ospfarea_edit',
                'ospfarea_interfaces',
                'ospfarea_delete',
                'ospfarea_changelog',
                'ospfarea_journal',
                'ospfinterface_list',
                'ospfinterface_add',
                'ospfinterface_bulk_edit',
                'ospfinterface_bulk_delete',
                'ospfinterface_bulk_import',
                'ospfinterface',
                'ospfinterface_edit',
                'ospfinterface_delete',
                'ospfinterface_changelog',
                'ospfinterface_journal',
                'eigrprouter_list',
                'eigrprouter_add',
                'eigrprouter_bulk_edit',
                'eigrprouter_bulk_delete',
                'eigrprouter_bulk_import',
                'eigrprouter_journal',
                'eigrprouter_changelog',
                'eigrprouter_list',
                'eigrprouter',
                'eigrprouter_address_families',
                'eigrprouter_interfaces',
                'eigrprouter_networks',
                'eigrprouter_edit',
                'eigrprouter_delete',
                'eigrpaddressfamily_list',
                'eigrpaddressfamily_add',
                'eigrpaddressfamily_bulk_edit',
                'eigrpaddressfamily_bulk_delete',
                'eigrpaddressfamily_bulk_import',
                'eigrpaddressfamily_journal',
                'eigrpaddressfamily_changelog',
                'eigrpaddressfamily_list',
                'eigrpaddressfamily',
                'eigrpaddressfamily_interfaces',
                'eigrpaddressfamily_networks',
                'eigrpaddressfamily_edit',
                'eigrpaddressfamily_delete',
                'eigrpnetwork_list',
                'eigrpnetwork_add',
                'eigrpnetwork_bulk_edit',
                'eigrpnetwork_bulk_delete',
                'eigrpnetwork_bulk_import',
                'eigrpnetwork_journal',
                'eigrpnetwork_changelog',
                'eigrpnetwork_list',
                'eigrpnetwork',
                'eigrpnetwork_edit',
                'eigrpnetwork_delete',
                'eigrpinterface_list',
                'eigrpinterface_add',
                'eigrpinterface_bulk_edit',
                'eigrpinterface_bulk_delete',
                'eigrpinterface_bulk_import',
                'eigrpinterface_journal',
                'eigrpinterface_changelog',
                'eigrpinterface_list',
                'eigrpinterface',
                'eigrpinterface_edit',
                'eigrpinterface_delete',
                'bgprouter_list',
                'bgprouter_add',
                'bgprouter',
                'bgprouter_edit',
                'bgprouter_delete',
                'bgprouter_changelog',
                'bgprouter_journal',
                'bgpscope_list',
                'bgpscope_add',
                'bgpscope',
                'bgpscope_edit',
                'bgpscope_delete',
                'bgpscope_changelog',
                'bgpscope_journal',
                'bgpaddressfamily_list',
                'bgpaddressfamily_add',
                'bgpaddressfamily',
                'bgpaddressfamily_edit',
                'bgpaddressfamily_delete',
                'bgpaddressfamily_changelog',
                'bgpaddressfamily_journal',
                'prefixlist_list',
                'prefixlist_add',
                # 'prefixlist_bulk_import',
                'prefixlist',
                'prefixlist_edit',
                'prefixlist_entries',
                'prefixlist_delete',
                'prefixlist_changelog',
                'prefixlist_journal',
                'prefixlistentry_list',
                'prefixlistentry_add',
                'prefixlistentry_bulk_edit',
                'prefixlistentry_bulk_delete',
                # 'prefixlistentry_bulk_import',
                'prefixlistentry',
                'prefixlistentry_edit',
                'prefixlistentry_delete',
                'prefixlistentry_changelog',
                'prefixlistentry_journal',
                'routemap_list',
                'routemap_add',
                # 'routemap_bulk_import',
                'routemap',
                'routemap_entries',
                'routemap_edit',
                'routemap_delete',
                'routemap_changelog',
                'routemap_journal',
                'routemapentry_list',
                'routemapentry_add',
                'routemapentry_bulk_edit',
                'routemapentry_bulk_delete',
                # 'routemapentry_bulk_import',
                'routemapentry',
                'routemapentry_edit',
                'routemapentry_delete',
                'routemapentry_changelog',
                'routemapentry_journal',
            ]
        )

    def customAssertListEquals(self, list1, list2, msg=None):
        list1_diff = list(set(list1) - set(list2))
        list2_diff = list(set(list2) - set(list1))

        differing = []
        if list1_diff:
            differing.append(f'First list has extra items {list1_diff}')
        if list2_diff:
            differing.append(f'Second list has extra items {list2_diff}')

        diffMsg = '\n'.join(differing)
        msg = self._formatMessage(msg, standardMsg=diffMsg)
        if list1_diff or list2_diff:
            self.fail(msg)

    @staticmethod
    def get_names(patterns):
        names = []
        for pattern in patterns:
            if hasattr(pattern, 'url_patterns'):
                names.extend(URLTestCase.get_names(pattern.url_patterns))
            else:
                names.append(pattern.name)
        return names

    def test_urls(self):
        self.maxDiff = None
        patterns = __import__('netbox_routing.urls', {}, {}, [""]).urlpatterns
        names = sorted(URLTestCase.get_names(patterns))

        self.customAssertListEquals(sorted(names), sorted(self.patterns))
