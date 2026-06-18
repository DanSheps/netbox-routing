# SPDX-License-Identifier: Apache-2.0

from utilities.choices import ChoiceSet

__all__ = (
    'ISISAddressFamilyChoices',
    'ISISAuthTypeChoices',
    'ISISCircuitTypeChoices',
    'ISISIsTypeChoices',
    'ISISMetricStyleChoices',
    'ISISNetworkTypeChoices',
    'ISISLevelChoices',
    'ISISSettingChoices',
)


class ISISLevelChoices(ChoiceSet):
    """IS-IS level identifier for per-level child rows (instance + interface)."""

    LEVEL1 = 1
    LEVEL2 = 2

    CHOICES = (
        (LEVEL1, 'Level-1'),
        (LEVEL2, 'Level-2'),
    )


class ISISAddressFamilyChoices(ChoiceSet):
    IPV4 = 'ipv4'
    IPV6 = 'ipv6'

    CHOICES = ((IPV4, 'IPv4'), (IPV6, 'IPv6'))


class ISISCircuitTypeChoices(ChoiceSet):
    LEVEL1 = 'level-1'
    LEVEL2 = 'level-2-only'
    LEVEL12 = 'level-1-2'

    CHOICES = (
        (LEVEL1, 'Level-1'),
        (LEVEL2, 'Level-2 Only'),
        (LEVEL12, 'Level-1-2'),
    )


class ISISNetworkTypeChoices(ChoiceSet):
    P2P = 'point-to-point'
    BROADCAST = 'broadcast'

    CHOICES = (
        (P2P, 'Point-to-Point'),
        (BROADCAST, 'Broadcast'),
    )


class ISISIsTypeChoices(ChoiceSet):
    LEVEL1 = 'level-1'
    LEVEL2 = 'level-2-only'
    LEVEL12 = 'level-1-2'

    CHOICES = (
        (LEVEL1, 'Level-1'),
        (LEVEL2, 'Level-2 Only'),
        (LEVEL12, 'Level-1-2'),
    )


class ISISMetricStyleChoices(ChoiceSet):
    WIDE = 'wide'
    NARROW = 'narrow'
    TRANSITION = 'transition'

    CHOICES = (
        (WIDE, 'Wide'),
        (NARROW, 'Narrow'),
        (TRANSITION, 'Transition'),
    )


class ISISAuthTypeChoices(ChoiceSet):
    MD5 = 'md5'
    TEXT = 'text'

    CHOICES = (
        (MD5, 'MD5'),
        (TEXT, 'Cleartext'),
    )


class ISISSettingChoices(ChoiceSet):
    """EAV long-tail of IS-IS scalars that don't warrant a dedicated column.

    Mirrors BGPSettingChoices: each key declares a FIELD_TYPES entry so the
    settings form/panel machinery (SettingsChoicePanel, the settings mixin)
    can render and validate the value generically. The common, filterable
    knobs (timers initial/max, lifetime, mtu, te, sr...) get their own model
    columns instead; only the divergent/long-tail scalars live here.
    """

    # SPF/LSP backoff sub-knob — vendor-specific algorithm (time vs count)
    SPF_SECOND_WAIT = 'spf_second_wait'        # Cisco/Nokia/IOS-XR: ms
    SPF_RAPID_RUNS = 'spf_rapid_runs'          # Junos: count of rapid runs
    LSP_SECOND_WAIT = 'lsp_second_wait'        # Cisco/Nokia/IOS-XR: ms

    # Behavioural long-tail
    GRACEFUL_RESTART = 'graceful_restart'
    LDP_SYNC = 'ldp_sync'
    PREFIX_SUPPRESSION = 'prefix_suppression'
    LOG_ADJ_CHANGES = 'log_adjacency_changes'
    ADVERTISE_PASSIVE_ONLY = 'advertise_passive_only'
    DEFAULT_ROUTE_TAG = 'default_route_tag'
    MULTI_TOPOLOGY = 'multi_topology'
    IGP_SHORTCUT = 'igp_shortcut'
    HELLO_PADDING = 'hello_padding'
    RIB_PRIORITY = 'rib_priority'

    CHOICES = [
        (SPF_SECOND_WAIT, 'SPF Second Wait (ms)'),
        (SPF_RAPID_RUNS, 'SPF Rapid Runs'),
        (LSP_SECOND_WAIT, 'LSP-Gen Second Wait (ms)'),
        (GRACEFUL_RESTART, 'Graceful Restart'),
        (LDP_SYNC, 'LDP-IGP Sync'),
        (PREFIX_SUPPRESSION, 'Prefix Suppression'),
        (LOG_ADJ_CHANGES, 'Log Adjacency Changes'),
        (ADVERTISE_PASSIVE_ONLY, 'Advertise Passive Only'),
        (DEFAULT_ROUTE_TAG, 'Default Route Tag'),
        (MULTI_TOPOLOGY, 'Multi-Topology'),
        (IGP_SHORTCUT, 'IGP Shortcut'),
        (HELLO_PADDING, 'Hello Padding'),
        (RIB_PRIORITY, 'RIB Priority'),
    ]

    FIELD_TYPES = {
        SPF_SECOND_WAIT: 'integer',
        SPF_RAPID_RUNS: 'integer',
        LSP_SECOND_WAIT: 'integer',
        GRACEFUL_RESTART: 'boolean',
        LDP_SYNC: 'boolean',
        PREFIX_SUPPRESSION: 'boolean',
        LOG_ADJ_CHANGES: 'boolean',
        ADVERTISE_PASSIVE_ONLY: 'boolean',
        DEFAULT_ROUTE_TAG: 'integer',
        MULTI_TOPOLOGY: 'boolean',
        IGP_SHORTCUT: 'boolean',
        HELLO_PADDING: 'boolean',
        RIB_PRIORITY: 'string',
    }
