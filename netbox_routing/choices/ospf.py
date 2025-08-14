from utilities.choices import ChoiceSet


class OSPFAreaTypeChoices(ChoiceSet):
    STANDARD = 'standard'
    BACKBONE = 'backbone'
    STUB = 'stub'
    TSA = 'tsa'
    NSSA = 'nssa'
    TNSSA = 'tnssa'

    CHOICES = [
        (STANDARD, 'Standard Area'),
        (BACKBONE, 'Backbone Area'),
        (STUB, 'Stub Area'),
        (TSA, 'Totally Stubby Area'),
        (NSSA, 'Not-So-Stubby Area'),
        (TNSSA, 'Totally Not-So-Stubby Area'),
    ]
