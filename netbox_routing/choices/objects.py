from utilities.choices import ChoiceSet


class PermitDenyChoices(ChoiceSet):
    PERMIT = 'permit'
    DENY = 'deny'

    CHOICES = [
        (PERMIT, 'Permit'),
        (DENY, 'Deny')
    ]
