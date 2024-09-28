from utilities.choices import ChoiceSet


class EIGRPRouterChoices(ChoiceSet):
    CLASSIC = 'classic'
    NAMED = 'named'

    CHOICES = [
        (CLASSIC, 'Classic Router'),
        (NAMED, 'Named Router')
    ]