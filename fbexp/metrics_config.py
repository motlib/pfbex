'''This module contains the configuration that specifies how TR-064 data is
mapped to prometheus metrics.'''


METRICS_CFG = [
    {
        # TR-64 service name
        'service': 'UserInterface1',
        # TR-64 action name
        'action': 'GetInfo',
        'metrics': [
            {
                # prometheus metrics name
                'metric': 'fritzbox_update_available',
                # prometheus documentation
                'doc': 'Fritzbox update available',
                # TR-64 value identifier
                'key': 'NewUpgradeAvailable',
                # conversion function transforming the value from TR-64 to
                # prometheus
                'fct': lambda x: 1 if x == '1' else 0,
            }
        ]
    },
    {
        'service': 'LANEthernetInterfaceConfig1',
        'action': 'GetInfo',
        'metrics': [
            {
                'metric': 'fritzbox_lan_status_enabled',
                'doc': 'LAN interface enabled',
                'key': 'NewEnable',
            },
            {
                'metric': 'fritzbox_lan_status',
                'doc': 'LAN interface status',
                'key': 'NewStatus',
                'fct': lambda x: 1 if x == 'Up' else 0
            },
        ]
    },
    {
        'service': 'LANEthernetInterfaceConfig1',
        'action': 'GetStatistics',
        'metrics': [
            {
                'metric': 'fritzbox_lan_received_bytes',
                'doc': 'LAN bytes received',
                'key': 'NewBytesReceived',
            },
            {
                'metric': 'fritzbox_lan_received_bytes',
                'doc': 'LAN bytes sent',
                'key': 'NewBytesSent',
            },
            {
                'metric': 'fritzbox_lan_received_bytes',
                'doc': 'LAN packets received',
                'key': 'NewPacketsReceived',
            },
            {
                'metric': 'fritzbox_lan_received_bytes',
                'doc': 'LAN packets sent',
                'key': 'NewPacketsReceived',
            }
        ]
    },
    {
        'service': 'WANDSLInterfaceConfig1',
        'action': 'GetInfo',
        'metrics': [
            {
                'metric': 'fritzbox_dsl_status_enabled',
                'doc': 'DSL enabled',
                'key': 'NewEnable',
            },
            {
                'metric': 'fritzbox_dsl_status',
                'doc': 'DSL Status',
                'key': 'NewStatus',
            },
            {
                'metric': 'fritzbox_dsl_datarate_kbps_up',
                'doc': 'DSL Upstream datarate in kpbs',
                'key': 'NewUpstreamCurrRate',
            },
            {
                'metric': 'fritzbox_dsl_datarate_kbps_down',
                'doc': 'DSL Downstream datarate in kpbs',
                'key': 'NewDownstreamCurrRate',
            },
            {
                'metric': 'fritzbox_dsl_noise_margin_dB_up',
                'doc': 'Noise Margin in dB',
                'key': 'NewUpstreamNoiseMargin',
                'fct': lambda x: x / 10.0,
            },
            {
                'metric': 'fritzbox_dsl_noise_margin_dB_down',
                'doc': 'Noise Margin in dB',
                'key': 'NewDownstreamNoiseMargin',
                'fct': lambda x: x / 10.0,
            },
            {
                'metric': 'fritzbox_dsl_attenuation_dB_up',
                'doc': 'Line attenuation in dB',
                'key': 'NewUpstreamAttenuation',
                'fct': lambda x: x / 10.0,
            },
            {
                'metric': 'fritzbox_dsl_attenuation_dB_down',
                'doc': 'Line attenuation in dB',
                'key': 'NewDownstreamAttenuation',
                'fct': lambda x: x / 10.0,
            }
        ]
    },
    {
        'service': 'WANPPPConnection:1',
        'action': 'GetStatusInfo',
        'metrics': [
            {
                'metric': 'fritzbox_ppp_connection_uptime',
                'doc': 'PPP connection uptime',
                'key': 'NewUptime',
            },
            {
                'metric': 'fritzbox_ppp_connection_state',
                'doc': 'PPP connection state',
                'key': 'NewConnectionStatus',
                'fct': lambda x: 1.0 if x == 'Connected' else 0.0
            },
        ]
    },
    {
        'service': 'WANCommonInterfaceConfig1',
        'action': 'GetTotalBytesSent',
        'metrics': [
            {
                'metric': 'fritzbox_wan_data_bytes_tx',
                'doc': 'WAN Tx data in bytes',
                'key': 'NewTotalBytesSent',
            }
        ]
    },
    {
        'service': 'WANCommonInterfaceConfig1',
        'action': 'GetTotalBytesReceived',
        'metrics': [
            {
                'metric': 'fritzbox_wan_data_bytes_rx',
                'doc': 'WAN Rx data in bytes',
                'key': 'NewTotalBytesReceived',
            }
        ]
    },
    {
        'service': 'WANCommonInterfaceConfig1',
        'action': 'GetTotalPacketsSent',
        'metrics': [
            {
                'metric': 'fritzbox_wan_data_packets_tx',
                'doc': 'WAN Tx packets',
                'key': 'NewTotalPacketsSent',
            }
        ]
    },
    {
        'service': 'WANCommonInterfaceConfig1',
        'action': 'GetTotalPacketsReceived',
        'metrics': [
            {
                'metric': 'fritzbox_wan_data_packets_rx',
                'doc': 'WAN Rx packets',
                'key': 'NewTotalPacketsReceived',
            }
        ]
    },
]
