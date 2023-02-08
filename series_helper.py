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

from influxdb import InfluxDBClient
from influxdb import SeriesHelper

# InfluxDB connections settings
host = 'influxDB_instance_domain'
port = 8086 		# 8086 is the default port
user = 'username'
password = 'password'
dbname = 'dbname'


myclient = InfluxDBClient(host, port, user, password, dbname)


class MySeriesHelper(SeriesHelper):
    """Instantiate SeriesHelper to write points to the backend."""
    class Meta:
        """Meta class stores time series helper configuration."""
        # The client should be an instance of InfluxDBClient.
        client = myclient
        # The series name must be a string. Add dependent fields/tags in curly brackets.
        series_name = 'Switch_Power_Consumption' # total is an alternative table
        # Defines all the fields in this time series.
        fields = ['Power_Consumption', 'Metric', 'Level', 'Importance']
        # Defines all the tags for the series.
        tags = ['Interface_Name', 'Host_IP']
        # autocommit must be set to True when using bulk_size
        autocommit = True



