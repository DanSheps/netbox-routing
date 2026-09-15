# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase

from netbox.graphql.schema import schema

__all__ = ('ISISGraphQLSchemaTestCase',)


class ISISGraphQLSchemaTestCase(TestCase):
    """Plaintext IS-IS auth keys must not be queryable via GraphQL.

    The keys are stored plaintext (routing-protocol auth, not config-access
    creds), but should not be exposed on the bulk GraphQL query surface. The
    non-secret auth *type* (md5/text) stays queryable.
    """

    @staticmethod
    def _field_names(typename):
        # NB: `schema.schema_converter.type_map` is a strawberry-graphql internal
        # (it is the standard way to introspect a built schema in tests, but not a
        # public API). Verified against strawberry-graphql 0.x / strawberry-django
        # as vendored by NetBox; if a future bump renames it, this canary fails
        # loudly here rather than silently re-exposing the excluded fields.
        gql_type = schema.schema_converter.type_map[typename]
        return {f.name for f in gql_type.definition.fields}

    def test_instance_auth_keys_excluded(self):
        fields = self._field_names('ISISInstanceType')
        self.assertNotIn('area_auth_key', fields)
        self.assertNotIn('domain_auth_key', fields)
        self.assertIn('area_auth_type', fields)
        self.assertIn('domain_auth_type', fields)

    def test_interface_hello_auth_key_excluded(self):
        fields = self._field_names('ISISInterfaceType')
        self.assertNotIn('hello_auth_key', fields)
        self.assertIn('hello_auth_type', fields)

    def test_level_auth_key_excluded(self):
        fields = self._field_names('ISISLevelType')
        self.assertNotIn('auth_key', fields)
        self.assertIn('auth_type', fields)

    def test_setting_raw_gfk_id_excluded(self):
        # `fields='__all__'` would win over `exclude` and re-expose the raw
        # `assigned_object_id`; the resolved `assigned_object` union (plus the
        # typed `assigned_object_type`) is the intended surface instead.
        fields = self._field_names('ISISSettingType')
        self.assertNotIn('assigned_object_id', fields)
        self.assertIn('assigned_object', fields)
        self.assertIn('assigned_object_type', fields)
