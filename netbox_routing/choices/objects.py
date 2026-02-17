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
