from utilities.choices import ChoiceSet


__all__ = ('AuthenticationChoices', 'OSPFInterfaceTypeChoices')


class AuthenticationChoices(ChoiceSet):
    KEYCHAIN = 'key-chain'
    MESSAGE_DIGEST = 'message-digest'
    NULL = 'null'

    CHOICES = [
        (KEYCHAIN, 'Key Chain'),
        (MESSAGE_DIGEST, 'Message Digest'),
        (NULL, 'Null Authentication'),
    ]


class OSPFInterfaceTypeChoices(ChoiceSet):
    BROADCAST = 'broadcast'
    POINT_TO_POINT = 'point-to-point'
    NON_BROADCAST = 'non-broadcast'
    POINT_TO_MULTIPOINT = 'point-to-multipoint'
    POINT_TO_MULTIPOINT_NON_BROADCAST = 'point-to-multipoint-non-broadcast'
    LOOPBACK = 'loopback'

    CHOICES = [
        (BROADCAST, 'Broadcast'),
        (NON_BROADCAST, 'Non-Broadcast'),
        (POINT_TO_POINT, 'Point-to-Point'),
        (POINT_TO_MULTIPOINT, 'Point-to-Multipoint'),
        (LOOPBACK, 'Loopback'),
        (POINT_TO_MULTIPOINT_NON_BROADCAST, 'Point-to-Multipoint Non-Broadcast'),
    ]
