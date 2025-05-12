from utilities.choices import ChoiceSet

__all__ = (
    'OSPFAreaTypeChoices',
    'OSPFNetworkTypeChoices',
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
class OSPFNetworkTypeChoices(ChoiceSet):
    BROADCAST = 'broadcast'
    NON_BROADCAST = 'non_broadcast'
    POINT_TO_POINT = 'point_to_point'
    POINT_TO_MULTIPOINT = 'point_to_multipoint'
    POINT_TO_MULTIPOINT_NON_BROADCAST = 'point_to_multipoint_non_broadcast'

    CHOICES = [
        (BROADCAST, 'Broadcast'),
        (NON_BROADCAST, 'Non Broadcast'),
        (POINT_TO_POINT, 'Point to Point'),
        (POINT_TO_MULTIPOINT, 'Point to Multipoint'),
        (POINT_TO_MULTIPOINT_NON_BROADCAST, 'Point to Multipoint Non Broadcast'),
   ]
