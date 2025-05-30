from utilities.choices import ChoiceSet

__all__ = (
    'OSPFAreaTypeChoices',
)

class OSPFAreaTypeChoices(ChoiceSet):
    STANDARD = 'standard'
    STUB = 'stub'
    TOTALLY_STUB = 'totally_stubby_area'
    NSSA = 'nssa'
    TOTALLY_NSSA = 'totally_nssa'

    CHOICES = [
        (STANDARD, 'Standard'),
        (STUB, 'Stub'),
        (TOTALLY_STUB, 'Totally Stubby Area'),
        (NSSA, 'NSSA'),
        (TOTALLY_NSSA, 'Totally NSSA'),
    ]
