from utilities.choices import ChoiceSet


__all__ = (
    'BGPAdditionalPathSelectChoices',
    'BGPAddressFamilies',
    'BGPBestPathASPath',
)


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


class BGPBestPathASPath(ChoiceSet):
    IGNORE = 'ignore'
    MULTIPATH = 'multipath-relax'

    CHOICES = [
        (IGNORE, 'Ignore'),
        (MULTIPATH, 'Multipath Relax Comparison')
    ]


class BGPAddressFamilies(ChoiceSet):
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
