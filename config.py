#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
 configuration file
'''
commands = {
        'basicOperationGroup':
        {
            'container':'basicOperationGroup',
            'grid_columns': 5,
            'sequences': [

                {
                    'name': 'Initialization',
                    'button_title': 'Initialization',
                    'sequence': [
                        (('_sequence_write',), (0x20,  0x000F),  "Heaters off"),
                        (('_sequence_write',), (0x40, 0x4E10),
                            "Setting DAC: BIAS to 0.8V"),
                        (('_sequence_write',), (0x4B, 0x9FFF),
                            "Setting DAC: ROFS to 1.595V"),
                        (('_sequence_write',), (0x4F, 0x0C0F),
                            "Setting DRS4 config register to 0xFF"),
                        (('_sequence_write',), (0x4F, 0x0D0F),
                            "Setting DRS4 write shift register to 0xFF"),
                        ],
                    'layout':'inline', #inline or row, not create in a new line
                    'inputs':None,
                    'type':'read', #widget type
                    },

                {
                    'name': 'start_calibration',
                    'button_title': 'Start calibration',
                    'sequence':
                    [
                        (('_sequence_write',), (0x4D, 0x51EB),
                            "Setting DAC: CAL- to 0.8V"),
                        (('_sequence_write',), (0x4C, 0x51EB),
                            "Setting DAC: CAL+ to 0.8V"),
                        (('_sequence_write',), (0x4E, 0x0003),
                            "Starting calibration source"),
                        ],
                    },
                {
                    'name': 'stop_calibration',
                    'button_title': 'Stop calibration',
                    'sequence':

                    [
                        (('_sequence_write',), (0x4E, 0x0000),
                            "Stopping calibration source"),
                        ],
                    },
                {

                    'name': 'read_temperatures',
                    'button_title': 'Read temperatures',
                    'layout': 'inline',
                    'inputs': None,

                    'sequence': [
                        (('_sequence_read', '_decode_temp'), (0x21,),
                            "Reading the temperature from I2C device 0x90"),
                        (('_sequence_read', '_decode_temp'), (0x22,),
                            "Reading the temperature from I2C device 0x92"),  # callback
                        ],
                    },
                {
                        'name': 'read_status',
                        'button_title': 'Read status',
                        'layout': 'inline',
                        'inputs': None,
                        'sequence': [
                            (('_sequence_read', 'decode_status'),
                                (0x02,), "Reading the status"),
                            ],
                        },
                {
                        'name': 'last_command',
                        'button_title': 'Last command',
                        'layout': 'inline',
                        'inputs': None,
                        'sequence':
                        [
                            (('_sequence_read',), (0x50,),
                                "Reading the last command"),
                            (('_sequence_read',), (0x51,),
                                "Reading the data from last command"),
                            (('_sequence_read',), (0x52,),
                                "Reading the commands counter"),
                            ],
                        },
                {
                        'name': 'enable_Full_mode',
                        'button_title': 'Enable Full mode',
                        'sequence': [
                            (('_sequence_write',), (0x81, 0x01FF),
                                "Enabling all channels"),
                            (('_sequence_write',), (0x80, 0x0003),
                                "Setting the full readout mode"),
                            ],
                        },
                {
                        'name': 'enable_sequencer',
                        'button_title': 'Enable sequencer',
                        'layout': 'inline',
                        'inputs': None,
                        'sequence':
                        [
                            (('_sequence_write',), (0x0F, 0x01A0),
                                "Enable DRS4 sequencer"),
                            ]
                        },
                {

                        'name': 'trigger_DRS_by_command',
                        'button_title': 'Trigger DRS by command',
                        'layout': 'inline',
                        'inputs': None,
                        'sequence':
                        [
                            (('_sequence_write',), (0x0F, 0x03A0),
                                "Enable DRS4 sequencer trigger"),
                            (('_sequence_write',), (0x0F, 0x01A0),
                                "Disable DRS4 sequencer trigger"),
                            ]
                        },

                {

                        'name': 'disable_sequencer',
                        'button_title': 'Disable sequencer',
                        'layout': 'inline',
                        'inputs': None,
                        'sequence':
                        [
                            (('_sequence_write',), (0x0F, 0x00A0),
                                "Disable DRS4 sequencer"),
                            ],
                        },
                ]
        },
    'readoutsGroup':
        {
                'container':'readoutsGroup',
                'grid_columns': 4,
                'sequences': [

                    {
                        'name': 'enable_ROI_mode',
                        'button_title': 'Enable ROI mode',
                        'label': 'ROI Readout Mode',
                        'thread_lock': True,  # disable button before its finish
                        'layout': 'row',
                        'inputs': [
                            {'name': 'ROI_delay_input', 'tooltip': 'ROI delay',
                                'type': 'int', 'default': 200, 'min': 0, 'max': 65535},
                            {'name': 'ROI_length_input', 'tooltip': 'Read length',
                                'type': 'int', 'default': 100, 'min': 0, 'max': 65535},
                            ],
                        'sequence':   [
                            (('_sequence_write',), (0x80, 0x0001),
                                "Setting the full readout mode"),
                            (('_sequence_write',), (0x81, 0x01FF),
                                "Enabling all channels"),
                            (('_sequence_write',), (0x82, 'ROI_delay_input'),
                                "Setting the delay to {ROI_delay_input}"),
                            (('_sequence_write',), (0x83, 'ROI_length_input'),
                                "Setting the readout length to {ROI_length_input}"),
                            ]
                        },
                    {
                        'name': 'enable_smart_mode',
                        'button_title': 'Enable Smart Mode',
                        'layout': 'row',
                        'thread_lock': True,  # disable button before its finish
                        'label': 'Smart Readout Mode',
                        'inputs': [{'name': 'smart_read_length', 'tooltip': 'Smart read length', 'type': 'int', 'default': 100, 'colspan': 1, 'max': 65535},
                            {'name': 'smart_read_start_cell', 'tooltip': 'Smart read start cell',
                                'type': 'int', 'default': 300, 'colspan': 1, 'max': 65535},
                            ],
                        'sequence': [
                            (('_sequence_write',), (0x80, 0x0002),
                                "Setting the full readout mode"),
                            (('_sequence_write',), (0x81, 0x01FF),
                                "Enabling all channels"),
                            (('_sequence_write',), (0x83, 'smart_read_length'),
                                "Setting the readout length to {smart_read_length}"),
                            (('_sequence_write',), (0x84, 'smart_read_start_cell'),
                                "Setting the start cell to {smart_read_start_cell}"),
                            ],
                        },

                    {
                        'name': 'burst_read',
                        'button_title': 'Burst read',
                        'label': 'Burst readout mode',
                        'layout':'row',
                        'type': 'read',
                        'thread_lock': True,  # disable button before its finish
                        'tooltip': 'burst read ',
                        'inputs': [{'type': 'int', 'name': 'nb_burst_reads', 'tooltip': 'Nb. of reads', 'default': 100, 'colspan': 2, 'max': 1024*9}],

                        'sequence': [
                            (('_sequence_write',), (0x72, 'nb_burst_reads'),
                                "Setting the burst readout length to {nb_burst_reads} "),
                            (('_burst_read',), (0x71,),
                                "Burst read of words from register"),
                            ]
                        }
                    ]
        },

    'readRegisterGroup': 
        {
                'container':'registerReadTab',
                'grid_columns': 5,
                'sequences': 
                [{'button_title': 'constant',
                    'inputs': None,
                    'label': 'constant',
                    'name': 'constant',
                    'sequence': [(('_sequence_read',),
                        (0,),
                        'constant (address=0x00)')],
                    'type': 'read'},
                    {'button_title': 'status',
                        'inputs': None,
                        'label': 'status',
                        'name': 'status',
                        'sequence': [(('_sequence_read',),
                            (2,),
                            'status (address=0x02)')],
                        'type': 'read'},
                    {'button_title': 'triggers',
                        'inputs': None,
                        'label': 'triggers',
                        'name': 'triggers',
                        'sequence': [(('_sequence_read',),
                            (6,),
                            'triggers (address=0x06)')],
                        'type': 'read'},
                    {'button_title': 'timestamp',
                        'inputs': None,
                        'label': 'timestamp',
                        'name': 'timestamp',
                        'sequence': [(('_sequence_read',),
                            (14,),
                            'timestamp '
                            '(address=0x0E)')],
                        'type': 'read'},
                    {'button_title': 'temp_90',
                        'inputs': None,
                        'label': 'temp 90',
                        'name': 'temp_90',
                        'sequence': [(('_sequence_read',),
                            (33,),
                            'temp_90 (address=0x21)')],
                        'type': 'read'},
                    {'button_title': 'temp_92',
                        'inputs': None,
                        'label': 'temp 92',
                        'name': 'temp_92',
                        'sequence': [(('_sequence_read',),
                            (34,),
                            'temp_92 (address=0x22)')],
                        'type': 'read'},
                    {'button_title': 'last_data',
                        'inputs': None,
                        'label': 'last data',
                        'name': 'last_data',
                        'sequence': [(('_sequence_read',),
                            (81,),
                            'last_data '
                            '(address=0x51)')],
                        'type': 'read'},
                    {'button_title': 'command_count',
                            'inputs': None,
                            'label': 'command count',
                            'name': 'command_count',
                            'sequence': [(('_sequence_read',),
                                (82,),
                                'command_count '
                                '(address=0x52)')],
                            'type': 'read'},
                    {'button_title': 'sram_pointer_write',
                            'inputs': None,
                            'label': 'sram pointer write',
                            'name': 'sram_pointer_write',
                            'sequence': [(('_sequence_read',),
                                (100,),
                                'sram_pointer_write '
                                '(address=0x64)')],
                            'type': 'read'},
                    {'button_title': 'fifo',
                            'inputs': None,
                            'label': 'fifo',
                            'name': 'fifo',
                            'sequence': [(('_sequence_read',),
                                (112,),
                                'fifo (address=0x70)')],
                            'type': 'read'},
                    {'button_title': 'fifo_burst',
                            'inputs': None,
                            'label': 'fifo burst',
                            'name': 'fifo_burst',
                            'sequence': [(('_sequence_read',),
                                (113,),
                                'fifo_burst '
                                '(address=0x71)')],
                            'type': 'read'},
                    {'button_title': 'counter_pattern_0',
                            'inputs': None,
                            'label': 'counter pattern 0',
                            'name': 'counter_pattern_0',
                            'sequence': [(('_sequence_read',),
                                (208,),
                                'counter_pattern_0 '
                                '(address=0xD0)')],
                            'type': 'read'},
                    {'button_title': 'counter_pattern_1',
                            'inputs': None,
                            'label': 'counter pattern 1',
                            'name': 'counter_pattern_1',
                            'sequence': [(('_sequence_read',),
                                (209,),
                                'counter_pattern_1 '
                                '(address=0xD1)')],
                            'type': 'read'},
                    {'button_title': 'counter_pattern_2',
                            'inputs': None,
                            'label': 'counter pattern 2',
                            'name': 'counter_pattern_2',
                            'sequence': [(('_sequence_read',),
                                (210,),
                                'counter_pattern_2 '
                                '(address=0xD2)')],
                            'type': 'read'},
                    {'button_title': 'counter_pattern_3',
                            'inputs': None,
                            'label': 'counter pattern 3',
                            'name': 'counter_pattern_3',
                            'sequence': [(('_sequence_read',),
                                (211,),
                                'counter_pattern_3 '
                                '(address=0xD3)')],
                            'type': 'read'},
                    {'button_title': 'counter_pattern_4',
                            'inputs': None,
                            'label': 'counter pattern 4',
                            'name': 'counter_pattern_4',
                            'sequence': [(('_sequence_read',),
                                (212,),
                                'counter_pattern_4 '
                                '(address=0xD4)')],
                            'type': 'read'},
                    {'button_title': 'counter_pattern_5',
                            'inputs': None,
                            'label': 'counter pattern 5',
                            'name': 'counter_pattern_5',
                            'sequence': [(('_sequence_read',),
                                (213,),
                                'counter_pattern_5 '
                                '(address=0xD5)')],
                            'type': 'read'},
                    {'button_title': 'counter_pattern_6',
                            'inputs': None,
                            'label': 'counter pattern 6',
                            'name': 'counter_pattern_6',
                            'sequence': [(('_sequence_read',),
                                (214,),
                                'counter_pattern_6 '
                                '(address=0xD6)')],
                            'type': 'read'},
                    {'button_title': 'counter_pattern_7',
                            'inputs': None,
                            'label': 'counter pattern 7',
                            'name': 'counter_pattern_7',
                            'sequence': [(('_sequence_read',),
                                (215,),
                                'counter_pattern_7 '
                                '(address=0xD7)')],
                            'type': 'read'},
                    {'button_title': 'counter_trigger_0',
                            'inputs': None,
                            'label': 'counter trigger 0',
                            'name': 'counter_trigger_0',
                            'sequence': [(('_sequence_read',),
                                (216,),
                                'counter_trigger_0 '
                                '(address=0xD8)')],
                            'type': 'read'},
                    {'button_title': 'counter_trigger_1',
                            'inputs': None,
                            'label': 'counter trigger 1',
                            'name': 'counter_trigger_1',
                            'sequence': [(('_sequence_read',),
                                (217,),
                                'counter_trigger_1 '
                                '(address=0xD9)')],
                            'type': 'read'},
                    {'button_title': 'counter_trigger_2',
                            'inputs': None,
                            'label': 'counter trigger 2',
                            'name': 'counter_trigger_2',
                            'sequence': [(('_sequence_read',),
                                (218,),
                                'counter_trigger_2 '
                                '(address=0xDA)')],
                            'type': 'read'},
                    {'button_title': 'counter_trigger_3',
                            'inputs': None,
                            'label': 'counter trigger 3',
                            'name': 'counter_trigger_3',
                            'sequence': [(('_sequence_read',),
                                (219,),
                                'counter_trigger_3 '
                                '(address=0xDB)')],
                            'type': 'read'},
                    {'button_title': 'counter_trigger_4',
                            'inputs': None,
                            'label': 'counter trigger 4',
                            'name': 'counter_trigger_4',
                            'sequence': [(('_sequence_read',),
                                (220,),
                                'counter_trigger_4 '
                                '(address=0xDC)')],
                            'type': 'read'},
                    {'button_title': 'counter_trigger_5',
                            'inputs': None,
                            'label': 'counter trigger 5',
                            'name': 'counter_trigger_5',
                            'sequence': [(('_sequence_read',),
                                (221,),
                                'counter_trigger_5 '
                                '(address=0xDD)')],
                            'type': 'read'},
                    {'button_title': 'counter_trigger_6',
                            'inputs': None,
                            'label': 'counter trigger 6',
                            'name': 'counter_trigger_6',
                            'sequence': [(('_sequence_read',),
                                (222,),
                                'counter_trigger_6 '
                                '(address=0xDE)')],
                            'type': 'read'},
                    {'button_title': 'counter_trigger_7',
                            'inputs': None,
                            'label': 'counter trigger 7',
                            'name': 'counter_trigger_7',
                            'sequence': [(('_sequence_read',),
                                (223,),
                                'counter_trigger_7 '
                                '(address=0xDF)')],
                            'type': 'read'},
                    {'button_title': 'debug_1',
                            'inputs': None,
                            'label': 'debug 1',
                            'name': 'debug_1',
                            'sequence': [(('_sequence_read',),
                                (241,),
                                'debug_1 (address=0xF1)')],
                            'type': 'read'},
                    {'button_title': 'debug_2',
                            'inputs': None,
                            'label': 'debug 2',
                            'name': 'debug_2',
                            'sequence': [(('_sequence_read',),
                                (242,),
                                'debug_2 (address=0xF2)')],
                            'type': 'read'},
                    {'button_title': 'debug',
                            'inputs': None,
                            'label': 'debug',
                            'name': 'debug',
                            'sequence': [(('_sequence_read',),
                                (255,),
                                'debug (address=0xFF)')],
                            'type': 'read'}
                    ]
                                        },
            }
commands_disabled={
        'readWriteRegisterGroup': 
        {
            'container':'registerReadWriteTab',
            'grid_columns': 4,
            'sequences': 
            [
                {'button_title': 'operation',
                    'inputs': [{'default': 4,
                        'max': 65535,
                        'name': 'operation_input',
                        'tooltip': 'value write '
                        'to '
                        '"operation '
                        '(addr=0x0F)"',
                        'colspan':1,
                        'type': 'int'}],
                    'label': 'operation',
                    'name': 'operation',
                    'sequence': [(('_sequence_write',),
                        (15,
                            'operation_input'),
                        'operation '
                        '(reg=0x0F)')],
                    'type': 'rw'},
                {'button_title': 'heaters',
                    'inputs': [{'default': 255,
                        'max': 65535,
                        'colspan':1,
                        'name': 'heaters_input',
                        'tooltip': 'value write '
                        'to "heaters '
                        '(addr=0x20)"',
                        'type': 'int'}],
                    'label': 'heaters',
                    'name': 'heaters',
                    'sequence': [(('_sequence_write',),
                        (32, 'heaters_input'),
                        'heaters (reg=0x20)')],
                    'type': 'rw'},
                {'button_title': 'dac_hv1',
                    'inputs': [{'default': 0,
                        'max': 65535,
                        'colspan':1,
                        'name': 'dac_hv1_input',
                        'tooltip': 'value write '
                        'to "dac_hv1 '
                        '(addr=0x30)"',
                        'type': 'int'}],
                    'label': 'dac hv1',
                    'name': 'dac_hv1',
                    'sequence': [(('_sequence_write',),
                        (48, 'dac_hv1_input'),
                        'dac_hv1 (reg=0x30)')],
                    'type': 'rw'},
                {'button_title': 'dac_hv2',
                    'inputs': [{'default': 0,
                        'max': 65535,
                        'colspan':1,
                        'name': 'dac_hv2_input',
                        'tooltip': 'value write '
                        'to "dac_hv2 '
                        '(addr=0x31)"',
                        'type': 'int'}],
                    'label': 'dac hv2',
                    'name': 'dac_hv2',
                    'sequence': [(('_sequence_write',),
                        (49, 'dac_hv2_input'),
                        'dac_hv2 (reg=0x31)')],
                    'type': 'rw'},
                {'button_title': 'dac_hv3',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'dac_hv3_input',
                            'tooltip': 'value write '
                            'to "dac_hv3 '
                            '(addr=0x32)"',
                            'type': 'int'}],
                        'label': 'dac hv3',
                        'name': 'dac_hv3',
                        'sequence': [(('_sequence_write',),
                            (50, 'dac_hv3_input'),
                            'dac_hv3 (reg=0x32)')],
                        'type': 'rw'},
                {'button_title': 'dac_hv4',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'dac_hv4_input',
                            'tooltip': 'value write '
                            'to "dac_hv4 '
                            '(addr=0x33)"',
                            'type': 'int'}],
                        'label': 'dac hv4',
                        'name': 'dac_hv4',
                        'sequence': [(('_sequence_write',),
                            (51, 'dac_hv4_input'),
                            'dac_hv4 (reg=0x33)')],
                        'type': 'rw'},
                {'button_title': 'dac_hv5',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'name': 'dac_hv5_input',
                            'colspan':1,
                            'tooltip': 'value write '
                            'to "dac_hv5 '
                            '(addr=0x34)"',
                            'type': 'int'}],
                        'label': 'dac hv5',
                        'name': 'dac_hv5',
                        'sequence': [(('_sequence_write',),
                            (52, 'dac_hv5_input'),
                            'dac_hv5 (reg=0x34)')],
                        'type': 'rw'},
                {'button_title': 'dac_hv6',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'name': 'dac_hv6_input',
                            'colspan':1,
                            'tooltip': 'value write '
                            'to "dac_hv6 '
                            '(addr=0x35)"',
                            'type': 'int'}],
                        'label': 'dac hv6',
                        'name': 'dac_hv6',
                        'sequence': [(('_sequence_write',),
                            (53, 'dac_hv6_input'),
                            'dac_hv6 (reg=0x35)')],
                        'type': 'rw'},
                {'button_title': 'dac_hv7',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'dac_hv7_input',
                            'tooltip': 'value write '
                            'to "dac_hv7 '
                            '(addr=0x36)"',
                            'type': 'int'}],
                        'label': 'dac hv7',
                        'name': 'dac_hv7',
                        'sequence': [(('_sequence_write',),
                            (54, 'dac_hv7_input'),
                            'dac_hv7 (reg=0x36)')],
                        'type': 'rw'},
                {'button_title': 'dac_hv8',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'name': 'dac_hv8_input',
                            'colspan':1,
                            'tooltip': 'value write '
                            'to "dac_hv8 '
                            '(addr=0x37)"',
                            'type': 'int'}],
                        'label': 'dac hv8',
                        'name': 'dac_hv8',
                        'sequence': [(('_sequence_write',),
                            (55, 'dac_hv8_input'),
                            'dac_hv8 (reg=0x37)')],
                        'type': 'rw'},
                {'button_title': 'dac_tlevel1',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'dac_tlevel1_input',
                            'tooltip': 'value write '
                            'to '
                            '"dac_tlevel1 '
                            '(addr=0x38)"',
                            'type': 'int'}],
                        'label': 'dac tlevel1',
                        'name': 'dac_tlevel1',
                        'sequence': [(('_sequence_write',),
                            (56,
                                'dac_tlevel1_input'),
                            'dac_tlevel1 '
                            '(reg=0x38)')],
                        'type': 'rw'},
                {'button_title': 'dac_tlevel2',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'dac_tlevel2_input',
                            'tooltip': 'value write '
                            'to '
                            '"dac_tlevel2 '
                            '(addr=0x39)"',
                            'type': 'int'}],
                        'label': 'dac tlevel2',
                        'name': 'dac_tlevel2',
                        'sequence': [(('_sequence_write',),
                            (57,
                                'dac_tlevel2_input'),
                            'dac_tlevel2 '
                            '(reg=0x39)')],
                        'type': 'rw'},
                {'button_title': 'dac_tlevel3',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'dac_tlevel3_input',
                            'tooltip': 'value write '
                            'to '
                            '"dac_tlevel3 '
                            '(addr=0x3A)"',
                            'type': 'int'}],
                        'label': 'dac tlevel3',
                        'name': 'dac_tlevel3',
                        'sequence': [(('_sequence_write',),
                            (58,
                                'dac_tlevel3_input'),
                            'dac_tlevel3 '
                            '(reg=0x3A)')],
                        'type': 'rw'},
                {'button_title': 'dac_tlevel4',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'dac_tlevel4_input',
                            'tooltip': 'value write '
                            'to '
                            '"dac_tlevel4 '
                            '(addr=0x3B)"',
                            'type': 'int'}],
                        'label': 'dac tlevel4',
                        'name': 'dac_tlevel4',
                        'sequence': [(('_sequence_write',),
                            (59,
                                'dac_tlevel4_input'),
                            'dac_tlevel4 '
                            '(reg=0x3B)')],
                        'type': 'rw'},
                {'button_title': 'dac_tlevel5',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'dac_tlevel5_input',
                            'tooltip': 'value write '
                            'to '
                            '"dac_tlevel5 '
                            '(addr=0x3C)"',
                            'type': 'int'}],
                        'label': 'dac tlevel5',
                        'name': 'dac_tlevel5',
                        'sequence': [(('_sequence_write',),
                            (60,
                                'dac_tlevel5_input'),
                            'dac_tlevel5 '
                            '(reg=0x3C)')],
                        'type': 'rw'},
                {'button_title': 'dac_tlevel6',
                        'inputs': [{'default': 0,
                            'colspan':1,
                            'max': 65535,
                            'name': 'dac_tlevel6_input',
                            'tooltip': 'value write '
                            'to '
                            '"dac_tlevel6 '
                            '(addr=0x3D)"',
                            'type': 'int'}],
                        'label': 'dac tlevel6',
                        'name': 'dac_tlevel6',
                        'sequence': [(('_sequence_write',),
                            (61,
                                'dac_tlevel6_input'),
                            'dac_tlevel6 '
                            '(reg=0x3D)')],
                        'type': 'rw'},
                {'button_title': 'dac_tlevel7',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'dac_tlevel7_input',
                            'tooltip': 'value write '
                            'to '
                            '"dac_tlevel7 '
                            '(addr=0x3E)"',
                            'type': 'int'}],
                        'label': 'dac tlevel7',
                        'name': 'dac_tlevel7',
                        'sequence': [(('_sequence_write',),
                            (62,
                                'dac_tlevel7_input'),
                            'dac_tlevel7 '
                            '(reg=0x3E)')],
                        'type': 'rw'},
                {'button_title': 'dac_tlevel8',
                        'inputs': [{'default': 0,
                            'colspan':1,
                            'max': 65535,
                            'name': 'dac_tlevel8_input',
                            'tooltip': 'value write '
                            'to '
                            '"dac_tlevel8 '
                            '(addr=0x3F)"',
                            'type': 'int'}],
                        'label': 'dac tlevel8',
                        'name': 'dac_tlevel8',
                        'sequence': [(('_sequence_write',),
                            (63,
                                'dac_tlevel8_input'),
                            'dac_tlevel8 '
                            '(reg=0x3F)')],
                        'type': 'rw'},
                {'button_title': 'dac_bias',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'dac_bias_input',
                            'tooltip': 'value write '
                            'to '
                            '"dac_bias '
                            '(addr=0x40)"',
                            'type': 'int'}],
                        'label': 'dac bias',
                        'name': 'dac_bias',
                        'sequence': [(('_sequence_write',),
                            (64, 'dac_bias_input'),
                            'dac_bias '
                            '(reg=0x40)')],
                        'type': 'rw'},
                {'button_title': 'dac_va',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'dac_va_input',
                            'tooltip': 'value write '
                            'to "dac_va '
                            '(addr=0x41)"',
                            'type': 'int'}],
                        'label': 'dac va',
                        'name': 'dac_va',
                        'sequence': [(('_sequence_write',),
                            (65, 'dac_va_input'),
                            'dac_va (reg=0x41)')],
                        'type': 'rw'},
                {'button_title': 'dac_vb',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'dac_vb_input',
                            'tooltip': 'value write '
                            'to "dac_vb '
                            '(addr=0x42)"',
                            'type': 'int'}],
                        'label': 'dac vb',
                        'name': 'dac_vb',
                        'sequence': [(('_sequence_write',),
                            (66, 'dac_vb_input'),
                            'dac_vb (reg=0x42)')],
                        'type': 'rw'},
                {'button_title': 'dac_rofs',
                        'inputs': [{'default': 0,
                            'colspan':1,
                            'max': 65535,
                            'name': 'dac_rofs_input',
                            'tooltip': 'value write '
                            'to '
                            '"dac_rofs '
                            '(addr=0x4B)"',
                            'type': 'int'}],
                        'label': 'dac rofs',
                        'name': 'dac_rofs',
                        'sequence': [(('_sequence_write',),
                            (75, 'dac_rofs_input'),
                            'dac_rofs '
                            '(reg=0x4B)')],
                        'type': 'rw'},
                {'button_title': 'dac_calp',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'dac_calp_input',
                            'tooltip': 'value write '
                            'to '
                            '"dac_calp '
                            '(addr=0x4C)"',
                            'type': 'int'}],
                        'label': 'dac calp',
                        'name': 'dac_calp',
                        'sequence': [(('_sequence_write',),
                            (76, 'dac_calp_input'),
                            'dac_calp '
                            '(reg=0x4C)')],
                        'type': 'rw'},
                {'button_title': 'dac_calm',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'dac_calm_input',
                            'tooltip': 'value write '
                            'to '
                            '"dac_calm '
                            '(addr=0x4D)"',
                            'type': 'int'}],
                        'label': 'dac calm',
                        'name': 'dac_calm',
                        'sequence': [(('_sequence_write',),
                            (77, 'dac_calm_input'),
                            'dac_calm '
                            '(reg=0x4D)')],
                        'type': 'rw'},
                {'button_title': 'calibration',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'calibration_input',
                            'tooltip': 'value write '
                            'to '
                            '"calibration '
                            '(addr=0x4E)"',
                            'type': 'int'}],
                        'label': 'calibration',
                        'name': 'calibration',
                        'sequence': [(('_sequence_write',),
                            (78,
                                'calibration_input'),
                            'calibration '
                            '(reg=0x4E)')],
                        'type': 'rw'},
                {'button_title': 'drs_config',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'drs_config_input',
                            'tooltip': 'value write '
                            'to '
                            '"drs_config '
                            '(addr=0x4F)"',
                            'type': 'int'}],
                        'label': 'drs config',
                        'name': 'drs_config',
                        'sequence': [(('_sequence_write',),
                            (79,
                                'drs_config_input'),
                            'drs_config '
                            '(reg=0x4F)')],
                        'type': 'rw'},
                {'button_title': 'sram_data',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'sram_data_input',
                            'tooltip': 'value write '
                            'to '
                            '"sram_data '
                            '(addr=0x60)"',
                            'type': 'int'}],
                        'label': 'sram data',
                        'name': 'sram_data',
                        'sequence': [(('_sequence_write',),
                            (96,
                                'sram_data_input'),
                            'sram_data '
                            '(reg=0x60)')],
                        'type': 'rw'},
                {'button_title': 'sram_data_inc',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'sram_data_inc_input',
                            'tooltip': 'value write '
                            'to '
                            '"sram_data_inc '
                            '(addr=0x61)"',
                            'type': 'int'}],
                        'label': 'sram data inc',
                        'name': 'sram_data_inc',
                        'sequence': [(('_sequence_write',),
                            (97,
                                'sram_data_inc_input'),
                            'sram_data_inc '
                            '(reg=0x61)')],
                        'type': 'rw'},
                {'button_title': 'sram_address_row',
                        'inputs': [{'default': 0,
                            'colspan':1,
                            'max': 65535,
                            'name': 'sram_address_row_input',
                            'tooltip': 'value write '
                            'to '
                            '"sram_address_row '
                            '(addr=0x62)"',
                            'type': 'int'}],
                        'label': 'sram address row',
                        'name': 'sram_address_row',
                        'sequence': [(('_sequence_write',),
                            (98,
                                'sram_address_row_input'),
                            'sram_address_row '
                            '(reg=0x62)')],
                        'type': 'rw'},
                {'button_title': 'sram_address_col',
                        'inputs': [{'default': 0,
                            'colspan':1,
                            'max': 65535,
                            'name': 'sram_address_col_input',
                            'tooltip': 'value write '
                            'to '
                            '"sram_address_col '
                            '(addr=0x63)"',
                            'type': 'int'}],
                        'label': 'sram address col',
                        'name': 'sram_address_col',
                        'sequence': [(('_sequence_write',),
                            (99,
                                'sram_address_col_input'),
                            'sram_address_col '
                            '(reg=0x63)')],
                        'type': 'rw'},
                {'button_title': 'sram_demo_data',
                        'inputs': [{'default': 0,
                            'colspan':1,
                            'max': 65535,
                            'name': 'sram_demo_data_input',
                            'tooltip': 'value write '
                            'to '
                            '"sram_demo_data '
                            '(addr=0x6E)"',
                            'type': 'int'}],
                        'label': 'sram demo data',
                        'name': 'sram_demo_data',
                        'sequence': [(('_sequence_write',),
                            (110,
                                'sram_demo_data_input'),
                            'sram_demo_data '
                            '(reg=0x6E)')],
                        'type': 'rw'},
                {'button_title': 'fifo_burst_length',
                        'inputs': [{'default': 0,
                            'colspan':1,
                            'max': 65535,
                            'name': 'fifo_burst_length_input',
                            'tooltip': 'value write '
                            'to '
                            '"fifo_burst_length '
                            '(addr=0x72)"',
                            'type': 'int'}],
                        'label': 'fifo burst length',
                        'name': 'fifo_burst_length',
                        'sequence': [(('_sequence_write',),
                            (114,
                                'fifo_burst_length_input'),
                            'fifo_burst_length '
                            '(reg=0x72)')],
                        'type': 'rw'},
                {'button_title': 'readout_mode',
                        'inputs': [{'default': 3,
                            'max': 65535,
                            'colspan':1,
                            'name': 'readout_mode_input',
                            'tooltip': 'value write '
                            'to '
                            '"readout_mode '
                            '(addr=0x80)"',
                            'type': 'int'}],
                        'label': 'readout mode',
                        'name': 'readout_mode',
                        'sequence': [(('_sequence_write',),
                            (128,
                                'readout_mode_input'),
                            'readout_mode '
                            '(reg=0x80)')],
                        'type': 'rw'},
                {'button_title': 'readout_channels',
                        'inputs': [{'default': 511,
                            'colspan':1,
                            'max': 65535,
                            'name': 'readout_channels_input',
                            'tooltip': 'value write '
                            'to '
                            '"readout_channels '
                            '(addr=0x81)"',
                            'type': 'int'}],
                        'label': 'readout channels',
                        'name': 'readout_channels',
                        'sequence': [(('_sequence_write',),
                            (129,
                                'readout_channels_input'),
                            'readout_channels '
                            '(reg=0x81)')],
                        'type': 'rw'},
                {'button_title': 'readout_delay',
                        'inputs': [{'default': 0,
                            'colspan':1,
                            'max': 65535,
                            'name': 'readout_delay_input',
                            'tooltip': 'value write '
                            'to '
                            '"readout_delay '
                            '(addr=0x82)"',
                            'type': 'int'}],
                        'label': 'readout delay',
                        'name': 'readout_delay',
                        'sequence': [(('_sequence_write',),
                            (130,
                                'readout_delay_input'),
                            'readout_delay '
                            '(reg=0x82)')],
                        'type': 'rw'},
                {'button_title': 'readout_length',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'readout_length_input',
                            'tooltip': 'value write '
                            'to '
                            '"readout_length '
                            '(addr=0x83)"',
                            'type': 'int'}],
                        'label': 'readout length',
                        'name': 'readout_length',
                        'sequence': [(('_sequence_write',),
                            (131,
                                'readout_length_input'),
                            'readout_length '
                            '(reg=0x83)')],
                        'type': 'rw'},
                {'button_title': 'readout_start',
                        'inputs': [{'default': 0,
                            'max': 65535,
                            'colspan':1,
                            'name': 'readout_start_input',
                            'tooltip': 'value write '
                            'to '
                            '"readout_start '
                            '(addr=0x84)"',
                            'type': 'int'}],
                        'label': 'readout start',
                        'name': 'readout_start',
                        'sequence': [(('_sequence_write',),
                            (132,
                                'readout_start_input'),
                            'readout_start '
                            '(reg=0x84)')],
                        'type': 'rw'},
                {'button_title': 'pattern_0',
                        'inputs': [{'default': 255,
                            'max': 65535,
                            'colspan':1,
                            'name': 'pattern_0_input',
                            'tooltip': 'value write '
                            'to '
                            '"pattern_0 '
                            '(addr=0xE0)"',
                            'type': 'int'}],
                        'label': 'pattern 0',
                        'name': 'pattern_0',
                        'sequence': [(('_sequence_write',),
                            (224,
                                'pattern_0_input'),
                            'pattern_0 '
                            '(reg=0xE0)')],
                        'type': 'rw'},
                {'button_title': 'pattern_1',
                        'inputs': [{'default': 255,
                            'max': 65535,
                            'colspan':1,
                            'name': 'pattern_1_input',
                            'tooltip': 'value write '
                            'to '
                            '"pattern_1 '
                            '(addr=0xE1)"',
                            'type': 'int'}],
                        'label': 'pattern 1',
                        'name': 'pattern_1',
                        'sequence': [(('_sequence_write',),
                            (225,
                                'pattern_1_input'),
                            'pattern_1 '
                            '(reg=0xE1)')],
                        'type': 'rw'},
                {'button_title': 'pattern_2',
                        'inputs': [{'default': 255,
                            'max': 65535,
                            'colspan':1,
                            'name': 'pattern_2_input',
                            'tooltip': 'value write '
                            'to '
                            '"pattern_2 '
                            '(addr=0xE2)"',
                            'type': 'int'}],
                        'label': 'pattern 2',
                        'name': 'pattern_2',
                        'sequence': [(('_sequence_write',),
                            (226,
                                'pattern_2_input'),
                            'pattern_2 '
                            '(reg=0xE2)')],
                        'type': 'rw'},
                {'button_title': 'pattern_3',
                        'inputs': [{'default': 255,
                            'colspan':1,
                            'max': 65535,
                            'name': 'pattern_3_input',
                            'tooltip': 'value write '
                            'to '
                            '"pattern_3 '
                            '(addr=0xE3)"',
                            'type': 'int'}],
                        'label': 'pattern 3',
                        'name': 'pattern_3',
                        'sequence': [(('_sequence_write',),
                            (227,
                                'pattern_3_input'),
                            'pattern_3 '
                            '(reg=0xE3)')],
                        'type': 'rw'},
                {'button_title': 'pattern_4',
                        'inputs': [{'default': 255,
                            'max': 65535,
                            'colspan':1,
                            'name': 'pattern_4_input',
                            'tooltip': 'value write '
                            'to '
                            '"pattern_4 '
                            '(addr=0xE4)"',
                            'type': 'int'}],
                        'label': 'pattern 4',
                        'name': 'pattern_4',
                        'sequence': [(('_sequence_write',),
                            (228,
                                'pattern_4_input'),
                            'pattern_4 '
                            '(reg=0xE4)')],
                        'type': 'rw'},
                {'button_title': 'pattern_5',
                        'inputs': [{'default': 255,
                            'max': 65535,
                            'colspan':1,
                            'name': 'pattern_5_input',
                            'tooltip': 'value write '
                            'to '
                            '"pattern_5 '
                            '(addr=0xE5)"',
                            'type': 'int'}],
                        'label': 'pattern 5',
                        'name': 'pattern_5',
                        'sequence': [(('_sequence_write',),
                            (229,
                                'pattern_5_input'),
                            'pattern_5 '
                            '(reg=0xE5)')],
                        'type': 'rw'},
                {'button_title': 'pattern_6',
                        'inputs': [{'default': 255,
                            'colspan':1,
                            'max': 65535,
                            'name': 'pattern_6_input',
                            'tooltip': 'value write '
                            'to '
                            '"pattern_6 '
                            '(addr=0xE6)"',
                            'type': 'int'}],
                        'label': 'pattern 6',
                        'name': 'pattern_6',
                        'sequence': [(('_sequence_write',),
                            (230,
                                'pattern_6_input'),
                            'pattern_6 '
                            '(reg=0xE6)')],
                        'type': 'rw'},
                {'button_title': 'pattern_7',
                        'inputs': [{'default': 255,
                            'colspan':1,
                            'max': 65535,
                            'name': 'pattern_7_input',
                            'tooltip': 'value write '
                            'to '
                            '"pattern_7 '
                            '(addr=0xE7)"',
                            'type': 'int'}],
                        'label': 'pattern 7',
                        'name': 'pattern_7',
                        'sequence': [(('_sequence_write',),
                            (231,
                                'pattern_7_input'),
                            'pattern_7 '
                            '(reg=0xE7)')],
                        'type': 'rw'}
                ]
                                                 },
    'writeRegisterGroup': 
        {
                'container':'registerWriteTab',
                'grid_columns': 4,
                'sequences': [{'button_title': 'sram_data_burst',
                    'inputs': [{'default': 0,
                        'max': 65535,
                        'colspan':1,
                        'name': 'sram_data_burst_input',
                        'tooltip': 'value write to '
                        '"sram_data_burst '
                        '(addr=0x6F)"',
                        'type': 'int'}],
                    'label': 'sram data burst',
                    'name': 'sram_data_burst',
                    'sequence': [(('_sequence_write',),
                        (111,
                            'sram_data_burst_input'),
                        'sram_data_burst '
                        '(reg=0x6F)')],
                    'type': 'write'}]
                }


        }
registers=[
  {
    "name": "constant",
    "address": "0x00",
    "operation": "read",
    "default": "0xCAFE"
  },
  {
    "name": "dummy",
    "address": "0x01",
    "operation": "read/write",
    "default": "0xC0DE"
  },
  {
    "name": "status",
    "address": "0x02",
    "operation": "read",
    "default": ""
  },
  {
    "name": "triggers",
    "address": "0x06",
    "operation": "read",
    "default": ""
  },
  {
    "name": "timestamp",
    "address": "0x0E",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "operation",
    "address": "0x0F",
    "operation": "read/write",
    "default": "0x0004"
  },
  {
    "name": "heaters",
    "address": "0x20",
    "operation": "read/write",
    "default": "0x00FF"
  },
  {
    "name": "temp_90",
    "address": "0x21",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "temp_92",
    "address": "0x22",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "dac_hv1",
    "address": "0x30",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_hv2",
    "address": "0x31",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_hv3",
    "address": "0x32",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_hv4",
    "address": "0x33",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_hv5",
    "address": "0x34",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_hv6",
    "address": "0x35",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_hv7",
    "address": "0x36",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_hv8",
    "address": "0x37",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_tlevel1",
    "address": "0x38",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_tlevel2",
    "address": "0x39",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_tlevel3",
    "address": "0x3A",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_tlevel4",
    "address": "0x3B",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_tlevel5",
    "address": "0x3C",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_tlevel6",
    "address": "0x3D",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_tlevel7",
    "address": "0x3E",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_tlevel8",
    "address": "0x3F",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_bias",
    "address": "0x40",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_va",
    "address": "0x41",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_vb",
    "address": "0x42",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_rofs",
    "address": "0x4B",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_calp",
    "address": "0x4C",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "dac_calm",
    "address": "0x4D",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "calibration",
    "address": "0x4E",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "drs_config",
    "address": "0x4F",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "last_command",
    "address": "0x50",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "last_data",
    "address": "0x51",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "command_count",
    "address": "0x52",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "sram_data",
    "address": "0x60",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "sram_data_inc",
    "address": "0x61",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "sram_address_row",
    "address": "0x62",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "sram_address_col",
    "address": "0x63",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "sram_pointer_write",
    "address": "0x64",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "sram_demo_data",
    "address": "0x6E",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "sram_data_burst",
    "address": "0x6F",
    "operation": "write",
    "default": "0x0000"
  },
  {
    "name": "fifo",
    "address": "0x70",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "fifo_burst",
    "address": "0x71",
    "operation": "read",
    "default": "0x000A"
  },
  {
    "name": "fifo_burst_length",
    "address": "0x72",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "readout_mode",
    "address": "0x80",
    "operation": "read/write",
    "default": "0x0003"
  },
  {
    "name": "readout_channels",
    "address": "0x81",
    "operation": "read/write",
    "default": "0x01FF"
  },
  {
    "name": "readout_delay",
    "address": "0x82",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "readout_length",
    "address": "0x83",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "readout_start",
    "address": "0x84",
    "operation": "read/write",
    "default": "0x0000"
  },
  {
    "name": "counter_pattern_0",
    "address": "0xD0",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "counter_pattern_1",
    "address": "0xD1",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "counter_pattern_2",
    "address": "0xD2",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "counter_pattern_3",
    "address": "0xD3",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "counter_pattern_4",
    "address": "0xD4",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "counter_pattern_5",
    "address": "0xD5",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "counter_pattern_6",
    "address": "0xD6",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "counter_pattern_7",
    "address": "0xD7",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "counter_trigger_0",
    "address": "0xD8",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "counter_trigger_1",
    "address": "0xD9",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "counter_trigger_2",
    "address": "0xDA",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "counter_trigger_3",
    "address": "0xDB",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "counter_trigger_4",
    "address": "0xDC",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "counter_trigger_5",
    "address": "0xDD",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "counter_trigger_6",
    "address": "0xDE",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "counter_trigger_7",
    "address": "0xDF",
    "operation": "read",
    "default": "0x0000"
  },
  {
    "name": "pattern_0",
    "address": "0xE0",
    "operation": "read/write",
    "default": "0x00FF"
  },
  {
    "name": "pattern_1",
    "address": "0xE1",
    "operation": "read/write",
    "default": "0x00FF"
  },
  {
    "name": "pattern_2",
    "address": "0xE2",
    "operation": "read/write",
    "default": "0x00FF"
  },
  {
    "name": "pattern_3",
    "address": "0xE3",
    "operation": "read/write",
    "default": "0x00FF"
  },
  {
    "name": "pattern_4",
    "address": "0xE4",
    "operation": "read/write",
    "default": "0x00FF"
  },
  {
    "name": "pattern_5",
    "address": "0xE5",
    "operation": "read/write",
    "default": "0x00FF"
  },
  {
    "name": "pattern_6",
    "address": "0xE6",
    "operation": "read/write",
    "default": "0x00FF"
  },
  {
    "name": "pattern_7",
    "address": "0xE7",
    "operation": "read/write",
    "default": "0x00FF"
  },
  {
    "name": "debug_1",
    "address": "0xF1",
    "operation": "read",
    "default": ""
  },
  {
    "name": "debug_2",
    "address": "0xF2",
    "operation": "read",
    "default": ""
  },
  {
    "name": "debug",
    "address": "0xFF",
    "operation": "read",
    "default": ""
  }
]
