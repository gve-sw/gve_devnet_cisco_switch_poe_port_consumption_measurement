#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from netmiko import ConnectHandler
from series_helper import MySeriesHelper
import json
import time


# Initialize ssh session to switch
def initialize_ssh(login):
    try:
        ch = ConnectHandler(**login)
        print('Connected')
        return ch
    except ConnectionError:
        print("Could not connect")


# Get all login details from json
def get_device_details(filename):
    try:
        with open(filename) as json_file:
            devices = json.load(json_file)
        login = []
        for device in devices.items():
            login.append(device[1])
    except FileNotFoundError:
        print("File: " + str(filename) + " could not be found")
    return login


'''
# Description: Configure energywise domain on the switch, required for gathering data through this script
# parameters: ssh connection, ip
def config_domain(ssh_connection, ip):
    #Once you have a domain you can not overwrite it
    base = "energywise domain testDomain3 security shared-secret 7 cisco protocol udp port 43440 IP "
    cmd = base + ip
    config_commands = ['configure terminal', cmd]
    ssh_connection.send_config_set(config_commands)


# Description: Schedule recurring events on switch to turn on recurring events on the switch
# parameters: ssh connection, interface, level, time
def reccurring_event(ssh_connection, interface, level, time):
    #Once you have a domain you can not overwrite it
    recurrence = 'energywise level {0} recurrence importance 100 at {1}'
    recurrence = recurrence.format(level, time)
    interfaceID = 'interface ' + interface
    config_commands = ['configure terminal', interfaceID, recurrence]
    ssh_connection.send_config_set(config_commands)
'''


# Function to return a Data Frame with power consumption on each interface on a switch
# parameters: ssh connection
def get_switch_power_total_interfaces(ssh_connection):
    query = 'energywise query importance 100 name * collect usage'
    result = ssh_connection.send_command(query)[181:]                   # Send query and remove intro text
    result = result[:(result.find('Queried:'))]                         # Remove tail of text
    result_list = result.splitlines()
    print(result_list)
    for i in range(len(result_list) - 1):
        print('Host_IP: {0} Interface_Name: {1} Power_Consumption: {2} Metric: {3} Level: {4} Importance: {5}'.format(
            str(result_list[i][:18].strip()), str(result_list[i][18:46].strip()),
            str(float(result_list[i][46:52].strip())), str(result_list[i][52:58].strip()),
            str(int(result_list[i][58:66].strip())), str(int(result_list[i][66:].strip()))))
        # Can also be changed to one row and one interface as column depending on how the data should be stored
        res = MySeriesHelper(Host_IP=result_list[i][:18].strip(),  Interface_Name=result_list[i][18:46].strip(),
                              Power_Consumption=float(result_list[i][46:52].strip()), Metric=result_list[i][52:58].strip(),
                              Level=int(result_list[i][58:66].strip()), Importance=int(result_list[i][66:].strip()))
        MySeriesHelper.Meta.client.write_points(res._json_body_(), time_precision='s', retention_policy='autogen')
    # return 'Measurement sent to InfluxDB'


'''
# Function to change energywise level on interface, if interface level=0 (offline) something must trigger interface on again.
# parameters: interface name, level of energywise, ssh
def interface_state(interface, level, ssh_connection):
    current_level = (ssh_connection.send_command('show running-config interface ' + interface + ' | include energywise'))[-1:]
    if current_level != level:
        config_commands = ['configure terminal',
                           'interface ' + interface + '',
                           'energywise level ' + level + '']
        ssh_connection.send_config_set(config_commands)
        return ssh_connection.send_command('show running-config interface ' + interface + ' | include energywise')
    else:
        return 'Level already set to that value'
'''

# Value in seconds between every measurement
sleeptime = 600

if __name__ == "__main__":
    # limit amount of measurements to integer value
    # for i in range(5):
    while True:
        for login in get_device_details('devices.json'):
            get_switch_power_total_interfaces(initialize_ssh(login))
        time.sleep(sleeptime)
