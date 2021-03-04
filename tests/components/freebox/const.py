"""Test constants."""

MOCK_HOST = "myrouter.freeboxos.fr"
MOCK_PORT = 1234

# router
DATA_SYSTEM_GET_CONFIG = {
    "mac": "68:A3:78:00:00:00",
    "model_info": {
        "has_ext_telephony": True,
        "has_speakers_jack": True,
        "wifi_type": "2d4_5g",
        "pretty_name": "Freebox Server (r2)",
        "customer_hdd_slots": 0,
        "name": "fbxgw-r2/full",
        "has_speakers": True,
        "internal_hdd_size": 250,
        "has_femtocell_exp": True,
        "has_internal_hdd": True,
        "has_dect": True,
    },
    "fans": [{"id": "fan0_speed", "name": "Ventilateur 1", "value": 2130}],
    "sensors": [
        {"id": "temp_hdd", "name": "Disque dur", "value": 40},
        {"id": "temp_sw", "name": "Température Switch", "value": 50},
        {"id": "temp_cpum", "name": "Température CPU M", "value": 60},
        {"id": "temp_cpub", "name": "Température CPU B", "value": 56},
    ],
    "board_name": "fbxgw2r",
    "disk_status": "active",
    "uptime": "156 jours 19 heures 56 minutes 16 secondes",
    "uptime_val": 13550176,
    "user_main_storage": "Disque dur",
    "box_authenticated": True,
    "serial": "762601T190510709",
    "firmware_version": "4.2.5",
}

# sensors
DATA_CONNECTION_GET_STATUS = {
    "type": "ethernet",
    "rate_down": 198900,
    "bytes_up": 12035728872949,
    "ipv4_port_range": [0, 65535],
    "rate_up": 1440000,
    "bandwidth_up": 700000000,
    "ipv6": "2a01:e35:ffff:ffff::1",
    "bandwidth_down": 1000000000,
    "media": "ftth",
    "state": "up",
    "bytes_down": 2355966141297,
    "ipv4": "82.67.00.00",
}

DATA_CALL_GET_CALLS_LOG = [
    {
        "number": "0988290475",
        "type": "missed",
        "id": 94,
        "duration": 15,
        "datetime": 1613752718,
        "contact_id": 0,
        "line_id": 0,
        "name": "0988290475",
        "new": True,
    },
    {
        "number": "0367250217",
        "type": "missed",
        "id": 93,
        "duration": 25,
        "datetime": 1613662328,
        "contact_id": 0,
        "line_id": 0,
        "name": "0367250217",
        "new": True,
    },
    {
        "number": "0184726018",
        "type": "missed",
        "id": 92,
        "duration": 25,
        "datetime": 1613225098,
        "contact_id": 0,
        "line_id": 0,
        "name": "0184726018",
        "new": True,
    },
]

DATA_STORAGE_GET_DISKS = [
    {
        "idle_duration": 0,
        "read_error_requests": 0,
        "read_requests": 110,
        "spinning": True,
        # "table_type": "ms-dos", API returns without dash, but codespell isn't agree
        "firmware": "SC1D",
        "type": "internal",
        "idle": False,
        "connector": 0,
        "id": 0,
        "write_error_requests": 0,
        "state": "enabled",
        "write_requests": 2708929,
        "total_bytes": 250050000000,
        "model": "ST9250311CS",
        "active_duration": 0,
        "temp": 40,
        "serial": "6VCQY907",
        "partitions": [
            {
                "fstype": "ext4",
                "total_bytes": 244950000000,
                "label": "Disque dur",
                "id": 2,
                "internal": True,
                "fsck_result": "no_run_yet",
                "state": "mounted",
                "disk_id": 0,
                "free_bytes": 227390000000,
                "used_bytes": 5090000000,
                "path": "L0Rpc3F1ZSBkdXI=",
            }
        ],
    }
]

# switch
WIFI_GET_GLOBAL_CONFIG = {"enabled": True, "mac_filter_state": "disabled"}

# device_tracker
DATA_LAN_GET_HOSTS_LIST = [
    {
        "l2ident": {"id": "8C:97:EA:00:00:00", "type": "mac_address"},
        "active": True,
        "persistent": False,
        "names": [
            {"name": "d633d0c8-958c-43cc-e807-d881b076924b", "source": "mdns"},
            {"name": "Freebox Player POP", "source": "mdns_srv"},
        ],
        "vendor_name": "Freebox SAS",
        "host_type": "smartphone",
        "interface": "pub",
        "id": "ether-8c:97:ea:00:00:00",
        "last_time_reachable": 1614107652,
        "primary_name_manual": False,
        "l3connectivities": [
            {
                "addr": "192.168.1.180",
                "active": True,
                "reachable": True,
                "last_activity": 1614107614,
                "af": "ipv4",
                "last_time_reachable": 1614104242,
            },
            {
                "addr": "fe80::dcef:dbba:6604:31d1",
                "active": True,
                "reachable": True,
                "last_activity": 1614107645,
                "af": "ipv6",
                "last_time_reachable": 1614107645,
            },
            {
                "addr": "2a01:e34:eda1:eb40:8102:4704:7ce0:2ace",
                "active": False,
                "reachable": False,
                "last_activity": 1611574428,
                "af": "ipv6",
                "last_time_reachable": 1611574428,
            },
            {
                "addr": "2a01:e34:eda1:eb40:c8e5:c524:c96d:5f5e",
                "active": False,
                "reachable": False,
                "last_activity": 1612475101,
                "af": "ipv6",
                "last_time_reachable": 1612475101,
            },
            {
                "addr": "2a01:e34:eda1:eb40:583a:49df:1df0:c2df",
                "active": True,
                "reachable": True,
                "last_activity": 1614107652,
                "af": "ipv6",
                "last_time_reachable": 1614107652,
            },
            {
                "addr": "2a01:e34:eda1:eb40:147e:3569:86ab:6aaa",
                "active": False,
                "reachable": False,
                "last_activity": 1612486752,
                "af": "ipv6",
                "last_time_reachable": 1612486752,
            },
        ],
        "default_name": "Freebox Player POP",
        "model": "fbx8am",
        "reachable": True,
        "last_activity": 1614107652,
        "primary_name": "Freebox Player POP",
    },
    {
        "l2ident": {"id": "DE:00:B0:00:00:00", "type": "mac_address"},
        "active": False,
        "persistent": False,
        "vendor_name": "",
        "host_type": "workstation",
        "interface": "pub",
        "id": "ether-de:00:b0:00:00:00",
        "last_time_reachable": 1607125599,
        "primary_name_manual": False,
        "default_name": "",
        "l3connectivities": [
            {
                "addr": "192.168.1.181",
                "active": False,
                "reachable": False,
                "last_activity": 1607125599,
                "af": "ipv4",
                "last_time_reachable": 1607125599,
            },
            {
                "addr": "192.168.1.182",
                "active": False,
                "reachable": False,
                "last_activity": 1605958758,
                "af": "ipv4",
                "last_time_reachable": 1605958758,
            },
            {
                "addr": "2a01:e34:eda1:eb40:dc00:b0ff:fedf:e30",
                "active": False,
                "reachable": False,
                "last_activity": 1607125594,
                "af": "ipv6",
                "last_time_reachable": 1607125594,
            },
        ],
        "reachable": False,
        "last_activity": 1607125599,
        "primary_name": "",
    },
    {
        "l2ident": {"id": "DC:00:B0:00:00:00", "type": "mac_address"},
        "active": True,
        "persistent": False,
        "names": [
            {"name": "Repeteur-Wifi-Freebox", "source": "mdns"},
            {"name": "Repeteur Wifi Freebox", "source": "mdns_srv"},
        ],
        "vendor_name": "",
        "host_type": "freebox_wifi",
        "interface": "pub",
        "id": "ether-dc:00:b0:00:00:00",
        "last_time_reachable": 1614107678,
        "primary_name_manual": False,
        "l3connectivities": [
            {
                "addr": "192.168.1.145",
                "active": True,
                "reachable": True,
                "last_activity": 1614107678,
                "af": "ipv4",
                "last_time_reachable": 1614107678,
            },
            {
                "addr": "fe80::de00:b0ff:fe52:6ef6",
                "active": True,
                "reachable": True,
                "last_activity": 1614107608,
                "af": "ipv6",
                "last_time_reachable": 1614107603,
            },
            {
                "addr": "2a01:e34:eda1:eb40:de00:b0ff:fe52:6ef6",
                "active": True,
                "reachable": True,
                "last_activity": 1614107618,
                "af": "ipv6",
                "last_time_reachable": 1614107618,
            },
        ],
        "default_name": "Repeteur Wifi Freebox",
        "model": "fbxwmr",
        "reachable": True,
        "last_activity": 1614107678,
        "primary_name": "Repeteur Wifi Freebox",
    },
    {
        "l2ident": {"id": "5E:65:55:00:00:00", "type": "mac_address"},
        "active": False,
        "persistent": False,
        "names": [
            {"name": "iPhoneofQuentin", "source": "dhcp"},
            {"name": "iPhone-of-Quentin", "source": "mdns"},
        ],
        "vendor_name": "",
        "host_type": "smartphone",
        "interface": "pub",
        "id": "ether-5e:65:55:00:00:00",
        "last_time_reachable": 1612611982,
        "primary_name_manual": False,
        "default_name": "iPhonedeQuentin",
        "l3connectivities": [
            {
                "addr": "192.168.1.148",
                "active": False,
                "reachable": False,
                "last_activity": 1612611973,
                "af": "ipv4",
                "last_time_reachable": 1612611973,
            },
            {
                "addr": "fe80::14ca:6c30:938b:e281",
                "active": False,
                "reachable": False,
                "last_activity": 1609693223,
                "af": "ipv6",
                "last_time_reachable": 1609693223,
            },
            {
                "addr": "fe80::1c90:2b94:1ba2:bd8b",
                "active": False,
                "reachable": False,
                "last_activity": 1610797303,
                "af": "ipv6",
                "last_time_reachable": 1610797303,
            },
            {
                "addr": "fe80::8c8:e58b:838e:6785",
                "active": False,
                "reachable": False,
                "last_activity": 1612611951,
                "af": "ipv6",
                "last_time_reachable": 1612611946,
            },
            {
                "addr": "2a01:e34:eda1:eb40:f0e7:e198:3a69:58",
                "active": False,
                "reachable": False,
                "last_activity": 1609693245,
                "af": "ipv6",
                "last_time_reachable": 1609693245,
            },
            {
                "addr": "2a01:e34:eda1:eb40:1dc4:c6f8:aa20:c83b",
                "active": False,
                "reachable": False,
                "last_activity": 1610797176,
                "af": "ipv6",
                "last_time_reachable": 1610797176,
            },
            {
                "addr": "2a01:e34:eda1:eb40:6cf6:5811:1770:c662",
                "active": False,
                "reachable": False,
                "last_activity": 1612611982,
                "af": "ipv6",
                "last_time_reachable": 1612611982,
            },
            {
                "addr": "2a01:e34:eda1:eb40:438:9b2c:4f8f:f48a",
                "active": False,
                "reachable": False,
                "last_activity": 1612611946,
                "af": "ipv6",
                "last_time_reachable": 1612611946,
            },
        ],
        "reachable": False,
        "last_activity": 1612611982,
        "primary_name": "iPhoneofQuentin",
    },
]