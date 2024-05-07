from utilities.choices import ChoiceSet


__all__ = (
    'BGPAdditionalPathSelectChoices',
    'BGPAddressFamilyChoices',
    'BGPBestPathASPathChoices',
    'BGPSettingChoices',
    'BFDChoices',
)


class BGPSettingChoices(ChoiceSet):
    SUMMARY = 'auto_summary'

    RID = 'router_id'
    ADDPATH_INSTALL = 'additional_paths_install'
    ADDPATH_RECEIVE = 'additional_paths_receive'
    ADDPATH_SEND = 'additional_paths_send'
    ASDOT = 'asdot'
    GR = 'graceful_restart'
    DEFAULT_ORIGINATE = 'default_information_originate'
    DEFAULT_METRIC = 'default_metric'
    DISTANCE_EBGP = 'distance_ebgp'
    DISTANCE_IBGP = 'distance_ibgp'
    DISTANCE_EMBGP = 'distance_embgp'
    DISTANCE_IMBGP = 'distance_imbgp'
    MAX_PATHS = 'paths_maximum'
    MAX_PATHS_SECONDARY = 'paths_maximum_secondary'
    KEEPALIVE = 'timers_keepalive'
    HOLD = 'timers_hold'

    CHOICES = [
        (RID, 'Router ID'),
        (SUMMARY, 'Auto summary'),
        (ADDPATH_INSTALL, 'Additional Pathss (install)'),
        (ADDPATH_RECEIVE, 'Additional Paths (receive)'),
        (ADDPATH_SEND, 'Additional Paths (send)'),
        (ASDOT, 'AS Dot Notation'),
        (GR, 'Graceful Restart'),
        (DEFAULT_ORIGINATE, 'Default Originate'),
        (DEFAULT_METRIC, 'Default Metric'),
        (DISTANCE_EBGP, 'eBGP Distance'),
        (DISTANCE_IBGP, 'iBGP Distance'),
        (DISTANCE_EMBGP, 'MP eBGP Distance'),
        (DISTANCE_IMBGP, 'MP iBGP Distance'),
        (MAX_PATHS, 'Maximum Paths'),
        (MAX_PATHS_SECONDARY, 'Maximum Paths (secondary)'),
        (KEEPALIVE, 'Keep Alive'),
        (HOLD, 'Hold Time'),
    ]

    FIELD_TYPES = {
        RID: 'ipaddr',
        SUMMARY: 'boolean',
        ADDPATH_INSTALL: 'integer',
        ADDPATH_RECEIVE: 'integer',
        ADDPATH_SEND: 'integer',
        ASDOT: 'boolean',
        GR: 'boolean',
        DEFAULT_ORIGINATE: 'boolean',
        DEFAULT_METRIC: 'integer',
        DISTANCE_EBGP: 'integer',
        DISTANCE_IBGP: 'integer',
        DISTANCE_EMBGP: 'integer',
        DISTANCE_IMBGP: 'integer',
        MAX_PATHS: 'integer',
        MAX_PATHS_SECONDARY: 'integer',
        KEEPALIVE: 'integer',
        HOLD: 'integer',
    }


class BGPAdditionalPathSelectChoices(ChoiceSet):
    ALL = 'all'
    BACKUP = 'backup'
    BEST_EXTERNAL = 'best-external'
    GROUP_BEST = 'group-best'

    CHOICES = [
        (ALL, 'All'),
        (BACKUP, 'Backup'),
        (BEST_EXTERNAL, 'Best External'),
        (GROUP_BEST, 'Group Best')
    ]


class BFDChoices(ChoiceSet):
    SINGLEHOP = 'singlehop'
    MULTIHOP = 'multihop'

    CHOICES = [
        (SINGLEHOP, 'Single-Hop'),
        (MULTIHOP, 'Multi-Hop')
    ]


class BGPBestPathASPathChoices(ChoiceSet):
    IGNORE = 'ignore'
    MULTIPATH = 'multipath-relax'

    CHOICES = [
        (IGNORE, 'Ignore'),
        (MULTIPATH, 'Multipath Relax Comparison')
    ]


class BGPAddressFamilyChoices(ChoiceSet):
    IPV4_UNICAST = 'ipv4-unicast'
    IPV6_UNICAST = 'ipv6-unicast'
    VPNV4_UNICAST = 'vpnv4-unicast'
    VPNV6_UNICAST = 'vpnv6-unicast'
    IPV4_MULTICAST = 'ipv4-multicast'
    IPV6_MULTICAST = 'ipv6-multicast'
    VPNV4_MULTICAST = 'vpnv4-multicast'
    VPNV6_MULTICAST = 'vpnv6-multicast'
    IPV4_FLOWSPEC = 'ipv4-flowspec'
    IPV6_FLOWSPEC = 'ipv6-flowspec'
    VPNV4_FLOWSPEC = 'vpnv4-flowspec'
    VPNV6_FLOWSPEC = 'vpnv6-flowspec'
    NSAP = 'nsap'
    L2VPNVPLS = 'l2vpn-vpls'
    L2VPSEVPN = 'l2vpn-evpn'
    LINKSTATE = 'link-state'
    RTFILTER_UNICAST = 'rtfilter-unicast'

    CHOICES = [
        (IPV4_UNICAST, 'IPv4 Unicast'),
        (IPV6_UNICAST, 'IPv6 Unicast'),
        (VPNV4_UNICAST, 'VPNv4 Unicast'),
        (VPNV6_UNICAST, 'VPNv6 Unicast'),
        (IPV4_MULTICAST, 'IPv4 Multicast'),
        (IPV6_MULTICAST, 'IPv6 Multicast'),
        (VPNV4_UNICAST, 'VPNv4 Multicast'),
        (VPNV6_MULTICAST, 'VPNv6 Multicast'),
        (IPV4_FLOWSPEC, 'IPv4 Flowspec'),
        (IPV6_FLOWSPEC, 'IPv6 Flowspec'),
        (VPNV4_FLOWSPEC, 'VPNv4 Flowspec'),
        (VPNV6_FLOWSPEC, 'VPNv6 Flowspec'),
        (NSAP, 'NSAP'),
        (L2VPNVPLS, 'L2VPN VPLS'),
        (L2VPSEVPN, 'L2VPN EVPN'),
        (LINKSTATE, 'LINK-STATE'),
        (RTFILTER_UNICAST, 'RTFILTER')
    ]
