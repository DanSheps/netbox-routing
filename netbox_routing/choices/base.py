from utilities.choices import ChoiceSet


__all__ = (
    'AuthenticationChoices',
)


class AuthenticationChoices(ChoiceSet):
    KEYCHAIN = 'key-chain'
    MESSAGE_DIGEST = 'message-digest'
    NULL = 'null'

    CHOICES = [
        (KEYCHAIN, 'Key Chain'),
        (MESSAGE_DIGEST, 'Message Digest'),
        (NULL, 'Null Authentication')
    ]