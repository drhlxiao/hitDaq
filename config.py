#!/usr/bin/python3
# -*- encoding: utf-8 -*-
'''
 configuration file
'''
config={
        'hw_init_sequences':[
        ('Reading constant register','r',(0x00,), 'hex'), #description, command type, value, response
        ('Heaters off','write_register',(0x20, 0x0F), 'hex'),
        ('Setting DAC: BIAS to 0.8V', 'w',(0x40, 0x4E10),'hex'),
        ('Setting DAC: ROFS to 1.595V','w',(0x4B,0x9FFF),'hex'),
        ('Setting DRS config register to 0xFF','w',(0x4F, 0xC0F),'hex'),
        ('Reading DRS config register ','r',(0x4F, ),'hex'),
        ('Reading the status','s',(),'')]

        }
