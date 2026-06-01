from utilities.choices import ChoiceSet


class ActionChoices(ChoiceSet):
    PERMIT = 'permit'
    DENY = 'deny'

    CHOICES = [(PERMIT, 'Permit', 'blue'), (DENY, 'Deny', 'red')]


class CommunityStatusChoices(ChoiceSet):
    key = "Community.status"

    STATUS_ACTIVE = 'active'
    STATUS_RESERVED = 'reserved'
    STATUS_DEPRECATED = 'deprecated'

    CHOICES = [
        (STATUS_ACTIVE, 'Active', 'blue'),
        (STATUS_RESERVED, 'Reserved', 'cyan'),
        (STATUS_DEPRECATED, 'Deprecated', 'red'),
    ]


class StaticRouteTypeChoices(ChoiceSet):
    key = 'StaticRoute.type'

    TYPE_UNICAST     = 'unicast'
    TYPE_BLACKHOLE   = 'blackhole'
    TYPE_UNREACHABLE = 'unreachable'

    CHOICES = [
        (TYPE_UNICAST,     'Unicast',     'blue'),
        (TYPE_BLACKHOLE,   'Blackhole',   'dark'),
        (TYPE_UNREACHABLE, 'Unreachable', 'orange'),
    ]
