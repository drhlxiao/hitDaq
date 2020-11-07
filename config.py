#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
 configuration file
'''
commands = {
    'basicOperationGroup':
        [

            {
                'name': 'Initialization',
                'button_title': 'Initialization',
                'sequence': [
                    ('set_register', 0x20,  0x000F,  "Heaters off"),
                    ('set_register', 0x40, 0x4E10,  "Setting DAC: BIAS to 0.8V"),
                    ('set_register', 0x4B, 0x9FFF,  "Setting DAC: ROFS to 1.595V"),
                    ('set_register', 0x4F, 0x0C0F,
                     "Setting DRS4 config register to 0xFF"),
                    ('set_register', 0x4F, 0x0D0F,
                     "Setting DRS4 write shift register to 0xFF"),
                ],
                'type':'inline',
                'inputs':None,
            },

            {
                'name': 'start_calibration',
                'button_title': 'Start calibration',
                'sequence':
                [
                    ('set_register', 0x4D, 0x51EB,  "Setting DAC: CAL- to 0.8V"),
                    ('set_register', 0x4C, 0x51EB, "Setting DAC: CAL+ to 0.8V"),
                    ('set_register', 0x4E, 0x0003, "Starting calibration source"),
                ],
            },
            {
                'name': 'stop_calibration',
                'button_title': 'Stop calibration',
                'sequence':

                [
                    ('set_register', 0x4E, 0x0000, "Stopping calibration source"),
                ],
            },
            {

                'name': 'read_temperatures',
                'button_title': 'Read temperatures',
                'type': 'inline',
                'inputs': None,

                'sequence': [
                    ('get_register', 0x21,
                     "Reading the temperature from I2C device 0x90", 'comm._decode_temp'),
                    ('get_register', 0x22,
                     "Reading the temperature from I2C device 0x92", 'comm._decode_temp'),
                ],
            },
            {
                'name': 'read_status',
                'button_title': 'Read status',
                'type': 'inline',
                'inputs': None,
                'sequence': [
                    ('get_register', 0x02, "Reading the status", 'comm.decode_status'),
                ],
            },
            {
                'name': 'last_command',
                'button_title': 'Last command',
                'type': 'inline',
                'inputs': None,
                'sequence':
                [
                    ('get_register', 0x50, "Reading the last command"),
                    ('get_register', 0x51, "Reading the data from last command"),
                    ('get_register', 0x52, "Reading the commands counter"),
                ],
            },
            {
                'name': 'enable_Full_mode',
                'button_title': 'Enable Full mode',
                'sequence': [
                    ('set_register', 0x81, 0x01FF,  "Enabling all channels"),
                    ('set_register', 0x80, 0x0003,
                        "Setting the full readout mode"),
                ],
            },
            {
                'name': 'enable_sequencer',
                'button_title': 'Enable sequencer',
                'type': 'inline',
                'inputs': None,
                'sequence':
                [
                    ('set_register', 0x0F, 0x01A0,
                        "Enable DRS4 sequencer"),
                ]
            },
            {

                'name': 'trigger_DRS_by_command',
                'button_title': 'Trigger DRS by command',
                'type': 'inline',
                'inputs': None,
                'sequence':
                [
                    ('set_register', 0x0F, 0x03A0,
                        "Enable DRS4 sequencer trigger"),
                    ('set_register', 0x0F, 0x01A0,
                        "Disable DRS4 sequencer trigger"),
                ]
            },

            {

                'name': 'disable_sequencer',
                'button_title': 'Disable sequencer',
                'type': 'inline',
                'inputs': None,
                'sequence':
                [
                    ('set_register', 0x0F, 0x00A0,
                        "Disable DRS4 sequencer"),
                ],
            },
        ],
    'readoutsGroup':
    [

            {
                'name': 'enable_ROI_mode',
                'button_title': 'Enable ROI mode',
                'label': 'ROI Readout Mode',
                'type': 'inline',
                'inputs': [
                    {'name': 'ROI_delay_input', 'tooltip': 'ROI delay',
                        'type': 'int', 'default': 200, 'min': 0, 'max': 65535},
                    {'name': 'ROI_length_input', 'tooltip': 'Read length',
                        'type': 'int', 'default': 100, 'min': 0, 'max': 65535},
                ],
                'sequence':   [
                    ('set_register', 0x80, 0x0001,
                        "Setting the full readout mode"),
                    ('set_register', 0x81, 0x01FF,  "Enabling all channels"),
                    ('set_register', 0x82, 'ROI_delay_input',
                        "Setting the delay to {ROI_delay_input}"),
                    ('set_register', 0x83, 'ROI_length_input',
                        "Setting the readout length to {ROI_length_input}"),
                ]
            },
            {
                'name': 'enable_smart_mode',
                'button_title': 'Enable Smart Mode',
                'type': 'inline',
                'label': 'Smart Readout Mode',
                'inputs': [{'name': 'smart_read_length', 'tooltip': 'Smart read length', 'type': 'int', 'default': 100, 'colspan': 1, 'max': 65535},
                           {'name': 'smart_read_start_cell', 'tooltip': 'Smart read start cell',
                               'type': 'int', 'default': 300, 'colspan': 1, 'max': 65535},
                           ],
                'sequence': [
                    ('set_register', 0x80, 0x0002,
                        "Setting the full readout mode"),
                    ('set_register', 0x81, 0x01FF,
                        "Enabling all channels"),
                    ('set_register', 0x83, 'smart_read_length',
                        "Setting the readout length to {smart_read_length}"),
                    ('set_register', 0x84, 'smart_read_start_cell',
                        "Setting the start cell to {smart_read_start_cell}"),
                ],
            },

            {
                'name': 'burst_read',
                'button_title': 'Burst read',
                'label': 'Burst readout mode',
                'type': 'row',
                'tooltip': 'burst read ',
                'inputs': [{'type': 'int', 'name': 'nb_burst_reads', 'tooltip': 'Nb. of reads', 'default': 100, 'colspan': 2, 'max': 1024*9}],

                'sequence': [
                    ('set_register', 0x72, 'nb_burst_reads',
                        "Setting the burst readout length to {nb_burst_reads} "),
                    ('get_burst_from_register', 0x71,
                        "Burst read of words from register"),
                ]
            }
        ]
}


buttons = {
    'registers': [
        {
            "name": "constant",
            "address": "0x00",
            "Operation": "read",
            "Default": "0xCAFE"
        },
        {
            "name": "dummy",
            "address": "0x01",
            "Operation": "rw",
            "Default": "0xC0DE"
        },
        {
            "name": "status",
            "address": "0x02",
            "Operation": "read",
            "Default": ""
        },
        {
            "name": "triggers",
            "address": "0x06",
            "Operation": "read",
            "Default": "external signals"
        },
        {
            "name": "timestamp",
            "address": "0x0E",
            "Operation": "read",
            "Default": "0x0000"
        },
        {
            "name": "operation",
            "address": "0x0F",
            "Operation": "rw",
            "Default": "0x0004"
        },
        {
            "name": "heaters",
            "address": "0x20",
            "Operation": "rw",
            "Default": "0x00FF"
        },
        {
            "name": "temp_90",
            "address": "0x21",
            "Operation": "read",
            "Default": "0x0000",
        },
        {
            "name": "temp_92",
            "address": "0x22",
            "Operation": "read",
            "Default": "0x0000"
        },
        {
            "name": "dac_hv1",
            "address": "0x30",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_hv2",
            "address": "0x31",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_hv3",
            "address": "0x32",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_hv4",
            "address": "0x33",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_hv5",
            "address": "0x34",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_hv6",
            "address": "0x35",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_hv7",
            "address": "0x36",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_hv8",
            "address": "0x37",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_tlevel1",
            "address": "0x38",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_tlevel2",
            "address": "0x39",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_tlevel3",
            "address": "0x3A",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_tlevel4",
            "address": "0x3B",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_tlevel5",
            "address": "0x3C",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_tlevel6",
            "address": "0x3D",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_tlevel7",
            "address": "0x3E",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_tlevel8",
            "address": "0x3F",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_bias",
            "address": "0x40",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_va",
            "address": "0x41",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_vb",
            "address": "0x42",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_rofs",
            "address": "0x4B",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_calp",
            "address": "0x4C",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "dac_calm",
            "address": "0x4D",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "calibration",
            "address": "0x4E",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "drs_config",
            "address": "0x4F",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "last_command",
            "address": "0x50",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "last_data",
            "address": "0x51",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "command_count",
            "address": "0x52",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "sram_data",
            "address": "0x60",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "sram_data_inc",
            "address": "0x61",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "sram_address_row",
            "address": "0x62",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "sram_address_col",
            "address": "0x63",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "sram_pointer_write",
            "address": "0x64",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "sram_pointer_read",
            "address": "0x65",
            "Operation": "read",
                    "Default": "not yet implemented"
        },
        {
            "name": "sram_demo_data",
            "address": "0x6E",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "sram_data_burst",
            "address": "0x6F",
            "Operation": "write",
                    "Default": "0x0000"
        },
        {
            "name": "fifo",
            "address": "0x70",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "fifo_burst",
            "address": "0x71",
            "Operation": "read",
                    "Default": "0x000A"
        },
        {
            "name": "fifo_burst_length",
            "address": "0x72",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "readout_mode",
            "address": "0x80",
            "Operation": "rw",
                    "Default": "0x0003"
        },
        {
            "name": "readout_channels",
            "address": "0x81",
            "Operation": "rw",
                    "Default": "0x01FF"
        },
        {
            "name": "readout_delay",
            "address": "0x82",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "readout_length",
            "address": "0x83",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "readout_start",
            "address": "0x84",
            "Operation": "rw",
                    "Default": "0x0000"
        },
        {
            "name": "counter_pattern_0",
            "address": "0xD0",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "counter_pattern_1",
            "address": "0xD1",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "counter_pattern_2",
            "address": "0xD2",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "counter_pattern_3",
            "address": "0xD3",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "counter_pattern_4",
            "address": "0xD4",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "counter_pattern_5",
            "address": "0xD5",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "counter_pattern_6",
            "address": "0xD6",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "counter_pattern_7",
            "address": "0xD7",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "counter_trigger_0",
            "address": "0xD8",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "counter_trigger_1",
            "address": "0xD9",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "counter_trigger_2",
            "address": "0xDA",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "counter_trigger_3",
            "address": "0xDB",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "counter_trigger_4",
            "address": "0xDC",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "counter_trigger_5",
            "address": "0xDD",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "counter_trigger_6",
            "address": "0xDE",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "counter_trigger_7",
            "address": "0xDF",
            "Operation": "read",
                    "Default": "0x0000"
        },
        {
            "name": "pattern_0",
            "address": "0xE0",
            "Operation": "rw",
                    "Default": "0x00FF"
        },
        {
            "name": "pattern_1",
            "address": "0xE1",
            "Operation": "rw",
                    "Default": "0x00FF"
        },
        {
            "name": "pattern_2",
            "address": "0xE2",
            "Operation": "rw",
                    "Default": "0x00FF"
        },
        {
            "name": "pattern_3",
            "address": "0xE3",
            "Operation": "read/write",
                    "Default": "0x00FF"
        },
        {
            "name": "pattern_4",
            "address": "0xE4",
            "Operation": "read/write",
                    "Default": "0x00FF"
        },
        {
            "name": "pattern_5",
            "address": "0xE5",
            "Operation": "read/write",
                    "Default": "0x00FF"
        },
        {
            "name": "pattern_6",
            "address": "0xE6",
            "Operation": "read/write",
                    "Default": "0x00FF"
        },
        {
            "name": "pattern_7",
            "address": "0xE7",
            "Operation": "read/write",
                    "Default": "0x00FF"
        },
        {
            "name": "debug_1",
            "address": "0xF1",
            "Operation": "read",
                    "Default": "depends on application"
        },
        {
            "name": "debug_2",
            "address": "0xF2",
            "Operation": "read",
                    "Default": "depends on application"
        },
        {
            "name": "debug",
            "address": "0xFF",
            "Operation": "read",
                    "Default": "depends on application"
        }
    ]
}
