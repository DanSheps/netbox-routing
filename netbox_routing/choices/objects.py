from utilities.choices import ChoiceSet


class PermitDenyChoices(ChoiceSet):
    PERMIT = 'permit'
    DENY = 'deny'

    CHOICES = [
        (PERMIT, 'Permit', 'blue'),
        (DENY, 'Deny', 'red')
    ]
