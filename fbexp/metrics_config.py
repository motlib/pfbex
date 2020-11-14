'''This module contains the configuration that specifies how TR-064 data is
mapped to prometheus metrics.'''


METRICS_CFG2 = [
    # Uptime
    {
        'metric': 'fritzbox_uptime',
        'type': 'counter',
        'doc': 'Fritzbox uptime',
        'items': [
            {
                'service': 'DeviceInfo1',
                'action': 'GetInfo',
                'attr': 'NewUpTime',
                'labels': {'type': 'device'},
            },
            {
                'service': 'WANIPConnection1',
                'action': 'GetStatusInfo',
                'attr': 'NewUptime',
                'labels': {'type': 'wan_ip_conn'},
            },

            # not available on 6591 Cable
            {
                'service': 'WANPPPConnection1',
                'action': 'GetStatusInfo',
                'attr': 'NewUptime',
                'labels': {'type': 'wan_ppp_conn'},
            },

        ]
    },

    # Software Update Available
    {
        'metric': 'fritzbox_update_available',
        'doc': 'Fritzbox software update available',
        'items': [
            {
                'service': 'UserInterface1',
                'action': 'GetInfo',
                'attr': 'NewUpgradeAvailable',
            }
        ]
    },

    # Network enabled
    {
        'metric': 'fritzbox_net_enabled',
        'doc': 'Network interface enabled',
        'items': [
            {
                'service': 'LANEthernetInterfaceConfig1',
                'action': 'GetInfo',
                'attr': 'NewEnable',
                'labels': {'if': 'lan'},
            },
            {
                'service': 'WLANConfiguration1',
                'action': 'GetInfo',
                'attr': 'NewEnable',
                'labels': {'if': 'wlan1'},
            },
            {
                'service': 'WLANConfiguration2',
                'action': 'GetInfo',
                'attr': 'NewEnable',
                'labels': {'if': 'wlan2'},
            },
            {
                # not available on 6591 Cable
                'service': 'WANDSLInterfaceConfig1',
                'action': 'GetInfo',
                'attr': 'NewEnable',
                'labels': {'if': 'dsl'},
            }
        ]
    },

    # Network status
    {
        'metric': 'fritzbox_net_status',
        'doc': 'Network interface status',
        'items': [
            {
                'service': 'LANEthernetInterfaceConfig1',
                'action': 'GetInfo',
                'attr': 'NewStatus',
                'labels': {'if': 'lan'},
                'fct': lambda x: 1 if x == 'Up' else 0
            },
            {
                'service': 'WLANConfiguration1',
                'action': 'GetInfo',
                'attr': 'NewStatus',
                'labels': {'if': 'wlan1'},
                'fct': lambda x: 1 if x == 'Up' else 0
            },
            {
                'service': 'WLANConfiguration2',
                'action': 'GetInfo',
                'attr': 'NewStatus',
                'labels': {'if': 'wlan1'},
                'fct': lambda x: 1 if x == 'Up' else 0
            },
            {
                # not available on 6591 Cable
                'service': 'WANDSLInterfaceConfig1',
                'action': 'GetInfo',
                'attr': 'NewStatus',
                'labels': {'if': 'dsl'},
                'fct': lambda x: 1 if x == 'Up' else 0
            }
        ]
    },

    # Network bytes
    {
        'metric': 'fritzbox_net_data',
        'type': 'counter',
        'doc': 'Network data volume',
        'items': [
            {
                'service': 'LANEthernetInterfaceConfig1',
                'action': 'GetStatistics',
                'attr': 'NewBytesReceived',
                'labels': { 'if': 'lan', 'dir': 'rx' }
            },
            {
                'service': 'LANEthernetInterfaceConfig1',
                'action': 'GetStatistics',
                'attr': 'NewBytesSent',
                'labels': { 'if': 'lan', 'dir': 'tx' }
            },
            {
                'service': 'WANCommonInterfaceConfig1',
                'action': 'GetTotalBytesSent',
                'attr': 'NewTotalBytesSent',
                'labels': {'if': 'wan', 'dir': 'tx'},
            },
            {
                'service': 'WANCommonInterfaceConfig1',
                'action': 'GetTotalBytesReceived',
                'attr': 'NewTotalBytesReceived',
                'labels': {'if': 'wan', 'dir': 'rx'},
            }

        ]
    },

    # Network packets
    {
        'metric': 'fritzbox_net_packets',
        'type': 'counter',
        'doc': 'Network data packets',
        'items': [
            {
                'service': 'LANEthernetInterfaceConfig1',
                'action': 'GetStatistics',
                'attr': 'NewPacketsReceived',
                'labels': { 'if': 'lan', 'dir': 'rx' }
            },
            {
                'service': 'LANEthernetInterfaceConfig1',
                'action': 'GetStatistics',
                'attr': 'NewPacketsSent',
                'labels': { 'if': 'lan', 'dir': 'tx' }
            },
            {
                'service': 'WANCommonInterfaceConfig1',
                'action': 'GetTotalPacketsReceived',
                'attr': 'NewTotalPacketsReceived',
                'labels': { 'if': 'wan', 'dir': 'rx' }
            },
            {
                'service': 'WANCommonInterfaceConfig1',
                'action': 'GetTotalPacketsSent',
                'attr': 'NewTotalPacketsSent',
                'labels': { 'if': 'wan', 'dir': 'tx' }
            },
            {
                'service': 'WLANConfiguration1',
                'action': 'GetStatistics',
                'attr': 'NewTotalPacketsSent',
                'labels': { 'if': 'wlan1', 'dir': 'tx' }
            },
            {
                'service': 'WLANConfiguration1',
                'action': 'GetStatistics',
                'attr': 'NewTotalPacketsReceived',
                'labels': { 'if': 'wlan1', 'dir': 'rx' }
            },
            {
                'service': 'WLANConfiguration2',
                'action': 'GetStatistics',
                'attr': 'NewTotalPacketsSent',
                'labels': { 'if': 'wlan2', 'dir': 'tx' }
            },
            {
                'service': 'WLANConfiguration2',
                'action': 'GetStatistics',
                'attr': 'NewTotalPacketsReceived',
                'labels': { 'if': 'wlan2', 'dir': 'rx' }
            },


        ]
    },

    # PPP Connection Status
    # not available for FRITZ!Box 6591 Cable (lgi)
    {

        'metric': 'fritzbox_ppp_connection_uptime',
        'type': 'counter',
        'doc': 'PPP connection uptime',
        'items': [
            {
                'service': 'WANPPPConnection1',
                'action': 'GetStatusInfo',
                'attr': 'NewUptime',
            }
        ]
    },
    {
        'metric': 'fritzbox_ppp_connection_state',
        'doc': 'PPP connection state',
        'items': [
            {
                'service': 'WANPPPConnection1',
                'action': 'GetStatusInfo',
                'attr': 'NewConnectionStatus',
                'fct': lambda x: 1.0 if x == 'Connected' else 0.0
            }
        ]
    },

    # Wifi Channel
    {
        'metric': 'fritzbox_wifi_channel',
        'doc': 'Wifi channel number',
        'items': [
            {
                'service': 'WLANConfiguration1',
                'action': 'GetInfo',
                'attr': 'NewChannel',
                'labels': {'if': 'wlan1'},
            },
            {
                'service': 'WLANConfiguration2',
                'action': 'GetInfo',
                'attr': 'NewChannel',
                'labels': {'if': 'wlan2'},
            }
        ]
    },

    # Wifi Connections
    {
        'metric': 'fritzbox_wifi_associations',
        'doc': 'wifi associations',
        'items': [
            {
                'service': 'WLANConfiguration1',
                'action': 'GetTotalAssociations',
                'attr': 'NewTotalAssociations',
                'labels': {'if': 'wlan1'},
            },
            {
                'service': 'WLANConfiguration2',
                'action': 'GetTotalAssociations',
                'attr': 'NewTotalAssociations',
                'labels': {'if': 'wlan2'},
            },
        ]
    }


    # DSL Interface Information
    # not available for FRITZ!Box 6591 Cable (lgi)

#    {
#        'service': 'WANDSLInterfaceConfig1',
#        'action': 'GetInfo',
#        'metrics': [
#            {
#                'metric': 'fritzbox_dsl_status_enabled',
#                'doc': 'DSL enabled',
#                'key': 'NewEnable',
#            },
#            {
#                'metric': 'fritzbox_dsl_status',
#                'doc': 'DSL Status',
#                'key': 'NewStatus',
#            },
#            {
#                'metric': 'fritzbox_dsl_datarate_kbps_up',
#                'doc': 'DSL Upstream datarate in kpbs',
#                'key': 'NewUpstreamCurrRate',
#            },
#            {
#                'metric': 'fritzbox_dsl_datarate_kbps_down',
#                'doc': 'DSL Downstream datarate in kpbs',
#                'key': 'NewDownstreamCurrRate',
#            },
#            {
#                'metric': 'fritzbox_dsl_noise_margin_dB_up',
#                'doc': 'Noise Margin in dB',
#                'key': 'NewUpstreamNoiseMargin',
#                'fct': lambda x: x / 10.0,
#            },
#            {
#                'metric': 'fritzbox_dsl_noise_margin_dB_down',
#                'doc': 'Noise Margin in dB',
#                'key': 'NewDownstreamNoiseMargin',
#                'fct': lambda x: x / 10.0,
#            },
#            {
#                'metric': 'fritzbox_dsl_attenuation_dB_up',
#                'doc': 'Line attenuation in dB',
#                'key': 'NewUpstreamAttenuation',
#                'fct': lambda x: x / 10.0,
#            },
#            {
#                'metric': 'fritzbox_dsl_attenuation_dB_down',
#                'doc': 'Line attenuation in dB',
#                'key': 'NewDownstreamAttenuation',
#                'fct': lambda x: x / 10.0,
#            }
#        ]
#    }

]
