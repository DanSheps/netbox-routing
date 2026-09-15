# SPDX-License-Identifier: Apache-2.0

from utilities.choices import ChoiceSet

__all__ = (
    'ISISAddressFamilyChoices',
    'ISISAuthTypeChoices',
    'ISISCircuitTypeChoices',
    'ISISFastRerouteChoices',
    'ISISFrrProtectionChoices',
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


class ISISFastRerouteChoices(ChoiceSet):
    """Process-wide IP fast-reroute computation flavour.

    IOS-XR 'fast-reroute per-prefix [remote-lfa|ti-lfa]', Junos
    backup-spf-options [use-post-convergence-lfa], Nokia loopfree-alternate
    [remote-lfa|ti-lfa]
    """

    LFA = 'lfa'
    REMOTE_LFA = 'remote-lfa'
    TI_LFA = 'ti-lfa'

    CHOICES = (
        (LFA, 'LFA'),
        (REMOTE_LFA, 'Remote LFA'),
        (TI_LFA, 'TI-LFA'),
    )


class ISISFrrProtectionChoices(ChoiceSet):
    """Per-interface repair coverage requested from the FRR computation.

    'node' covers node-and-link (Junos node-link-protection); 'link' is
    link-only.
    """

    LINK = 'link'
    NODE = 'node'

    CHOICES = (
        (LINK, 'Link protection'),
        (NODE, 'Node protection'),
    )


class ISISAuthTypeChoices(ChoiceSet):
    MD5 = 'md5'
    TEXT = 'text'
    HMAC_SHA1 = 'hmac-sha-1'
    HMAC_SHA256 = 'hmac-sha-256'

    CHOICES = (
        (MD5, 'MD5'),
        (TEXT, 'Cleartext'),
        (HMAC_SHA1, 'HMAC-SHA-1'),
        (HMAC_SHA256, 'HMAC-SHA-256'),
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
    SPF_SECOND_WAIT = 'spf_second_wait'  # Cisco/Nokia/IOS-XR: ms
    SPF_RAPID_RUNS = 'spf_rapid_runs'  # Junos: count of rapid runs
    LSP_SECOND_WAIT = 'lsp_second_wait'  # Cisco/Nokia/IOS-XR: ms

    # Traffic-engineering router-ID (IOS/IOS-XR 'mpls traffic-eng router-id';
    # derived from the global router-id on
    # Junos/Nokia, where it reads as absent). Value is an IP address or, on
    # Cisco platforms, an interface reference — a string either way.
    TE_IPV4_ROUTER_ID = 'te_ipv4_router_id'
    TE_IPV6_ROUTER_ID = 'te_ipv6_router_id'

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
        (TE_IPV4_ROUTER_ID, 'TE IPv4 Router-ID'),
        (TE_IPV6_ROUTER_ID, 'TE IPv6 Router-ID'),
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
        TE_IPV4_ROUTER_ID: 'string',
        TE_IPV6_ROUTER_ID: 'string',
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
